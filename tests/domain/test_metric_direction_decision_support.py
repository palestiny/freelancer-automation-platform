from datetime import datetime

from app.domain.metric_direction_policy import (
    MetricDirectionInterpretation,
    MetricDirectionPolicy,
    MetricPolarity,
)
from app.domain.performance_evidence_decision_support import DescriptiveDirection
from app.domain.performance_history import PerformanceWindow
from app.domain.performance_trend import PerformanceTrend
from app.domain.statistical_evidence_composition import (
    StatisticalEvidenceComposition,
    StatisticalEvidenceEligibilityReason,
    StatisticalEvidenceInterpretation,
)
from app.domain.performance_reliability import SourceReliabilityAssessment, SourceReliabilityReason
from app.domain.performance_evidence_decision_support import compose_performance_evidence


def _trend(change: float) -> PerformanceTrend:
    return PerformanceTrend(
        metric_name="profit",
        unit="EGP",
        current_window=PerformanceWindow(datetime(2026, 2, 1), datetime(2026, 2, 8)),
        baseline_window=PerformanceWindow(datetime(2026, 1, 25), datetime(2026, 2, 1)),
        current_average=100 + change,
        baseline_average=100,
        absolute_change=change,
        relative_change=change / 100,
        current_observation_ids=("c1",),
        baseline_observation_ids=("b1",),
        current_evidence_quality=80,
        baseline_evidence_quality=80,
    )


def _reliability():
    return SourceReliabilityAssessment(
        eligible=True,
        reason=SourceReliabilityReason.ELIGIBLE,
        minimum_reliability=80,
    )


def _stat():
    return StatisticalEvidenceComposition(
        business_id="b1",
        metric_name="profit",
        unit="EGP",
        method="welch_two_sample_t_test",
        observation_ids=("b1", "b2", "c1", "c2"),
        eligible=True,
        reason=StatisticalEvidenceEligibilityReason.ELIGIBLE,
        interpretation=StatisticalEvidenceInterpretation.STATISTICALLY_DETECTED_DIFFERENCE,
        alpha=0.05,
        first_window=PerformanceWindow(datetime(2026, 1, 25), datetime(2026, 2, 1)),
        second_window=PerformanceWindow(datetime(2026, 2, 1), datetime(2026, 2, 8)),
        current_evidence_quality=80,
        baseline_evidence_quality=80,
        current_source_reliability=_reliability(),
        baseline_source_reliability=_reliability(),
        mean_difference=10,
    )


def test_higher_is_favorable_maps_increase_to_favorable():
    result = compose_performance_evidence(
        trend=_trend(10),
        statistical_evidence=_stat(),
        business_id="b1",
        metric_direction_policy=MetricDirectionPolicy(MetricPolarity.HIGHER_IS_FAVORABLE),
    )
    assert result.metric_direction_interpretation is MetricDirectionInterpretation.FAVORABLE


def test_lower_is_favorable_maps_increase_to_unfavorable():
    result = compose_performance_evidence(
        trend=_trend(10),
        statistical_evidence=_stat(),
        business_id="b1",
        metric_direction_policy=MetricDirectionPolicy(MetricPolarity.LOWER_IS_FAVORABLE),
    )
    assert result.metric_direction_interpretation is MetricDirectionInterpretation.UNFAVORABLE


def test_missing_policy_does_not_infer_polarity():
    result = compose_performance_evidence(
        trend=_trend(10),
        statistical_evidence=_stat(),
        business_id="b1",
        metric_direction_policy=None,
    )
    assert result.metric_direction_interpretation is MetricDirectionInterpretation.NOT_INTERPRETABLE


def test_neutral_metric_is_neutral():
    result = compose_performance_evidence(
        trend=_trend(10),
        statistical_evidence=_stat(),
        business_id="b1",
        metric_direction_policy=MetricDirectionPolicy(MetricPolarity.DIRECTION_NEUTRAL),
    )
    assert result.metric_direction_interpretation is MetricDirectionInterpretation.NEUTRAL
