import pytest
from datetime import datetime, timezone

from app.application.client_project_risk import ClientProjectRiskEvaluator
from app.domain.client_project_risk import RiskComparisonOperator, RiskConstraint, RiskScope
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


def make_opportunity() -> Opportunity:
    return Opportunity(
        source_platform="example_marketplace",
        source_opportunity_id="synthetic-risk-001",
        title="Build a professional dashboard",
        description="Deliver a dashboard under explicit client requirements.",
    )


def make_context(*evidence: Evidence, applicable=True) -> EvaluationContext:
    return EvaluationContext(
        subject=make_opportunity(),
        evidence=evidence,
        evaluation_time=datetime(2026, 9, 29, 12, tzinfo=timezone.utc),
        applicability={
            CriterionId.CLIENT_PROJECT_RISK: (
                CriterionApplicability.APPLICABLE
                if applicable
                else CriterionApplicability.NOT_APPLICABLE
            )
        },
    )


def evidence(
    evidence_id: str,
    *,
    scope: RiskScope,
    signal: str,
    value,
    quality=EvidenceQuality.PRESENT_AND_USABLE,
    kind=EvidenceKind.FACT,
    uncertainty=(),
) -> Evidence:
    return Evidence(
        evidence_id=evidence_id,
        kind=kind,
        value={"scope": scope.value, "signal": signal, "value": value},
        provenance="synthetic:test",
        observed_at=datetime(2026, 9, 29, 11, tzinfo=timezone.utc),
        quality=quality,
        uncertainty=uncertainty,
    )


def constraint(
    constraint_id="risk-constraint",
    *,
    scope=RiskScope.PROJECT,
    signal="scope_stability",
    operator=RiskComparisonOperator.ALLOWED_VALUES,
    expected_values=("STABLE",),
    evidence_refs=("risk.evidence",),
) -> RiskConstraint:
    return RiskConstraint(
        constraint_id=constraint_id,
        scope=scope,
        signal=signal,
        operator=operator,
        expected_values=expected_values,
        evidence_refs=evidence_refs,
    )


def policy(*constraints: RiskConstraint) -> EvaluationPolicy:
    if not constraints:
        constraints = (constraint(),)
    return EvaluationPolicy(
        policy_id="client-project-risk-v1",
        policy_version="1",
        required_criteria=(CriterionId.CLIENT_PROJECT_RISK,),
        client_project_risk_constraints=constraints,
    )


def test_satisfied_project_risk_constraint_returns_pass():
    context = make_context(
        evidence(
            "risk.evidence",
            scope=RiskScope.PROJECT,
            signal="scope_stability",
            value="STABLE",
        )
    )

    result = ClientProjectRiskEvaluator().evaluate(
        make_opportunity(), policy(), context
    )

    assert result.outcome is CriterionOutcome.PASS
    assert result.evidence_refs == ("risk.evidence",)


def test_satisfied_client_risk_constraint_returns_pass():
    context = make_context(
        evidence(
            "risk.client",
            scope=RiskScope.CLIENT,
            signal="acceptance_condition",
            value="EXPLICIT",
        )
    )

    result = ClientProjectRiskEvaluator().evaluate(
        make_opportunity(),
        policy(
            constraint(
                scope=RiskScope.CLIENT,
                signal="acceptance_condition",
                expected_values=("EXPLICIT",),
                evidence_refs=("risk.client",),
            )
        ),
        context,
    )

    assert result.outcome is CriterionOutcome.PASS


def test_explicit_policy_violation_returns_fail():
    context = make_context(
        evidence(
            "risk.evidence",
            scope=RiskScope.PROJECT,
            signal="scope_stability",
            value="UNSTABLE",
        )
    )

    result = ClientProjectRiskEvaluator().evaluate(make_opportunity(), policy(), context)

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
            "risk.evidence",
            scope=RiskScope.PROJECT,
            signal="scope_stability",
            value="STABLE",
            quality=quality,
        )
    )

    result = ClientProjectRiskEvaluator().evaluate(
        make_opportunity(), policy(), context
    )

    assert result.outcome is CriterionOutcome.INSUFFICIENT_DATA


def test_missing_referenced_evidence_returns_insufficient_data():
    result = ClientProjectRiskEvaluator().evaluate(
        make_opportunity(), policy(), make_context()
    )

    assert result.outcome is CriterionOutcome.INSUFFICIENT_DATA
    assert result.missing_evidence == ("risk.evidence",)


def test_wrong_scope_is_not_accepted():
    context = make_context(
        evidence(
            "risk.evidence",
            scope=RiskScope.CLIENT,
            signal="scope_stability",
            value="STABLE",
        )
    )

    result = ClientProjectRiskEvaluator().evaluate(
        make_opportunity(), policy(), context
    )

    assert result.outcome is CriterionOutcome.INSUFFICIENT_DATA


def test_wrong_signal_identity_is_not_accepted():
    context = make_context(
        evidence(
            "risk.evidence",
            scope=RiskScope.PROJECT,
            signal="deadline_pressure",
            value="STABLE",
        )
    )

    result = ClientProjectRiskEvaluator().evaluate(
        make_opportunity(), policy(), context
    )

    assert result.outcome is CriterionOutcome.INSUFFICIENT_DATA


def test_conflicting_usable_values_without_precedence_return_insufficient_data():
    context = make_context(
        evidence(
            "risk-a",
            scope=RiskScope.PROJECT,
            signal="scope_stability",
            value="STABLE",
        ),
        evidence(
            "risk-b",
            scope=RiskScope.PROJECT,
            signal="scope_stability",
            value="UNSTABLE",
        ),
    )

    result = ClientProjectRiskEvaluator().evaluate(
        make_opportunity(),
        policy(
            constraint(evidence_refs=("risk-a", "risk-b")),
        ),
        context,
    )

    assert result.outcome is CriterionOutcome.INSUFFICIENT_DATA
    assert result.evidence_refs == ("risk-a", "risk-b")


def test_violation_plus_unresolved_evidence_is_conservative():
    context = make_context(
        evidence(
            "risk-a",
            scope=RiskScope.PROJECT,
            signal="scope_stability",
            value="UNSTABLE",
        ),
        evidence(
            "risk-b",
            scope=RiskScope.PROJECT,
            signal="scope_stability",
            value="STABLE",
            quality=EvidenceQuality.PRESENT_BUT_AMBIGUOUS,
        ),
    )

    result = ClientProjectRiskEvaluator().evaluate(
        make_opportunity(),
        policy(constraint(evidence_refs=("risk-a", "risk-b"))),
        context,
    )

    assert result.outcome is CriterionOutcome.INSUFFICIENT_DATA


def test_not_applicable_requires_explicit_context():
    result = ClientProjectRiskEvaluator().evaluate(
        make_opportunity(), policy(), make_context(applicable=False)
    )

    assert result.outcome is CriterionOutcome.NOT_APPLICABLE


def test_no_risk_evidence_is_not_inferred_from_opportunity_fields():
    opportunity = Opportunity(
        source_platform="example_marketplace",
        source_opportunity_id="synthetic-risk-002",
        title="Stable scope, explicit acceptance, trusted client",
        description="No evidence snapshot was supplied.",
    )
    context = EvaluationContext(
        subject=opportunity,
        evidence=(),
        evaluation_time=datetime(2026, 9, 29, 12, tzinfo=timezone.utc),
    )

    result = ClientProjectRiskEvaluator().evaluate(
        opportunity,
        policy(),
        context,
    )

    assert result.outcome is CriterionOutcome.INSUFFICIENT_DATA


def test_policy_identity_uncertainty_and_evidence_refs_are_preserved():
    context = make_context(
        evidence(
            "risk.evidence",
            scope=RiskScope.PROJECT,
            signal="scope_stability",
            value="STABLE",
            uncertainty=("scope interpretation remains uncertain",),
        )
    )

    result = ClientProjectRiskEvaluator().evaluate(
        make_opportunity(), policy(), context
    )

    assert result.policy_id == "client-project-risk-v1"
    assert result.policy_version == "1"
    assert result.evidence_refs == ("risk.evidence",)
    assert result.uncertainty == ("scope interpretation remains uncertain",)
    assert not hasattr(result, "score")
    assert not hasattr(result, "confidence")


def test_context_for_different_opportunity_is_rejected():
    context = make_context(
        evidence(
            "risk.evidence",
            scope=RiskScope.PROJECT,
            signal="scope_stability",
            value="STABLE",
        )
    )
    other = Opportunity(
        source_platform="example_marketplace",
        source_opportunity_id="different",
        title="Different opportunity",
        description="Different description.",
    )

    with pytest.raises(ValueError, match="subject"):
        ClientProjectRiskEvaluator().evaluate(other, policy(), context)


def test_policy_rejects_duplicate_risk_constraint_ids():
    first = constraint()
    second = constraint(
        constraint_id=first.constraint_id,
        signal="deadline_pressure",
    )

    with pytest.raises(ValueError, match="duplicate ids"):
        EvaluationPolicy(
            policy_id="client-project-risk-v1",
            policy_version="1",
            required_criteria=(CriterionId.CLIENT_PROJECT_RISK,),
            client_project_risk_constraints=(first, second),
        )


def test_constraint_rejects_duplicate_evidence_references():
    with pytest.raises(ValueError, match="duplicates"):
        constraint(evidence_refs=("risk.evidence", "risk.evidence"))


def test_ai_assertion_is_not_accepted_without_explicit_policy_evidence_kind():
    context = make_context(
        evidence(
            "risk.ai",
            scope=RiskScope.CLIENT,
            signal="trust_assessment",
            value="LOW_RISK",
            kind=EvidenceKind.HYPOTHESIS,
        )
    )

    result = ClientProjectRiskEvaluator().evaluate(
        make_opportunity(),
        policy(
            constraint(
                scope=RiskScope.CLIENT,
                signal="trust_assessment",
                expected_values=("LOW_RISK",),
                evidence_refs=("risk.ai",),
            )
        ),
        context,
    )

    assert result.outcome is CriterionOutcome.INSUFFICIENT_DATA


def test_derived_risk_evidence_requires_lineage_and_explicit_kind():
    context = make_context(
        Evidence(
            evidence_id="risk.derived",
            kind=EvidenceKind.OBSERVATION,
            value={
                "scope": RiskScope.PROJECT.value,
                "signal": "scope_stability",
                "value": "STABLE",
            },
            provenance="derived:test",
            observed_at=datetime(2026, 9, 29, 11, tzinfo=timezone.utc),
            quality=EvidenceQuality.PRESENT_AND_USABLE,
            derivation_refs=("risk.source",),
        ),
        evidence(
            "risk.source",
            scope=RiskScope.PROJECT,
            signal="scope_observation",
            value="EXPLICIT",
        ),
    )

    result = ClientProjectRiskEvaluator().evaluate(
        make_opportunity(), policy(), context
    )

    assert result.outcome is CriterionOutcome.PASS


def test_unknown_operator_is_rejected():
    with pytest.raises(ValueError, match="supported RiskComparisonOperator"):
        RiskConstraint(
            constraint_id="invalid",
            scope=RiskScope.PROJECT,
            signal="scope_stability",
            operator="UNKNOWN",
            expected_values=("STABLE",),
            evidence_refs=("risk.evidence",),
        )


def test_empty_expected_values_are_rejected():
    with pytest.raises(ValueError, match="expected_values"):
        RiskConstraint(
            constraint_id="invalid",
            scope=RiskScope.PROJECT,
            signal="scope_stability",
            operator=RiskComparisonOperator.ALLOWED_VALUES,
            expected_values=(),
            evidence_refs=("risk.evidence",),
        )


def test_risk_constraint_rejects_unknown_scope():
    with pytest.raises(ValueError, match="RiskScope"):
        RiskConstraint(
            constraint_id="invalid",
            scope="UNKNOWN",
            signal="scope_stability",
            operator=RiskComparisonOperator.ALLOWED_VALUES,
            expected_values=("STABLE",),
            evidence_refs=("risk.evidence",),
        )
