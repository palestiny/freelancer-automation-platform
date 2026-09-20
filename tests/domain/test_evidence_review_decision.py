import pytest

from app.domain.evidence_review_handoff import ReviewTarget, create_evidence_review_handoff
from app.domain.evidence_review_decision import (
    EvidenceReviewDecision,
    ReviewDecisionOutcome,
    create_evidence_review_decision,
)
from app.domain.performance_evidence_decision_support import (
    CombinedEvidencePosture,
    DescriptiveDirection,
    InferentialStatus,
    PerformanceEvidenceDecisionSupport,
)


def _handoff():
    evidence = PerformanceEvidenceDecisionSupport(
        business_id="b1",
        metric_name="profit",
        unit="EGP",
        descriptive_direction=DescriptiveDirection.IMPROVING,
        inferential_status=InferentialStatus.STATISTICAL_DIFFERENCE_DETECTED,
        posture=CombinedEvidencePosture.DESCRIPTIVE_CHANGE_WITH_STATISTICAL_DETECTION,
        statistical_observation_ids=("a", "b", "c"),
        current_observation_ids=("c",),
        baseline_observation_ids=("a", "b"),
    )
    return create_evidence_review_handoff(
        evidence=evidence,
        target=ReviewTarget.POLICY_REVIEW,
        reason="Review operating policy.",
    )


def test_review_decision_preserves_handoff_lineage_and_target():
    decision = create_evidence_review_decision(
        handoff=_handoff(),
        reviewer_id="reviewer-1",
        outcome=ReviewDecisionOutcome.ACCEPT,
        rationale="Evidence is sufficient for explicit policy review.",
    )
    assert decision.business_id == "b1"
    assert decision.observation_ids == ("a", "b", "c")
    assert decision.target is ReviewTarget.POLICY_REVIEW
    assert decision.outcome is ReviewDecisionOutcome.ACCEPT


def test_accept_is_not_authorization():
    decision = create_evidence_review_decision(
        handoff=_handoff(),
        reviewer_id="reviewer-1",
        outcome=ReviewDecisionOutcome.ACCEPT,
        rationale="Reviewed.",
    )
    assert decision.authorized is False


@pytest.mark.parametrize("value", ["", " "])
def test_reviewer_id_and_rationale_are_required(value):
    with pytest.raises(ValueError):
        create_evidence_review_decision(
            handoff=_handoff(),
            reviewer_id=value,
            outcome=ReviewDecisionOutcome.ACCEPT,
            rationale="Reviewed.",
        )
    with pytest.raises(ValueError):
        create_evidence_review_decision(
            handoff=_handoff(),
            reviewer_id="reviewer-1",
            outcome=ReviewDecisionOutcome.ACCEPT,
            rationale=value,
        )


def test_invalid_outcome_type_is_rejected():
    with pytest.raises(TypeError):
        create_evidence_review_decision(
            handoff=_handoff(),
            reviewer_id="reviewer-1",
            outcome="accept",
            rationale="Reviewed.",
        )
