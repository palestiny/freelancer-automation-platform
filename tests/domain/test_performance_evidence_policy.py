from app.domain.performance_history import PerformanceWindow
from datetime import datetime

from app.domain.performance_evidence_decision_support import (
    CombinedEvidencePosture,
    DescriptiveDirection,
    InferentialStatus,
    PerformanceEvidenceDecisionSupport,
)
from app.domain.performance_evidence_policy import (
    PerformanceEvidencePolicyState,
    assess_performance_evidence_policy,
)


def _support(posture, direction=DescriptiveDirection.INCREASED):
    return PerformanceEvidenceDecisionSupport(
        business_id="b1",
        metric_name="profit",
        unit="EGP",
        descriptive_direction=direction,
        inferential_status=(
            InferentialStatus.UNAVAILABLE
            if posture is CombinedEvidencePosture.INFERENTIAL_EVIDENCE_UNAVAILABLE
            else InferentialStatus.STATISTICAL_DIFFERENCE_DETECTED
        ),
        posture=posture,
        statistical_observation_ids=("s1", "s2"),
        statistical_method="welch_two_sample_t_test",
        statistical_first_window=PerformanceWindow(datetime(2026, 1, 25), datetime(2026, 2, 1)),
        statistical_second_window=PerformanceWindow(datetime(2026, 2, 1), datetime(2026, 2, 8)),
        statistical_difference_direction=DescriptiveDirection.IMPROVING,
        current_window_start=datetime(2026, 2, 1),
        current_window_end=datetime(2026, 2, 8),
        baseline_window_start=datetime(2026, 1, 25),
        baseline_window_end=datetime(2026, 2, 1),
        current_observation_ids=("c1",),
        baseline_observation_ids=("b1",),
    )


def test_aligned_improvement_supports_improvement():
    result = assess_performance_evidence_policy(
        support=_support(
            CombinedEvidencePosture.DESCRIPTIVE_CHANGE_WITH_STATISTICAL_DETECTION
        )
    )
    assert result.state is PerformanceEvidencePolicyState.SUPPORTS_IMPROVEMENT


def test_aligned_decline_supports_decline():
    result = assess_performance_evidence_policy(
        support=_support(
            CombinedEvidencePosture.DESCRIPTIVE_CHANGE_WITH_STATISTICAL_DETECTION,
            DescriptiveDirection.DECREASED,
        )
    )
    assert result.state is PerformanceEvidencePolicyState.SUPPORTS_DECLINE


def test_descriptive_only_change_is_not_presented_as_statistically_supported():
    result = assess_performance_evidence_policy(
        support=_support(
            CombinedEvidencePosture.DESCRIPTIVE_CHANGE_WITHOUT_STATISTICAL_DETECTION
        )
    )
    assert result.state is PerformanceEvidencePolicyState.DESCRIPTIVE_CHANGE_ONLY


def test_unavailable_inference_is_insufficient_evidence():
    result = assess_performance_evidence_policy(
        support=_support(CombinedEvidencePosture.INFERENTIAL_EVIDENCE_UNAVAILABLE)
    )
    assert result.state is PerformanceEvidencePolicyState.EVIDENCE_INSUFFICIENT


def test_context_invalid_remains_explicit():
    result = assess_performance_evidence_policy(
        support=_support(CombinedEvidencePosture.CONTEXT_INVALID)
    )
    assert result.state is PerformanceEvidencePolicyState.CONTEXT_INVALID
