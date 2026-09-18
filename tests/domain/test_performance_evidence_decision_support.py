from datetime import datetime, timezone

from app.domain.performance_history import PerformanceWindow
from app.domain.performance_trend import PerformanceTrend
from app.domain.statistical_evidence_composition import (
    StatisticalEvidenceComposition,
    StatisticalEvidenceEligibilityReason,
    StatisticalEvidenceInterpretation,
)
from app.domain.performance_evidence_decision_support import (
    CombinedEvidencePosture,
    DescriptiveDirection,
    InferentialStatus,
    compose_performance_evidence,
)


def _trend(change: float) -> PerformanceTrend:
    return PerformanceTrend(
        metric_name="profit",
        unit="EGP",
        current_window=PerformanceWindow(datetime(2026, 2, 1), datetime(2026, 2, 8)),
        baseline_window=PerformanceWindow(datetime(2026, 1, 25), datetime(2026, 2, 1)),
        current_average=100.0 + change,
        baseline_average=100.0,
        absolute_change=change,
        relative_change=change / 100.0,
        current_observation_ids=("c1",),
        baseline_observation_ids=("b1",),
        current_evidence_quality=80,
        baseline_evidence_quality=80,
    )


def _stat(*, interpretation, eligible=True):
    return StatisticalEvidenceComposition(
        business_id="b1",
        metric_name="profit",
        unit="EGP",
        method="welch_two_sample_t_test",
        observation_ids=("b1", "b2", "c1", "c2"),
        eligible=eligible,
        reason=(
            StatisticalEvidenceEligibilityReason.ELIGIBLE
            if eligible else StatisticalEvidenceEligibilityReason.INSUFFICIENT_EVIDENCE_QUALITY
        ),
        interpretation=interpretation,
        alpha=0.05,
    )


def test_aligned_improvement_is_explicit():
    result = compose_performance_evidence(
        trend=_trend(10.0),
        statistical_evidence=_stat(
            interpretation=StatisticalEvidenceInterpretation.STATISTICALLY_DETECTED_DIFFERENCE
        ),
        business_id="b1",
    )
    assert result.descriptive_direction is DescriptiveDirection.IMPROVING
    assert result.inferential_status is InferentialStatus.STATISTICAL_DIFFERENCE_DETECTED
    assert result.posture is CombinedEvidencePosture.DESCRIPTIVE_AND_STATISTICAL_ALIGNMENT


def test_descriptive_change_without_statistical_detection_is_not_suppressed():
    result = compose_performance_evidence(
        trend=_trend(-10.0),
        statistical_evidence=_stat(
            interpretation=StatisticalEvidenceInterpretation.NO_STATISTICALLY_DETECTED_DIFFERENCE
        ),
        business_id="b1",
    )
    assert result.descriptive_direction is DescriptiveDirection.DECLINING
    assert result.posture is CombinedEvidencePosture.DESCRIPTIVE_CHANGE_WITHOUT_STATISTICAL_DETECTION


def test_ineligible_statistical_evidence_remains_unavailable():
    result = compose_performance_evidence(
        trend=_trend(10.0),
        statistical_evidence=_stat(
            interpretation=StatisticalEvidenceInterpretation.STATISTICALLY_DETECTED_DIFFERENCE,
            eligible=False,
        ),
        business_id="b1",
    )
    assert result.inferential_status is InferentialStatus.UNAVAILABLE
    assert result.posture is CombinedEvidencePosture.INFERENTIAL_EVIDENCE_UNAVAILABLE


def test_context_mismatch_is_explicit():
    result = compose_performance_evidence(
        trend=_trend(10.0),
        statistical_evidence=_stat(
            interpretation=StatisticalEvidenceInterpretation.STATISTICALLY_DETECTED_DIFFERENCE
        ),
        business_id="other",
    )
    assert result.posture is CombinedEvidencePosture.CONTEXT_INVALID
