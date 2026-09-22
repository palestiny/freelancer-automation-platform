from app.domain.performance_history import PerformanceWindow
from datetime import datetime
from app.domain.performance_evidence_decision_support import (
    CombinedEvidencePosture,
    DescriptiveDirection,
    InferentialStatus,
    PerformanceEvidenceDecisionSupport,
)
from app.domain.statistical_evidence_learning_handoff import (
    LearningHandoffTarget,
    create_statistical_evidence_learning_handoff,
)


def _evidence():
    return PerformanceEvidenceDecisionSupport(
        business_id="b1",
        metric_name="profit",
        unit="EGP",
        descriptive_direction=DescriptiveDirection.DECLINING,
        inferential_status=InferentialStatus.STATISTICAL_DIFFERENCE_DETECTED,
        posture=CombinedEvidencePosture.STATISTICAL_AND_DESCRIPTIVE_DIRECTION_CONFLICT,
        statistical_observation_ids=("s1", "s2"),
        statistical_method="welch_two_sample_t_test",
        statistical_first_window=PerformanceWindow(datetime(2026, 1, 25), datetime(2026, 2, 1)),
        statistical_second_window=PerformanceWindow(datetime(2026, 2, 1), datetime(2026, 2, 8)),
        statistical_difference_direction=DescriptiveDirection.DECREASED,
        current_observation_ids=("c1", "c2"),
        baseline_observation_ids=("b1", "b2"),
    )


def test_handoff_preserves_evidence_and_target():
    result = create_statistical_evidence_learning_handoff(
        evidence=_evidence(),
        statement="Review the observed performance change.",
        target=LearningHandoffTarget.POLICY_REVIEW,
    )
    assert result.business_id == "b1"
    assert result.metric_name == "profit"
    assert result.unit == "EGP"
    assert result.target is LearningHandoffTarget.POLICY_REVIEW
    assert result.statistical_observation_ids == ("s1", "s2")
    assert result.current_observation_ids == ("c1", "c2")
    assert result.baseline_observation_ids == ("b1", "b2")


def test_handoff_does_not_require_statistical_availability():
    evidence = _evidence()
    evidence = PerformanceEvidenceDecisionSupport(
        **{**evidence.__dict__, "inferential_status": InferentialStatus.UNAVAILABLE, "posture": CombinedEvidencePosture.INFERENTIAL_EVIDENCE_UNAVAILABLE, "statistical_difference_direction": DescriptiveDirection.UNAVAILABLE}
    )
    result = create_statistical_evidence_learning_handoff(
        evidence=evidence,
        statement="Review descriptive evidence.",
        target=LearningHandoffTarget.EXPERIMENT,
    )
    assert result.target is LearningHandoffTarget.EXPERIMENT
    assert result.inferential_status is InferentialStatus.UNAVAILABLE
