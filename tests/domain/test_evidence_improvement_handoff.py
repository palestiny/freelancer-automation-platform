from datetime import datetime

from app.domain.performance_history import PerformanceWindow

from app.domain.performance_evidence_decision_support import (
    CombinedEvidencePosture,
    DescriptiveDirection,
    InferentialStatus,
    PerformanceEvidenceDecisionSupport,
)
from app.domain.evidence_improvement_handoff import (
    ImprovementHandoffStatus,
    create_improvement_handoff,
)


def _support(*, inferential=InferentialStatus.STATISTICAL_DIFFERENCE_DETECTED):
    return PerformanceEvidenceDecisionSupport(
        business_id="b1",
        metric_name="profit",
        unit="EGP",
        descriptive_direction=DescriptiveDirection.IMPROVING,
        inferential_status=inferential,
        posture=CombinedEvidencePosture.DESCRIPTIVE_CHANGE_WITH_STATISTICAL_DETECTION,
        statistical_observation_ids=("b1", "b2", "c1", "c2"),
        statistical_first_window=PerformanceWindow(datetime(2026, 1, 1), datetime(2026, 1, 8)),
        statistical_second_window=PerformanceWindow(datetime(2026, 2, 1), datetime(2026, 2, 8)),
        current_window_start=datetime(2026, 2, 1),
        current_window_end=datetime(2026, 2, 8),
        baseline_window_start=datetime(2026, 1, 1),
        baseline_window_end=datetime(2026, 1, 8),
        current_observation_ids=("c1", "c2"),
        baseline_observation_ids=("b1", "b2"),
    )


def test_explicit_request_creates_review_handoff():
    result = create_improvement_handoff(
        evidence=_support(),
        request_review=True,
        statement="Review the observed profit improvement.",
        requested_at=datetime(2026, 9, 20),
    )
    assert result.status is ImprovementHandoffStatus.READY_FOR_REVIEW
    assert result.observation_ids == ("b1", "b2", "c1", "c2")


def test_no_explicit_request_does_not_create_handoff():
    result = create_improvement_handoff(
        evidence=_support(),
        request_review=False,
        statement="Review later.",
        requested_at=datetime(2026, 9, 20),
    )
    assert result.status is ImprovementHandoffStatus.NOT_REQUESTED


def test_unavailable_inferential_evidence_blocks_handoff():
    result = create_improvement_handoff(
        evidence=_support(inferential=InferentialStatus.UNAVAILABLE),
        request_review=True,
        statement="Review this.",
        requested_at=datetime(2026, 9, 20),
    )
    assert result.status is ImprovementHandoffStatus.EVIDENCE_NOT_ELIGIBLE
