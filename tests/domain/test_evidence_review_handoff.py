from app.domain.performance_history import PerformanceWindow
from datetime import datetime
import pytest

from app.domain.performance_evidence_decision_support import (
    CombinedEvidencePosture,
    DescriptiveDirection,
    InferentialStatus,
    PerformanceEvidenceDecisionSupport,
)
from app.domain.evidence_review_handoff import (
    EvidenceReviewHandoff,
    ReviewTarget,
    create_evidence_review_handoff,
)


def _support() -> PerformanceEvidenceDecisionSupport:
    return PerformanceEvidenceDecisionSupport(
        business_id="b1",
        metric_name="profit",
        unit="EGP",
        descriptive_direction=DescriptiveDirection.IMPROVING,
        inferential_status=InferentialStatus.STATISTICAL_DIFFERENCE_DETECTED,
        posture=CombinedEvidencePosture.DESCRIPTIVE_CHANGE_WITH_STATISTICAL_DETECTION,
        statistical_observation_ids=("a", "b", "c"),
        statistical_method="welch_two_sample_t_test",
        statistical_first_window=PerformanceWindow(datetime(2026, 1, 25), datetime(2026, 2, 1)),
        statistical_second_window=PerformanceWindow(datetime(2026, 2, 1), datetime(2026, 2, 8)),
        statistical_difference_direction=DescriptiveDirection.IMPROVING,
        current_observation_ids=("c",),
        baseline_observation_ids=("a", "b"),
    )


def test_handoff_preserves_composed_evidence_and_lineage():
    handoff = create_evidence_review_handoff(
        evidence=_support(),
        target=ReviewTarget.POLICY_REVIEW,
        reason="Review whether current operating policy should be revisited.",
    )

    assert handoff.business_id == "b1"
    assert handoff.metric_name == "profit"
    assert handoff.unit == "EGP"
    assert handoff.descriptive_direction is DescriptiveDirection.IMPROVING
    assert handoff.inferential_status is InferentialStatus.STATISTICAL_DIFFERENCE_DETECTED
    assert handoff.posture is CombinedEvidencePosture.DESCRIPTIVE_CHANGE_WITH_STATISTICAL_DETECTION
    assert handoff.observation_ids == ("a", "b", "c")


def test_handoff_does_not_claim_authorization():
    handoff = create_evidence_review_handoff(
        evidence=_support(),
        target=ReviewTarget.HUMAN_REVIEW,
        reason="Independent review requested.",
    )

    assert handoff.target is ReviewTarget.HUMAN_REVIEW
    assert handoff.authorized is False


@pytest.mark.parametrize("reason", ["", "   "])
def test_empty_reason_is_rejected(reason):
    with pytest.raises(ValueError):
        create_evidence_review_handoff(
            evidence=_support(),
            target=ReviewTarget.HUMAN_REVIEW,
            reason=reason,
        )
