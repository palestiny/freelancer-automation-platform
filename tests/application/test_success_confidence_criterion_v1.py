import pytest
from datetime import datetime, timezone

from app.application.success_confidence import SuccessConfidenceEvaluator
from app.domain.evaluation_context import (
    CriterionApplicability,
    EvaluationContext,
    Evidence,
    EvidenceKind,
    EvidenceQuality,
)
from app.domain.opportunity import Opportunity
from app.domain.opportunity_intelligence import (
    CriterionId,
    CriterionOutcome,
    EvaluationPolicy,
)
from app.domain.success_confidence import (
    SuccessComparisonOperator,
    SuccessCondition,
    SuccessConditionScope,
)


def make_opportunity() -> Opportunity:
    return Opportunity(
        source_platform="example_marketplace",
        source_opportunity_id="synthetic-success-001",
        title="Build a professional dashboard",
        description="Deliver a dashboard under explicit success conditions.",
    )


def make_context(*evidence: Evidence, applicable=True) -> EvaluationContext:
    return EvaluationContext(
        subject=make_opportunity(),
        evidence=evidence,
        evaluation_time=datetime(2026, 9, 30, 12, tzinfo=timezone.utc),
        applicability={
            CriterionId.SUCCESS_CONFIDENCE: (
                CriterionApplicability.APPLICABLE
                if applicable
                else CriterionApplicability.NOT_APPLICABLE
            )
        },
    )


def evidence(
    evidence_id: str,
    *,
    scope: SuccessConditionScope,
    signal: str,
    value,
    quality=EvidenceQuality.PRESENT_AND_USABLE,
    kind=EvidenceKind.FACT,
    uncertainty=(),
    derivation_refs=(),
) -> Evidence:
    return Evidence(
        evidence_id=evidence_id,
        kind=kind,
        value={"scope": scope.value, "signal": signal, "value": value},
        provenance="synthetic:test",
        observed_at=datetime(2026, 9, 30, 11, tzinfo=timezone.utc),
        quality=quality,
        derivation_refs=derivation_refs,
        uncertainty=uncertainty,
    )


def condition(
    condition_id="success-condition",
    *,
    scope=SuccessConditionScope.DELIVERY,
    signal="delivery_state",
    operator=SuccessComparisonOperator.ALLOWED_VALUES,
    expected_values=("DELIVERABLE",),
    evidence_refs=("success.evidence",),
) -> SuccessCondition:
    return SuccessCondition(
        condition_id=condition_id,
        scope=scope,
        signal=signal,
        operator=operator,
        expected_values=expected_values,
        evidence_refs=evidence_refs,
    )


def policy(*conditions: SuccessCondition) -> EvaluationPolicy:
    if not conditions:
        conditions = (condition(),)
    return EvaluationPolicy(
        policy_id="success-confidence-v1",
        policy_version="1",
        required_criteria=(CriterionId.SUCCESS_CONFIDENCE,),
        success_confidence_conditions=conditions,
    )


@pytest.mark.parametrize("scope", list(SuccessConditionScope))
def test_satisfied_success_condition_returns_pass_for_each_scope(scope):
    signal = f"{scope.value.lower()}_state"
    expected = "SATISFIED"
    context = make_context(
        evidence(
            "success.evidence",
            scope=scope,
            signal=signal,
            value=expected,
        )
    )

    result = SuccessConfidenceEvaluator().evaluate(
        make_opportunity(),
        policy(
            condition(
                scope=scope,
                signal=signal,
                expected_values=(expected,),
            )
        ),
        context,
    )

    assert result.outcome is CriterionOutcome.PASS


def test_explicit_policy_violation_returns_fail():
    context = make_context(
        evidence(
            "success.evidence",
            scope=SuccessConditionScope.DELIVERY,
            signal="delivery_state",
            value="BLOCKED",
        )
    )

    result = SuccessConfidenceEvaluator().evaluate(
        make_opportunity(), policy(), context
    )

    assert result.outcome is CriterionOutcome.FAIL


@pytest.mark.parametrize(
    "quality",
    [
        EvidenceQuality.PRESENT_BUT_AMBIGUOUS,
        EvidenceQuality.PRESENT_BUT_STALE,
        EvidenceQuality.PRESENT_BUT_LOW_QUALITY,
        EvidenceQuality.MISSING,
    ],
)
def test_unusable_required_evidence_returns_insufficient_data(quality):
    context = make_context(
        evidence(
            "success.evidence",
            scope=SuccessConditionScope.DELIVERY,
            signal="delivery_state",
            value="DELIVERABLE",
            quality=quality,
        )
    )

    result = SuccessConfidenceEvaluator().evaluate(
        make_opportunity(), policy(), context
    )

    assert result.outcome is CriterionOutcome.INSUFFICIENT_DATA


def test_missing_referenced_evidence_returns_insufficient_data():
    result = SuccessConfidenceEvaluator().evaluate(
        make_opportunity(), policy(), make_context()
    )

    assert result.outcome is CriterionOutcome.INSUFFICIENT_DATA
    assert result.missing_evidence == ("success.evidence",)


def test_wrong_scope_is_not_accepted():
    context = make_context(
        evidence(
            "success.evidence",
            scope=SuccessConditionScope.REQUIREMENT,
            signal="delivery_state",
            value="DELIVERABLE",
        )
    )

    result = SuccessConfidenceEvaluator().evaluate(
        make_opportunity(), policy(), context
    )

    assert result.outcome is CriterionOutcome.INSUFFICIENT_DATA


def test_wrong_signal_identity_is_not_accepted():
    context = make_context(
        evidence(
            "success.evidence",
            scope=SuccessConditionScope.DELIVERY,
            signal="acceptance_state",
            value="DELIVERABLE",
        )
    )

    result = SuccessConfidenceEvaluator().evaluate(
        make_opportunity(), policy(), context
    )

    assert result.outcome is CriterionOutcome.INSUFFICIENT_DATA


@pytest.mark.parametrize(
    "kind",
    [
        EvidenceKind.ASSUMPTION,
        EvidenceKind.HYPOTHESIS,
        EvidenceKind.FORECAST,
    ],
)
def test_unadmissible_evidence_kind_returns_insufficient_data(kind):
    context = make_context(
        evidence(
            "success.ai",
            scope=SuccessConditionScope.DELIVERY,
            signal="delivery_state",
            value="DELIVERABLE",
            kind=kind,
        )
    )

    result = SuccessConfidenceEvaluator().evaluate(
        make_opportunity(),
        policy(),
        context,
    )

    assert result.outcome is CriterionOutcome.INSUFFICIENT_DATA


@pytest.mark.parametrize(
    "kind",
    [
        EvidenceKind.FACT,
        EvidenceKind.OBSERVATION,
        EvidenceKind.ESTIMATE,
        EvidenceKind.EXPERIMENT_RESULT,
    ],
)
def test_admissible_evidence_kinds_can_establish_success(kind):
    context = make_context(
        evidence(
            "success.evidence",
            scope=SuccessConditionScope.DELIVERY,
            signal="delivery_state",
            value="DELIVERABLE",
            kind=kind,
        )
    )

    result = SuccessConfidenceEvaluator().evaluate(
        make_opportunity(), policy(), context
    )

    assert result.outcome is CriterionOutcome.PASS


def test_conflicting_usable_values_without_precedence_return_insufficient_data():
    context = make_context(
        evidence(
            "success-a",
            scope=SuccessConditionScope.DELIVERY,
            signal="delivery_state",
            value="DELIVERABLE",
        ),
        evidence(
            "success-b",
            scope=SuccessConditionScope.DELIVERY,
            signal="delivery_state",
            value="BLOCKED",
        ),
    )

    result = SuccessConfidenceEvaluator().evaluate(
        make_opportunity(),
        policy(condition(evidence_refs=("success-a", "success-b"))),
        context,
    )

    assert result.outcome is CriterionOutcome.INSUFFICIENT_DATA
    assert result.evidence_refs == ("success-a", "success-b")


def test_violation_plus_unresolved_evidence_is_conservative():
    context = make_context(
        evidence(
            "success-a",
            scope=SuccessConditionScope.DELIVERY,
            signal="delivery_state",
            value="BLOCKED",
        ),
        evidence(
            "success-b",
            scope=SuccessConditionScope.DELIVERY,
            signal="delivery_state",
            value="DELIVERABLE",
            quality=EvidenceQuality.PRESENT_BUT_AMBIGUOUS,
        ),
    )

    result = SuccessConfidenceEvaluator().evaluate(
        make_opportunity(),
        policy(condition(evidence_refs=("success-a", "success-b"))),
        context,
    )

    assert result.outcome is CriterionOutcome.INSUFFICIENT_DATA


def test_not_applicable_requires_explicit_context():
    result = SuccessConfidenceEvaluator().evaluate(
        make_opportunity(), policy(), make_context(applicable=False)
    )

    assert result.outcome is CriterionOutcome.NOT_APPLICABLE


def test_empty_condition_set_returns_not_applicable():
    context = make_context()
    empty_policy = EvaluationPolicy(
        policy_id="success-confidence-v1",
        policy_version="1",
        required_criteria=(CriterionId.SUCCESS_CONFIDENCE,),
        success_confidence_conditions=(),
    )

    result = SuccessConfidenceEvaluator().evaluate(
        make_opportunity(), empty_policy, context
    )

    assert result.outcome is CriterionOutcome.NOT_APPLICABLE


def test_no_success_evidence_is_not_inferred_from_opportunity_fields():
    opportunity = Opportunity(
        source_platform="example_marketplace",
        source_opportunity_id="synthetic-success-002",
        title="DELIVERABLE WITHIN_DEADLINE BLOCKERS_RESOLVED",
        description="The text contains success-looking claims but no evidence.",
    )
    context = EvaluationContext(
        subject=opportunity,
        evidence=(),
        evaluation_time=datetime(2026, 9, 30, 12, tzinfo=timezone.utc),
    )

    result = SuccessConfidenceEvaluator().evaluate(
        opportunity,
        policy(),
        context,
    )

    assert result.outcome is CriterionOutcome.INSUFFICIENT_DATA


def test_context_for_different_opportunity_is_rejected():
    context = make_context(
        evidence(
            "success.evidence",
            scope=SuccessConditionScope.DELIVERY,
            signal="delivery_state",
            value="DELIVERABLE",
        )
    )
    other = Opportunity(
        source_platform="example_marketplace",
        source_opportunity_id="different",
        title="Different opportunity",
        description="Different description.",
    )

    with pytest.raises(ValueError, match="subject"):
        SuccessConfidenceEvaluator().evaluate(other, policy(), context)


def test_policy_rejects_duplicate_condition_ids():
    first = condition()
    second = condition(
        condition_id=first.condition_id,
        signal="deadline_state",
    )

    with pytest.raises(ValueError, match="duplicate ids"):
        EvaluationPolicy(
            policy_id="success-confidence-v1",
            policy_version="1",
            required_criteria=(CriterionId.SUCCESS_CONFIDENCE,),
            success_confidence_conditions=(first, second),
        )


def test_condition_rejects_duplicate_evidence_references():
    with pytest.raises(ValueError, match="duplicates"):
        condition(evidence_refs=("success.evidence", "success.evidence"))


def test_derived_success_evidence_requires_explicit_lineage():
    context = make_context(
        Evidence(
            evidence_id="success.derived",
            kind=EvidenceKind.OBSERVATION,
            value={
                "scope": SuccessConditionScope.DEADLINE.value,
                "signal": "deadline_state",
                "value": "WITHIN_DEADLINE",
            },
            provenance="derived:test",
            observed_at=datetime(2026, 9, 30, 11, tzinfo=timezone.utc),
            quality=EvidenceQuality.PRESENT_AND_USABLE,
            derivation_refs=("deadline.source",),
        ),
        evidence(
            "deadline.source",
            scope=SuccessConditionScope.DEADLINE,
            signal="deadline_input",
            value="CALCULATED",
        ),
    )

    result = SuccessConfidenceEvaluator().evaluate(
        make_opportunity(),
        policy(
            condition(
                scope=SuccessConditionScope.DEADLINE,
                signal="deadline_state",
                expected_values=("WITHIN_DEADLINE",),
                evidence_refs=("success.derived",),
            )
        ),
        context,
    )

    assert result.outcome is CriterionOutcome.PASS


def test_unknown_operator_is_rejected():
    with pytest.raises(ValueError, match="supported SuccessComparisonOperator"):
        SuccessCondition(
            condition_id="invalid",
            scope=SuccessConditionScope.DELIVERY,
            signal="delivery_state",
            operator="UNKNOWN",
            expected_values=("DELIVERABLE",),
            evidence_refs=("success.evidence",),
        )


def test_empty_expected_values_are_rejected():
    with pytest.raises(ValueError, match="expected_values"):
        SuccessCondition(
            condition_id="invalid",
            scope=SuccessConditionScope.DELIVERY,
            signal="delivery_state",
            operator=SuccessComparisonOperator.ALLOWED_VALUES,
            expected_values=(),
            evidence_refs=("success.evidence",),
        )


def test_success_condition_rejects_unknown_scope():
    with pytest.raises(ValueError, match="SuccessConditionScope"):
        SuccessCondition(
            condition_id="invalid",
            scope="UNKNOWN",
            signal="delivery_state",
            operator=SuccessComparisonOperator.ALLOWED_VALUES,
            expected_values=("DELIVERABLE",),
            evidence_refs=("success.evidence",),
        )


def test_policy_identity_uncertainty_and_evidence_refs_are_preserved():
    context = make_context(
        evidence(
            "success.evidence",
            scope=SuccessConditionScope.DELIVERY,
            signal="delivery_state",
            value="DELIVERABLE",
            uncertainty=("delivery evidence is based on a current plan",),
        )
    )

    result = SuccessConfidenceEvaluator().evaluate(
        make_opportunity(), policy(), context
    )

    assert result.policy_id == "success-confidence-v1"
    assert result.policy_version == "1"
    assert result.evidence_refs == ("success.evidence",)
    assert result.uncertainty == ("delivery evidence is based on a current plan",)
    assert not hasattr(result, "score")
    assert not hasattr(result, "confidence")
    assert not hasattr(result, "probability")


def test_criterion_outcomes_are_not_accepted_as_evidence():
    context = make_context(
        Evidence(
            evidence_id="criterion.result",
            kind=EvidenceKind.FACT,
            value={
                "criterion_id": CriterionId.REQUIREMENT_FIT.value,
                "outcome": CriterionOutcome.PASS.value,
            },
            provenance="synthetic:criterion-result",
            observed_at=datetime(2026, 9, 30, 11, tzinfo=timezone.utc),
            quality=EvidenceQuality.PRESENT_AND_USABLE,
        )
    )

    result = SuccessConfidenceEvaluator().evaluate(
        make_opportunity(),
        policy(),
        context,
    )

    assert result.outcome is CriterionOutcome.INSUFFICIENT_DATA


def test_identical_snapshot_is_deterministic():
    context = make_context(
        evidence(
            "success.evidence",
            scope=SuccessConditionScope.DELIVERY,
            signal="delivery_state",
            value="DELIVERABLE",
        )
    )
    selected_policy = policy()

    first = SuccessConfidenceEvaluator().evaluate(
        make_opportunity(), selected_policy, context
    )
    second = SuccessConfidenceEvaluator().evaluate(
        make_opportunity(), selected_policy, context
    )

    assert first == second
