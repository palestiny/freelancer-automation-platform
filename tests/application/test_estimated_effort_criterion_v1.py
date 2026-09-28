from datetime import datetime, timezone

from app.application.estimated_effort import EstimatedEffortEvaluator
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
from app.domain.estimated_effort import EffortConstraint


def make_opportunity() -> Opportunity:
    return Opportunity(
        source_platform="example_marketplace",
        source_opportunity_id="synthetic-estimated-effort-001",
        title="Build a React dashboard",
        description="Implement dashboard pages and responsive layouts.",
    )


def make_context(*evidence: Evidence, applicable=True) -> EvaluationContext:
    return EvaluationContext(
        subject=make_opportunity(),
        evidence=evidence,
        evaluation_time=datetime(2026, 9, 28, 12, tzinfo=timezone.utc),
        applicability={
            CriterionId.ESTIMATED_EFFORT: (
                CriterionApplicability.APPLICABLE
                if applicable
                else CriterionApplicability.NOT_APPLICABLE
            )
        },
    )


def policy(*constraints: EffortConstraint) -> EvaluationPolicy:
    return EvaluationPolicy(
        policy_id="estimated-effort-v1",
        policy_version="1",
        required_criteria=(CriterionId.ESTIMATED_EFFORT,),
        estimated_effort_constraints=constraints,
    )


def effort_evidence(
    evidence_id: str,
    value: int,
    *,
    unit="HOURS",
    scope_refs=("scope.dashboard",),
    quality=EvidenceQuality.PRESENT_AND_USABLE,
    uncertainty=(),
    kind=EvidenceKind.ESTIMATE,
) -> Evidence:
    return Evidence(
        evidence_id=evidence_id,
        kind=kind,
        value={"value": value, "unit": unit, "scope_refs": scope_refs},
        provenance="synthetic:test",
        observed_at=datetime(2026, 9, 28, 11, tzinfo=timezone.utc),
        quality=quality,
        uncertainty=uncertainty,
    )


def constraint(
    constraint_id: str = "max-hours",
    *,
    maximum_value=40,
    unit="HOURS",
    evidence_refs=("effort.estimate",),
    required_scope_refs=("scope.dashboard",),
) -> EffortConstraint:
    return EffortConstraint(
        constraint_id=constraint_id,
        maximum_value=maximum_value,
        unit=unit,
        evidence_refs=evidence_refs,
        required_scope_refs=required_scope_refs,
    )


def test_usable_estimate_within_explicit_policy_constraint_returns_pass():
    context = make_context(effort_evidence("effort.estimate", 20))
    result = EstimatedEffortEvaluator().evaluate(make_opportunity(), policy(constraint()), context)
    assert result.outcome is CriterionOutcome.PASS
    assert result.evidence_refs == ("effort.estimate",)


def test_explicit_effort_constraint_violation_returns_fail():
    context = make_context(effort_evidence("effort.estimate", 50))
    result = EstimatedEffortEvaluator().evaluate(make_opportunity(), policy(constraint()), context)
    assert result.outcome is CriterionOutcome.FAIL


def test_missing_required_effort_evidence_returns_insufficient_data():
    result = EstimatedEffortEvaluator().evaluate(make_opportunity(), policy(constraint()), make_context())
    assert result.outcome is CriterionOutcome.INSUFFICIENT_DATA
    assert result.missing_evidence == ("effort.estimate",)


def test_missing_scope_does_not_allow_estimate_to_pass():
    context = make_context(effort_evidence("effort.estimate", 20, scope_refs=()))
    result = EstimatedEffortEvaluator().evaluate(make_opportunity(), policy(constraint()), context)
    assert result.outcome is CriterionOutcome.INSUFFICIENT_DATA


def test_ambiguous_estimate_returns_insufficient_data():
    context = make_context(effort_evidence("effort.estimate", 20, quality=EvidenceQuality.PRESENT_BUT_AMBIGUOUS))
    result = EstimatedEffortEvaluator().evaluate(make_opportunity(), policy(constraint()), context)
    assert result.outcome is CriterionOutcome.INSUFFICIENT_DATA


def test_stale_estimate_returns_insufficient_data():
    context = make_context(effort_evidence("effort.estimate", 20, quality=EvidenceQuality.PRESENT_BUT_STALE))
    result = EstimatedEffortEvaluator().evaluate(make_opportunity(), policy(constraint()), context)
    assert result.outcome is CriterionOutcome.INSUFFICIENT_DATA


def test_low_quality_estimate_returns_insufficient_data():
    context = make_context(effort_evidence("effort.estimate", 20, quality=EvidenceQuality.PRESENT_BUT_LOW_QUALITY))
    result = EstimatedEffortEvaluator().evaluate(make_opportunity(), policy(constraint()), context)
    assert result.outcome is CriterionOutcome.INSUFFICIENT_DATA


def test_conflicting_usable_estimates_without_policy_precedence_return_insufficient_data():
    context = make_context(effort_evidence("effort-a", 20), effort_evidence("effort-b", 50))
    result = EstimatedEffortEvaluator().evaluate(
        make_opportunity(),
        policy(constraint(evidence_refs=("effort-a", "effort-b"))),
        context,
    )
    assert result.outcome is CriterionOutcome.INSUFFICIENT_DATA
    assert result.evidence_refs == ("effort-a", "effort-b")


def test_assumption_is_not_treated_as_effort_estimate():
    context = make_context(effort_evidence("effort.assumption", 20, kind=EvidenceKind.ASSUMPTION))
    result = EstimatedEffortEvaluator().evaluate(
        make_opportunity(),
        policy(constraint(evidence_refs=("effort.assumption",))),
        context,
    )
    assert result.outcome is CriterionOutcome.INSUFFICIENT_DATA


def test_uncertainty_is_preserved_and_not_converted_to_a_score():
    context = make_context(
        effort_evidence("effort.estimate", 20, uncertainty=("requirements ambiguity",))
    )
    result = EstimatedEffortEvaluator().evaluate(make_opportunity(), policy(constraint()), context)
    assert result.outcome is CriterionOutcome.PASS
    assert result.uncertainty == ("requirements ambiguity",)
    assert not hasattr(result, "score")
    assert not hasattr(result, "confidence")


def test_not_applicable_requires_explicit_context():
    result = EstimatedEffortEvaluator().evaluate(
        make_opportunity(),
        policy(constraint()),
        make_context(applicable=False),
    )
    assert result.outcome is CriterionOutcome.NOT_APPLICABLE


def test_estimated_effort_does_not_infer_from_opportunity_fields():
    opportunity = Opportunity(
        source_platform="example_marketplace",
        source_opportunity_id="synthetic-estimated-effort-002",
        title="Two hour React task",
        description="Tiny task, easy to complete quickly.",
    )
    context = EvaluationContext(
        subject=opportunity,
        evidence=(),
        evaluation_time=datetime(2026, 9, 28, 12, tzinfo=timezone.utc),
    )
    result = EstimatedEffortEvaluator().evaluate(opportunity, policy(constraint()), context)
    assert result.outcome is CriterionOutcome.INSUFFICIENT_DATA


def test_estimate_unit_mismatch_is_not_silently_converted():
    context = make_context(effort_evidence("effort.estimate", 20, unit="DAYS"))
    result = EstimatedEffortEvaluator().evaluate(
        make_opportunity(), policy(constraint(unit="HOURS")), context
    )
    assert result.outcome is CriterionOutcome.INSUFFICIENT_DATA


def test_context_for_different_opportunity_is_rejected():
    context = make_context(effort_evidence("effort.estimate", 20))
    other = Opportunity(
        source_platform="example_marketplace",
        source_opportunity_id="different",
        title="Different opportunity",
        description="Different description.",
    )
    try:
        EstimatedEffortEvaluator().evaluate(other, policy(constraint()), context)
    except ValueError as exc:
        assert "subject" in str(exc)
    else:
        raise AssertionError("mismatched evaluation subject must be rejected")


def test_policy_identity_is_preserved():
    context = make_context(effort_evidence("effort.estimate", 20))
    result = EstimatedEffortEvaluator().evaluate(make_opportunity(), policy(constraint()), context)
    assert result.policy_id == "estimated-effort-v1"
    assert result.policy_version == "1"
