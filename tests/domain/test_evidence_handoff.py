from app.domain.performance_history import PerformanceWindow
from datetime import datetime
from app.domain.performance_evidence_decision_support import (
    CombinedEvidencePosture,
    DescriptiveDirection,
    InferentialStatus,
    PerformanceEvidenceDecisionSupport,
)
from app.domain.evidence_handoff import (
    EvidenceHandoffStatus,
    create_evidence_handoff,
)


def _support(posture=CombinedEvidencePosture.DESCRIPTIVE_CHANGE_WITH_STATISTICAL_DETECTION,
             inferential=InferentialStatus.STATISTICAL_DIFFERENCE_DETECTED):
    return PerformanceEvidenceDecisionSupport(
        business_id="b1",
        metric_name="profit",
        unit="EGP",
        descriptive_direction=DescriptiveDirection.IMPROVING,
        inferential_status=inferential,
        posture=posture,
        statistical_observation_ids=("a", "b"),
        statistical_method="welch_two_sample_t_test",
        statistical_first_window=PerformanceWindow(datetime(2026, 1, 25), datetime(2026, 2, 1)),
        statistical_second_window=PerformanceWindow(datetime(2026, 2, 1), datetime(2026, 2, 8)),
        statistical_difference_direction=(DescriptiveDirection.UNAVAILABLE if inferential is InferentialStatus.UNAVAILABLE else DescriptiveDirection.IMPROVING),
        current_observation_ids=("c1",),
        baseline_observation_ids=("b1",),
    )


def test_ready_handoff_requires_named_consumer():
    result = create_evidence_handoff(
        evidence=_support(),
        consumer_id="portfolio-review",
    )
    assert result.status is EvidenceHandoffStatus.READY
    assert result.consumer_id == "portfolio-review"


def test_unavailable_inferential_evidence_is_not_ready():
    result = create_evidence_handoff(
        evidence=_support(
            posture=CombinedEvidencePosture.INFERENTIAL_EVIDENCE_UNAVAILABLE,
            inferential=InferentialStatus.UNAVAILABLE,
        ),
        consumer_id="portfolio-review",
    )
    assert result.status is EvidenceHandoffStatus.NOT_READY


def test_invalid_context_is_not_ready():
    result = create_evidence_handoff(
        evidence=_support(posture=CombinedEvidencePosture.CONTEXT_INVALID),
        consumer_id="portfolio-review",
    )
    assert result.status is EvidenceHandoffStatus.NOT_READY


def test_empty_consumer_is_rejected():
    try:
        create_evidence_handoff(evidence=_support(), consumer_id=" ")
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError")
