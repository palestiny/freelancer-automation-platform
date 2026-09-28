from datetime import datetime, timezone

import pytest

from app.domain.evaluation_context import (
    CriterionApplicability,
    EvaluationContext,
    Evidence,
    EvidenceKind,
    EvidenceQuality,
)
from app.domain.opportunity import Opportunity
from app.domain.opportunity_intelligence import CriterionId


def make_opportunity() -> Opportunity:
    return Opportunity(
        source_platform="example_marketplace",
        source_opportunity_id="synthetic-001",
        title="Build a React dashboard",
        description="Create a responsive dashboard.",
    )


def make_evidence(**overrides) -> Evidence:
    values = {
        "evidence_id": "evidence-001",
        "kind": EvidenceKind.FACT,
        "value": "React",
        "provenance": "profile:declared-capabilities",
        "observed_at": datetime(2026, 9, 28, 12, 0, tzinfo=timezone.utc),
        "quality": EvidenceQuality.PRESENT_AND_USABLE,
    }
    values.update(overrides)
    return Evidence(**values)


def test_evidence_is_immutable_and_preserves_required_provenance():
    evidence = make_evidence()

    assert evidence.evidence_id == "evidence-001"
    assert evidence.kind is EvidenceKind.FACT
    assert evidence.provenance == "profile:declared-capabilities"
    assert evidence.quality is EvidenceQuality.PRESENT_AND_USABLE

    with pytest.raises((AttributeError, TypeError)):
        evidence.value = "Vue"


def test_evidence_distinguishes_epistemic_kind_from_quality():
    estimate = make_evidence(
        evidence_id="effort-001",
        kind=EvidenceKind.ESTIMATE,
        value=12,
        quality=EvidenceQuality.PRESENT_BUT_AMBIGUOUS,
    )

    assert estimate.kind is EvidenceKind.ESTIMATE
    assert estimate.quality is EvidenceQuality.PRESENT_BUT_AMBIGUOUS


def test_derived_evidence_requires_lineage():
    derived = make_evidence(
        evidence_id="derived-001",
        kind=EvidenceKind.FACT,
        value="requirement-fit-input",
        derivation_refs=("evidence-001",),
    )

    assert derived.derivation_refs == ("evidence-001",)


def test_evidence_rejects_duplicate_lineage_references():
    with pytest.raises(ValueError, match="derivation_refs"):
        make_evidence(
            derivation_refs=("evidence-001", "evidence-001"),
        )


def test_evaluation_context_is_immutable_snapshot():
    context = EvaluationContext(
        subject=make_opportunity(),
        evidence=(make_evidence(),),
        evaluation_time=datetime(2026, 9, 28, 12, 30, tzinfo=timezone.utc),
        applicability={
            CriterionId.ELIGIBILITY: CriterionApplicability.APPLICABLE,
            CriterionId.REQUIREMENT_FIT: CriterionApplicability.APPLICABLE,
        },
    )

    assert context.subject.source_opportunity_id == "synthetic-001"
    assert context.evidence == (make_evidence(),)
    assert (
        context.applicability[CriterionId.REQUIREMENT_FIT]
        is CriterionApplicability.APPLICABLE
    )

    with pytest.raises((AttributeError, TypeError)):
        context.evaluation_time = datetime.now(timezone.utc)


def test_evaluation_context_rejects_duplicate_evidence_identity():
    first = make_evidence(evidence_id="same-id")
    second = make_evidence(
        evidence_id="same-id",
        kind=EvidenceKind.OBSERVATION,
        value="another observation",
    )

    with pytest.raises(ValueError, match="unique"):
        EvaluationContext(
            subject=make_opportunity(),
            evidence=(first, second),
            evaluation_time=datetime(2026, 9, 28, 12, 30, tzinfo=timezone.utc),
        )


def test_context_can_explicitly_mark_criterion_not_applicable():
    context = EvaluationContext(
        subject=make_opportunity(),
        evidence=(),
        evaluation_time=datetime(2026, 9, 28, 12, 30, tzinfo=timezone.utc),
        applicability={
            CriterionId.ECONOMIC_FIT: CriterionApplicability.NOT_APPLICABLE,
        },
    )

    assert (
        context.applicability[CriterionId.ECONOMIC_FIT]
        is CriterionApplicability.NOT_APPLICABLE
    )


def test_context_does_not_treat_missing_applicability_as_not_applicable():
    context = EvaluationContext(
        subject=make_opportunity(),
        evidence=(),
        evaluation_time=datetime(2026, 9, 28, 12, 30, tzinfo=timezone.utc),
    )

    assert CriterionId.ECONOMIC_FIT not in context.applicability


def test_context_rejects_non_timezone_aware_evaluation_time():
    with pytest.raises(ValueError, match="timezone-aware"):
        EvaluationContext(
            subject=make_opportunity(),
            evidence=(),
            evaluation_time=datetime(2026, 9, 28, 12, 30),
        )


def test_evidence_rejects_non_timezone_aware_observation_time():
    with pytest.raises(ValueError, match="timezone-aware"):
        make_evidence(
            observed_at=datetime(2026, 9, 28, 12, 0),
        )


def test_missing_quality_is_explicit():
    missing = make_evidence(
        evidence_id="missing-001",
        value=None,
        provenance="marketplace:project-detail",
        quality=EvidenceQuality.MISSING,
        observed_at=None,
    )

    assert missing.quality is EvidenceQuality.MISSING
    assert missing.observed_at is None
