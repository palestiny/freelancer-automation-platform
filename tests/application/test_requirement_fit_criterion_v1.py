from datetime import datetime, timezone

from app.application.requirement_fit import RequirementFitEvaluator
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
from app.domain.requirement_fit import CapabilityRequirement


def make_opportunity() -> Opportunity:
    return Opportunity(
        source_platform="example_marketplace",
        source_opportunity_id="synthetic-requirement-fit-001",
        title="Build a React dashboard",
        description="Create a responsive dashboard.",
        required_capabilities=frozenset({"react"}),
    )


def make_context(*evidence: Evidence, applicable=True) -> EvaluationContext:
    return EvaluationContext(
        subject=make_opportunity(),
        evidence=evidence,
        evaluation_time=datetime(2026, 9, 28, 12, tzinfo=timezone.utc),
        applicability={
            CriterionId.REQUIREMENT_FIT: (
                CriterionApplicability.APPLICABLE
                if applicable
                else CriterionApplicability.NOT_APPLICABLE
            )
        },
    )


def policy(*requirements: CapabilityRequirement) -> EvaluationPolicy:
    return EvaluationPolicy(
        policy_id="requirement-fit-v1",
        policy_version="1",
        required_criteria=(CriterionId.REQUIREMENT_FIT,),
        requirement_fit_requirements=requirements,
    )


def capability_evidence(
    evidence_id: str,
    capability_id: str,
    *,
    compatibility="SUPPORTED",
    quality=EvidenceQuality.PRESENT_AND_USABLE,
) -> Evidence:
    return Evidence(
        evidence_id=evidence_id,
        kind=EvidenceKind.FACT,
        value={
            "capability_id": capability_id,
            "compatibility": compatibility,
        },
        provenance="synthetic:test",
        observed_at=datetime(2026, 9, 28, 11, tzinfo=timezone.utc),
        quality=quality,
    )


def requirement(
    requirement_id: str,
    capability_id: str,
    *evidence_ids: str,
) -> CapabilityRequirement:
    return CapabilityRequirement(
        requirement_id=requirement_id,
        capability_id=capability_id,
        evidence_refs=evidence_ids,
    )


def test_exact_normalized_capability_match_returns_pass():
    context = make_context(
        capability_evidence("cap.react", "react"),
    )

    result = RequirementFitEvaluator().evaluate(
        make_opportunity(),
        policy(requirement("req-react", "react", "cap.react")),
        context,
    )

    assert result.outcome is CriterionOutcome.PASS
    assert result.evidence_refs == ("cap.react",)


def test_multiple_mandatory_requirements_must_all_be_satisfied():
    context = make_context(
        capability_evidence("cap.react", "react"),
        capability_evidence("cap.typescript", "typescript"),
    )

    result = RequirementFitEvaluator().evaluate(
        make_opportunity(),
        policy(
            requirement("req-react", "react", "cap.react"),
            requirement("req-typescript", "typescript", "cap.typescript"),
        ),
        context,
    )

    assert result.outcome is CriterionOutcome.PASS


def test_missing_mandatory_capability_evidence_returns_insufficient_data():
    context = make_context()

    result = RequirementFitEvaluator().evaluate(
        make_opportunity(),
        policy(requirement("req-react", "react", "cap.react")),
        context,
    )

    assert result.outcome is CriterionOutcome.INSUFFICIENT_DATA
    assert result.missing_evidence == ("cap.react",)


def test_ambiguous_capability_evidence_returns_insufficient_data():
    context = make_context(
        capability_evidence(
            "cap.react",
            "react",
            quality=EvidenceQuality.PRESENT_BUT_AMBIGUOUS,
        ),
    )

    result = RequirementFitEvaluator().evaluate(
        make_opportunity(),
        policy(requirement("req-react", "react", "cap.react")),
        context,
    )

    assert result.outcome is CriterionOutcome.INSUFFICIENT_DATA
    assert result.evidence_refs == ("cap.react",)


def test_stale_capability_evidence_returns_insufficient_data():
    context = make_context(
        capability_evidence(
            "cap.react",
            "react",
            quality=EvidenceQuality.PRESENT_BUT_STALE,
        ),
    )

    result = RequirementFitEvaluator().evaluate(
        make_opportunity(),
        policy(requirement("req-react", "react", "cap.react")),
        context,
    )

    assert result.outcome is CriterionOutcome.INSUFFICIENT_DATA


def test_low_quality_capability_evidence_returns_insufficient_data():
    context = make_context(
        capability_evidence(
            "cap.react",
            "react",
            quality=EvidenceQuality.PRESENT_BUT_LOW_QUALITY,
        ),
    )

    result = RequirementFitEvaluator().evaluate(
        make_opportunity(),
        policy(requirement("req-react", "react", "cap.react")),
        context,
    )

    assert result.outcome is CriterionOutcome.INSUFFICIENT_DATA


def test_explicit_incompatibility_is_the_fail_path():
    context = make_context(
        capability_evidence(
            "cap.react",
            "react",
            compatibility="INCOMPATIBLE",
        ),
    )

    result = RequirementFitEvaluator().evaluate(
        make_opportunity(),
        policy(requirement("req-react", "react", "cap.react")),
        context,
    )

    assert result.outcome is CriterionOutcome.FAIL
    assert result.evidence_refs == ("cap.react",)


def test_contradictory_usable_capability_evidence_returns_insufficient_data():
    context = make_context(
        capability_evidence("cap-a", "react", compatibility="SUPPORTED"),
        capability_evidence("cap-b", "react", compatibility="INCOMPATIBLE"),
    )

    result = RequirementFitEvaluator().evaluate(
        make_opportunity(),
        policy(requirement("req-react", "react", "cap-a", "cap-b")),
        context,
    )

    assert result.outcome is CriterionOutcome.INSUFFICIENT_DATA
    assert result.evidence_refs == ("cap-a", "cap-b")


def test_not_applicable_requires_explicit_context():
    context = make_context(applicable=False)

    result = RequirementFitEvaluator().evaluate(
        make_opportunity(),
        policy(requirement("req-react", "react", "cap.react")),
        context,
    )

    assert result.outcome is CriterionOutcome.NOT_APPLICABLE


def test_missing_capability_is_not_inferred_from_opportunity_fields():
    opportunity = Opportunity(
        source_platform="example_marketplace",
        source_opportunity_id="synthetic-requirement-fit-002",
        title="React expert needed",
        description="React, TypeScript and strong frontend experience required.",
        required_capabilities=frozenset({"react"}),
    )
    context = EvaluationContext(
        subject=opportunity,
        evidence=(),
        evaluation_time=datetime(2026, 9, 28, 12, tzinfo=timezone.utc),
    )

    result = RequirementFitEvaluator().evaluate(
        opportunity,
        policy(requirement("req-typescript", "typescript", "cap.typescript")),
        context,
    )

    assert result.outcome is CriterionOutcome.INSUFFICIENT_DATA


def test_no_partial_match_or_numeric_score_is_produced():
    context = make_context(
        capability_evidence("cap-react", "react"),
    )

    result = RequirementFitEvaluator().evaluate(
        make_opportunity(),
        policy(
            requirement("req-react", "react", "cap-react"),
            requirement("req-typescript", "typescript", "cap-typescript"),
        ),
        context,
    )

    assert result.outcome is CriterionOutcome.INSUFFICIENT_DATA
    assert not hasattr(result, "score")
    assert not hasattr(result, "percentage")


def test_policy_identity_is_preserved():
    context = make_context(
        capability_evidence("cap-react", "react"),
    )

    result = RequirementFitEvaluator().evaluate(
        make_opportunity(),
        policy(requirement("req-react", "react", "cap-react")),
        context,
    )

    assert result.policy_id == "requirement-fit-v1"
    assert result.policy_version == "1"


def test_context_for_different_opportunity_is_rejected():
    context = make_context(
        capability_evidence("cap-react", "react"),
    )
    other = Opportunity(
        source_platform="example_marketplace",
        source_opportunity_id="different",
        title="Different opportunity",
        description="Different description.",
    )

    try:
        RequirementFitEvaluator().evaluate(
            other,
            policy(requirement("req-react", "react", "cap-react")),
            context,
        )
    except ValueError as exc:
        assert "subject" in str(exc)
    else:
        raise AssertionError("mismatched evaluation subject must be rejected")


def test_requirement_rejects_duplicate_evidence_references():
    try:
        CapabilityRequirement(
            requirement_id="invalid",
            capability_id="react",
            evidence_refs=("cap.react", "cap.react"),
        )
    except ValueError as exc:
        assert "duplicates" in str(exc)
    else:
        raise AssertionError("duplicate evidence references must be rejected")


def test_unsupported_capability_assertion_returns_insufficient_data():
    context = make_context(
        capability_evidence(
            "cap-react",
            "react",
            compatibility="UNKNOWN",
        ),
    )

    result = RequirementFitEvaluator().evaluate(
        make_opportunity(),
        policy(requirement("req-react", "react", "cap-react")),
        context,
    )

    assert result.outcome is CriterionOutcome.INSUFFICIENT_DATA


def test_policy_rejects_duplicate_requirement_ids():
    try:
        policy(
            requirement("duplicate", "react", "cap-react"),
            requirement("duplicate", "typescript", "cap-typescript"),
        )
    except ValueError as exc:
        assert "duplicate ids" in str(exc)
    else:
        raise AssertionError("duplicate requirement ids must be rejected")


def test_capability_identity_mismatch_is_not_treated_as_support():
    context = make_context(
        capability_evidence("cap-react", "vue"),
    )

    result = RequirementFitEvaluator().evaluate(
        make_opportunity(),
        policy(requirement("req-react", "react", "cap-react")),
        context,
    )

    assert result.outcome is CriterionOutcome.INSUFFICIENT_DATA


def test_supported_evidence_alone_cannot_cancel_incompatible_evidence():
    context = make_context(
        capability_evidence("cap-supported", "react", compatibility="SUPPORTED"),
        capability_evidence("cap-incompatible", "react", compatibility="INCOMPATIBLE"),
    )

    result = RequirementFitEvaluator().evaluate(
        make_opportunity(),
        policy(requirement(
            "req-react",
            "react",
            "cap-supported",
            "cap-incompatible",
        )),
        context,
    )

    assert result.outcome is CriterionOutcome.INSUFFICIENT_DATA
