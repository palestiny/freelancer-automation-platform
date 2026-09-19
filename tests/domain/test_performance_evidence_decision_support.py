from datetime import datetime, timezone

from app.domain.performance_history import PerformanceWindow
from app.domain.performance_trend import PerformanceTrend
from app.domain.performance_reliability import SourceReliabilityAssessment, SourceReliabilityReason
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
        mean_difference=10.0,
        first_window=PerformanceWindow(datetime(2026, 1, 25), datetime(2026, 2, 1)),
        second_window=PerformanceWindow(datetime(2026, 2, 1), datetime(2026, 2, 8)),
        current_evidence_quality=80,
        baseline_evidence_quality=75,
        current_source_reliability=SourceReliabilityAssessment(eligible=True, reason=SourceReliabilityReason.ELIGIBLE, minimum_reliability=80),
        baseline_source_reliability=SourceReliabilityAssessment(eligible=True, reason=SourceReliabilityReason.ELIGIBLE, minimum_reliability=80),
    )


def test_statistical_detection_does_not_claim_directional_alignment():
    result = compose_performance_evidence(
        trend=_trend(10.0),
        statistical_evidence=_stat(
            interpretation=StatisticalEvidenceInterpretation.STATISTICALLY_DETECTED_DIFFERENCE
        ),
        business_id="b1",
    )
    assert result.descriptive_direction is DescriptiveDirection.IMPROVING
    assert result.inferential_status is InferentialStatus.STATISTICAL_DIFFERENCE_DETECTED
    assert result.posture is CombinedEvidencePosture.DESCRIPTIVE_CHANGE_WITH_STATISTICAL_DETECTION
    assert result.current_observation_ids == ("c1",)
    assert result.baseline_observation_ids == ("b1",)
    assert result.statistical_observation_ids == ("b1", "b2", "c1", "c2")


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
    assert result.statistical_difference_direction is DescriptiveDirection.IMPROVING


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


def test_zero_descriptive_change_is_not_called_aligned_with_statistical_detection():
    result = compose_performance_evidence(
        trend=_trend(0.0),
        statistical_evidence=_stat(
            interpretation=StatisticalEvidenceInterpretation.STATISTICALLY_DETECTED_DIFFERENCE
        ),
        business_id="b1",
    )
    assert result.descriptive_direction is DescriptiveDirection.NO_CHANGE
    assert result.posture is CombinedEvidencePosture.NO_DESCRIPTIVE_CHANGE


def test_result_rejects_duplicate_statistical_observation_ids():
    import pytest
    from app.domain.performance_evidence_decision_support import PerformanceEvidenceDecisionSupport

    with pytest.raises(ValueError):
        PerformanceEvidenceDecisionSupport(
            business_id="b1",
            metric_name="profit",
            unit="EGP",
            descriptive_direction=DescriptiveDirection.IMPROVING,
            inferential_status=InferentialStatus.UNAVAILABLE,
            posture=CombinedEvidencePosture.INFERENTIAL_EVIDENCE_UNAVAILABLE,
            statistical_observation_ids=("x", "x"),
            statistical_difference_direction=DescriptiveDirection.UNAVAILABLE,
            current_observation_ids=("c1",),
            baseline_observation_ids=("b1",),
        )


def test_result_rejects_alignment_posture_when_inferential_status_is_unavailable():
    import pytest
    from app.domain.performance_evidence_decision_support import PerformanceEvidenceDecisionSupport
    with pytest.raises(ValueError):
        PerformanceEvidenceDecisionSupport(
            business_id="b1", metric_name="profit", unit="EGP",
            descriptive_direction=DescriptiveDirection.IMPROVING,
            inferential_status=InferentialStatus.UNAVAILABLE,
            posture=CombinedEvidencePosture.DESCRIPTIVE_CHANGE_WITH_STATISTICAL_DETECTION,
            statistical_observation_ids=("x",), current_observation_ids=("c1",),
            baseline_observation_ids=("b1",),
        )


def test_result_rejects_statistical_detection_with_no_descriptive_change():
    import pytest
    from app.domain.performance_evidence_decision_support import PerformanceEvidenceDecisionSupport
    with pytest.raises(ValueError):
        PerformanceEvidenceDecisionSupport(
            business_id="b1", metric_name="profit", unit="EGP",
            descriptive_direction=DescriptiveDirection.NO_CHANGE,
            inferential_status=InferentialStatus.STATISTICAL_DIFFERENCE_DETECTED,
            posture=CombinedEvidencePosture.DESCRIPTIVE_CHANGE_WITH_STATISTICAL_DETECTION,
            statistical_observation_ids=("x",),
            statistical_difference_direction=DescriptiveDirection.IMPROVING,
            current_observation_ids=("c1",), baseline_observation_ids=("b1",),
        )
