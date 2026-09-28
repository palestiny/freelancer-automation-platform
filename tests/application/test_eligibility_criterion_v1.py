from datetime import datetime, timezone

from app.application.eligibility import EligibilityEvaluator
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
from app.domain.eligibility import EligibilityConstraint


def make_opportunity() -> Opportunity:
    return Opportunity(
        source_platform="example_marketplace",
        source_opportunity_id="synthetic-eligibility-001",
        title="Build a React dashboard",
        description="Create a responsive dashboard.",
    )


def make_context(*evidence: Evidence, applicable=True) -> EvaluationContext:
    return EvaluationContext(
        subject=make_opportunity(),
        evidence=evidence,
        evaluation_time=datetime(2026, 9, 28, 12, tzinfo=timezone.utc),
        applicability={
            CriterionId.ELIGIBILITY: (
                CriterionApplicability.APPLICABLE
                if applicable
                else CriterionApplicability.NOT_APPLICABLE
            )
        },
    )


def policy(*constraints: EligibilityConstraint) -> EvaluationPolicy:
    return EvaluationPolicy(
        policy_id="eligibility-v1",
        policy_version="1",
        required_criteria=(CriterionId.ELIGIBILITY,),
        eligibility_constraints=constraints,
    )


def evidence(
    evidence_id: str,
    value: str,
    *,
    quality=EvidenceQuality.PRESENT_AND_USABLE,
) -> Evidence:
    return Evidence(
        evidence_id=evidence_id,
        kind=EvidenceKind.FACT,
        value=value,
        provenance="synthetic:test",
        observed_at=datetime(2026, 9, 28, 11, tzinfo=timezone.utc),
        quality=quality,
    )


def constraint(constraint_id: str, *evidence_ids: str, allowed=("OPEN",)) -> EligibilityConstraint:
    return EligibilityConstraint(
        constraint_id=constraint_id,
        evidence_refs=evidence_ids,
        allowed_values=allowed,
    )


def test_satisfied_status_constraint_returns_pass():
    context = make_context(evidence("opportunity.status", "OPEN"))
    result = EligibilityEvaluator().evaluate(make_opportunity(), policy(
        constraint("status-open", "opportunity.status")
    ), context)

    assert result.outcome is CriterionOutcome.PASS
    assert result.evidence_refs == ("opportunity.status",)


def test_violated_status_constraint_returns_fail():
    context = make_context(evidence("opportunity.status", "CLOSED"))
    result = EligibilityEvaluator().evaluate(make_opportunity(), policy(
        constraint("status-open", "opportunity.status")
    ), context)

    assert result.outcome is CriterionOutcome.FAIL
    assert result.evidence_refs == ("opportunity.status",)


def test_missing_required_evidence_returns_insufficient_data():
    context = make_context()
    result = EligibilityEvaluator().evaluate(make_opportunity(), policy(
        constraint("status-open", "opportunity.status")
    ), context)

    assert result.outcome is CriterionOutcome.INSUFFICIENT_DATA
    assert result.missing_evidence == ("opportunity.status",)


def test_ambiguous_evidence_returns_insufficient_data():
    context = make_context(
        evidence(
            "opportunity.status",
            "OPEN OR CLOSED",
            quality=EvidenceQuality.PRESENT_BUT_AMBIGUOUS,
        )
    )
    result = EligibilityEvaluator().evaluate(make_opportunity(), policy(
        constraint("status-open", "opportunity.status")
    ), context)

    assert result.outcome is CriterionOutcome.INSUFFICIENT_DATA
    assert "opportunity.status" in result.evidence_refs


def test_stale_evidence_returns_insufficient_data():
    context = make_context(
        evidence(
            "opportunity.status",
            "OPEN",
            quality=EvidenceQuality.PRESENT_BUT_STALE,
        )
    )
    result = EligibilityEvaluator().evaluate(make_opportunity(), policy(
        constraint("status-open", "opportunity.status")
    ), context)

    assert result.outcome is CriterionOutcome.INSUFFICIENT_DATA


def test_low_quality_evidence_returns_insufficient_data():
    context = make_context(
        evidence(
            "opportunity.status",
            "OPEN",
            quality=EvidenceQuality.PRESENT_BUT_LOW_QUALITY,
        )
    )
    result = EligibilityEvaluator().evaluate(make_opportunity(), policy(
        constraint("status-open", "opportunity.status")
    ), context)

    assert result.outcome is CriterionOutcome.INSUFFICIENT_DATA


def test_no_applicable_constraints_returns_not_applicable():
    context = make_context(applicable=False)
    result = EligibilityEvaluator().evaluate(make_opportunity(), policy(), context)

    assert result.outcome is CriterionOutcome.NOT_APPLICABLE


def test_title_or_budget_does_not_infer_eligibility():
    opportunity = Opportunity(
        source_platform="example_marketplace",
        source_opportunity_id="synthetic-eligibility-002",
        title="OPEN urgent project budget $5000",
        description="Client has excellent reputation.",
    )

    result = EligibilityEvaluator().evaluate(
        opportunity,
        policy(constraint("status-open", "opportunity.status")),
        EvaluationContext(
            subject=opportunity,
            evidence=(),
            evaluation_time=datetime(2026, 9, 28, 12, tzinfo=timezone.utc),
        ),
    )

    assert result.outcome is CriterionOutcome.INSUFFICIENT_DATA


def test_contradictory_evidence_without_precedence_returns_insufficient_data():
    context = make_context(
        evidence("status-observation-a", "OPEN"),
        evidence("status-observation-b", "CLOSED"),
    )
    result = EligibilityEvaluator().evaluate(make_opportunity(), policy(
        constraint(
            "status-open",
            "status-observation-a",
            "status-observation-b",
        )
    ), context)

    assert result.outcome is CriterionOutcome.INSUFFICIENT_DATA
    assert result.evidence_refs == (
        "status-observation-a",
        "status-observation-b",
    )


def test_policy_version_is_preserved():
    context = make_context(evidence("opportunity.type", "FREELANCE"))
    result = EligibilityEvaluator().evaluate(make_opportunity(), policy(
        constraint("type-freelance", "opportunity.type", allowed=("FREELANCE",))
    ), context)

    assert result.policy_id == "eligibility-v1"
    assert result.policy_version == "1"


def test_identical_snapshot_is_deterministic():
    context = make_context(evidence("opportunity.status", "OPEN"))
    selected_policy = policy(constraint("status-open", "opportunity.status"))

    first = EligibilityEvaluator().evaluate(make_opportunity(), selected_policy, context)
    second = EligibilityEvaluator().evaluate(make_opportunity(), selected_policy, context)

    assert first == second


def test_context_for_different_opportunity_is_rejected():
    context = make_context(evidence("opportunity.status", "OPEN"))
    other = Opportunity(
        source_platform="example_marketplace",
        source_opportunity_id="different",
        title="Different opportunity",
        description="Different description.",
    )

    try:
        EligibilityEvaluator().evaluate(
            other,
            policy(constraint("status-open", "opportunity.status")),
            context,
        )
    except ValueError as exc:
        assert "subject" in str(exc)
    else:
        raise AssertionError("mismatched evaluation subject must be rejected")


def test_constraint_rejects_duplicate_evidence_references():
    try:
        EligibilityConstraint(
            constraint_id="invalid",
            evidence_refs=("status", "status"),
            allowed_values=("OPEN",),
        )
    except ValueError as exc:
        assert "duplicates" in str(exc)
    else:
        raise AssertionError("duplicate evidence references must be rejected")


def test_constraint_rejects_empty_allowed_values():
    try:
        EligibilityConstraint(
            constraint_id="invalid",
            evidence_refs=("status",),
            allowed_values=(),
        )
    except ValueError as exc:
        assert "allowed values" in str(exc)
    else:
        raise AssertionError("empty allowed values must be rejected")
