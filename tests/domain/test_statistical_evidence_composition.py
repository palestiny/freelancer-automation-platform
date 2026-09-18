from datetime import datetime, timezone

from app.domain.business_performance import PerformanceSourceType
from app.domain.performance_reliability import (
    SourceReliabilityAssessment,
    SourceReliabilityReason,
)
from app.domain.performance_history import PerformanceWindow
from app.domain.statistical_mean_comparison import (
    MeanComparisonResult,
    MeanComparisonStatus,
)
from app.domain.statistical_evidence_composition import (
    StatisticalEvidenceEligibilityReason,
    StatisticalEvidenceInterpretation,
    compose_statistical_evidence,
)


def _window():
    return PerformanceWindow(
        start=datetime(2026, 1, 1, tzinfo=timezone.utc),
        end=datetime(2026, 1, 8, tzinfo=timezone.utc),
    )


def _result(*, status=MeanComparisonStatus.APPLICABLE, rejects_null=False):
    return MeanComparisonResult(
        business_id="b1",
        metric_name="profit",
        unit="EGP",
        first_window=_window(),
        second_window=PerformanceWindow(
            start=datetime(2026, 1, 8, tzinfo=timezone.utc),
            end=datetime(2026, 1, 15, tzinfo=timezone.utc),
        ),
        first_observation_ids=("a", "b"),
        second_observation_ids=("c", "d"),
        sample_size_first=2,
        sample_size_second=2,
        mean_first=100.0,
        mean_second=90.0,
        mean_difference=10.0,
        t_statistic=2.5,
        degrees_of_freedom=2.0,
        p_value=0.05,
        alpha=0.05,
        method="welch_two_sample_t_test",
        rejects_null=rejects_null if status is MeanComparisonStatus.APPLICABLE else None,
        status=status,
    )


def _eligible():
    return SourceReliabilityAssessment(
        eligible=True,
        reason=SourceReliabilityReason.ELIGIBLE,
        minimum_reliability=80,
    )


def test_detected_difference_is_eligible_when_evidence_gates_pass():
    result = compose_statistical_evidence(
        comparison=_result(rejects_null=True),
        current_evidence_quality=80,
        baseline_evidence_quality=75,
        current_source_reliability=_eligible(),
        baseline_source_reliability=_eligible(),
        minimum_evidence_quality=60,
    )

    assert result.eligible is True
    assert result.interpretation is StatisticalEvidenceInterpretation.STATISTICALLY_DETECTED_DIFFERENCE
    assert result.reason is StatisticalEvidenceEligibilityReason.ELIGIBLE
    assert result.observation_ids == ("a", "b", "c", "d")


def test_non_significant_result_remains_eligible_evidence():
    result = compose_statistical_evidence(
        comparison=_result(rejects_null=False),
        current_evidence_quality=80,
        baseline_evidence_quality=75,
        current_source_reliability=_eligible(),
        baseline_source_reliability=_eligible(),
        minimum_evidence_quality=60,
    )

    assert result.eligible is True
    assert result.interpretation is StatisticalEvidenceInterpretation.NO_STATISTICALLY_DETECTED_DIFFERENCE


def test_inapplicable_statistical_result_is_not_eligible():
    result = compose_statistical_evidence(
        comparison=_result(status=MeanComparisonStatus.INSUFFICIENT_OBSERVATIONS),
        current_evidence_quality=80,
        baseline_evidence_quality=75,
        current_source_reliability=_eligible(),
        baseline_source_reliability=_eligible(),
        minimum_evidence_quality=60,
    )

    assert result.eligible is False
    assert result.reason is StatisticalEvidenceEligibilityReason.STATISTICAL_RESULT_NOT_APPLICABLE
    assert result.interpretation is StatisticalEvidenceInterpretation.STATISTICAL_RESULT_NOT_APPLICABLE


def test_low_evidence_quality_blocks_statistical_evidence():
    result = compose_statistical_evidence(
        comparison=_result(rejects_null=True),
        current_evidence_quality=59,
        baseline_evidence_quality=80,
        current_source_reliability=_eligible(),
        baseline_source_reliability=_eligible(),
        minimum_evidence_quality=60,
    )

    assert result.eligible is False
    assert result.reason is StatisticalEvidenceEligibilityReason.INSUFFICIENT_EVIDENCE_QUALITY


def test_low_source_reliability_blocks_statistical_evidence():
    ineligible = SourceReliabilityAssessment(
        eligible=False,
        reason=SourceReliabilityReason.INSUFFICIENT_RELIABILITY,
        minimum_reliability=40,
    )
    result = compose_statistical_evidence(
        comparison=_result(rejects_null=True),
        current_evidence_quality=80,
        baseline_evidence_quality=80,
        current_source_reliability=ineligible,
        baseline_source_reliability=_eligible(),
        minimum_evidence_quality=60,
    )

    assert result.eligible is False
    assert result.reason is StatisticalEvidenceEligibilityReason.INSUFFICIENT_SOURCE_RELIABILITY
