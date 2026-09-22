from app.domain.performance_history import PerformanceWindow
from datetime import datetime
from app.domain.performance_evidence_decision_support import (
    CombinedEvidencePosture,
    DescriptiveDirection,
    InferentialStatus,
    PerformanceEvidenceDecisionSupport,
)
from app.domain.evidence_consumer_handoff import (
    EvidenceReviewState,
    create_evidence_review_item,
)


def _support(*, posture=CombinedEvidencePosture.DESCRIPTIVE_CHANGE_WITH_STATISTICAL_DETECTION, inferential_status=InferentialStatus.STATISTICAL_DIFFERENCE_DETECTED):
    return PerformanceEvidenceDecisionSupport(
        business_id="b1",
        metric_name="profit",
        unit="EGP",
        descriptive_direction=DescriptiveDirection.IMPROVING,
        inferential_status=inferential_status,
        posture=posture,
        statistical_observation_ids=("b1", "b2", "c1", "c2"),
        statistical_method="welch_two_sample_t_test",
        statistical_first_window=PerformanceWindow(datetime(2026, 1, 25), datetime(2026, 2, 1)),
        statistical_second_window=PerformanceWindow(datetime(2026, 2, 1), datetime(2026, 2, 8)),
        statistical_difference_direction=(DescriptiveDirection.UNAVAILABLE if inferential_status is InferentialStatus.UNAVAILABLE else DescriptiveDirection.IMPROVING),
        current_observation_ids=("c1", "c2"),
        baseline_observation_ids=("b1", "b2"),
    )


def test_usable_evidence_is_ready_for_review():
    item = create_evidence_review_item(_support())
    assert item.state is EvidenceReviewState.READY_FOR_REVIEW
    assert item.observation_ids == ("b1", "b2", "c1", "c2")


def test_unavailable_inferential_evidence_is_explicitly_unavailable():
    item = create_evidence_review_item(
        _support(
            posture=CombinedEvidencePosture.INFERENTIAL_EVIDENCE_UNAVAILABLE,
            inferential_status=InferentialStatus.UNAVAILABLE,
        )
    )
    assert item.state is EvidenceReviewState.EVIDENCE_UNAVAILABLE


def test_invalid_context_is_not_reviewable():
    item = create_evidence_review_item(
        _support(posture=CombinedEvidencePosture.CONTEXT_INVALID)
    )
    assert item.state is EvidenceReviewState.CONTEXT_INVALID
