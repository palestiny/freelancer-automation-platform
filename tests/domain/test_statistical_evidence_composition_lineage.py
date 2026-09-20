from datetime import datetime
import pytest

from app.domain.performance_history import PerformanceWindow
from app.domain.performance_reliability import SourceReliabilityAssessment, SourceReliabilityReason
from app.domain.statistical_evidence_composition import (
    StatisticalEvidenceComposition,
    StatisticalEvidenceEligibilityReason,
    StatisticalEvidenceInterpretation,
)


def _window(start_day, end_day):
    return PerformanceWindow(datetime(2026, 1, start_day), datetime(2026, 1, end_day))


def _base(**kwargs):
    values = dict(
        business_id="b1",
        metric_name="profit",
        unit="EGP",
        method="welch_two_sample_t_test",
        observation_ids=("a", "b", "c", "d"),
        eligible=True,
        reason=StatisticalEvidenceEligibilityReason.ELIGIBLE,
        interpretation=StatisticalEvidenceInterpretation.STATISTICALLY_DETECTED_DIFFERENCE,
        alpha=0.05,
        mean_difference=10.0,
        first_window=_window(1, 8),
        second_window=_window(8, 15),
        current_evidence_quality=80,
        baseline_evidence_quality=80,
        current_source_reliability=SourceReliabilityAssessment(eligible=True, reason=SourceReliabilityReason.ELIGIBLE, minimum_reliability=80),
        baseline_source_reliability=SourceReliabilityAssessment(eligible=True, reason=SourceReliabilityReason.ELIGIBLE, minimum_reliability=80),
    )
    values.update(kwargs)
    return StatisticalEvidenceComposition(**values)


def test_composition_preserves_statistical_windows_and_difference():
    result = _base()
    assert result.mean_difference == 10.0
    assert result.first_window == _window(1, 8)
    assert result.second_window == _window(8, 15)


def test_composition_rejects_overlapping_statistical_windows():
    with pytest.raises(ValueError):
        _base(second_window=_window(7, 15))


def test_composition_allows_missing_mean_difference_for_non_applicable_result():
    result = _base(
        eligible=False,
        reason=StatisticalEvidenceEligibilityReason.STATISTICAL_RESULT_NOT_APPLICABLE,
        interpretation=StatisticalEvidenceInterpretation.STATISTICAL_RESULT_NOT_APPLICABLE,
        mean_difference=None,
    )
    assert result.mean_difference is None
