from datetime import datetime, timedelta, timezone
from math import isclose

import pytest

from app.domain.business_performance import BusinessPerformanceObservation, PerformanceSourceType
from app.domain.performance_history import PerformanceWindow
from app.domain.statistical_mean_comparison import (
    MeanComparisonResult,
    MeanComparisonStatus,
    compare_historical_means,
)

START = datetime(2026, 1, 1, tzinfo=timezone.utc)


def item(id: str, actual: float, *, business_id: str = "business-1", at: datetime = START):
    return BusinessPerformanceObservation(
        id=id,
        business_id=business_id,
        source_type=PerformanceSourceType.OPERATIONAL,
        source_id=f"source-{id}",
        metric_name="delivery_hours",
        unit="hours",
        expected_value=None,
        actual_value=actual,
        observed_at=at,
    )


def window(start: datetime) -> PerformanceWindow:
    return PerformanceWindow(start, start + timedelta(days=1))


def test_welch_comparison_calculates_known_result():
    first = window(START)
    second = window(START + timedelta(days=2))
    result = compare_historical_means(
        (item("a1", 8), item("a2", 10, at=START + timedelta(hours=1)), item("a3", 12, at=START + timedelta(hours=2)),
         item("b1", 18, at=START + timedelta(days=2)), item("b2", 20, at=START + timedelta(days=2, hours=1)),
         item("b3", 22, at=START + timedelta(days=2, hours=2))),
        first_window=first,
        second_window=second,
    )
    assert result.status is MeanComparisonStatus.APPLICABLE
    assert result.method == "welch_two_sample_t_test"
    assert result.alpha == 0.05
    assert result.sample_size_first == 3
    assert result.sample_size_second == 3
    assert isclose(result.mean_first, 10.0)
    assert isclose(result.mean_second, 20.0)
    assert isclose(result.mean_difference, -10.0)
    assert isclose(result.t_statistic, -6.123724356957945, rel_tol=1e-9)
    assert isclose(result.degrees_of_freedom, 4.0, rel_tol=1e-9)
    assert result.p_value < 0.01
    assert result.rejects_null is True


def test_comparison_requires_two_observations_per_window():
    result = compare_historical_means(
        (item("a1", 10), item("b1", 20, at=START + timedelta(days=2))),
        first_window=window(START),
        second_window=window(START + timedelta(days=2)),
    )
    assert result.status is MeanComparisonStatus.INSUFFICIENT_OBSERVATIONS


def test_comparison_rejects_mixed_context():
    result = compare_historical_means(
        (item("a1", 10), item("a2", 11, at=START + timedelta(hours=1)),
         item("b1", 20, at=START + timedelta(days=2)), item("b2", 21, business_id="business-2", at=START + timedelta(days=2, hours=1))),
        first_window=window(START),
        second_window=window(START + timedelta(days=2)),
    )
    assert result.status is MeanComparisonStatus.INVALID_CONTEXT


def test_comparison_rejects_non_finite_values():
    result = compare_historical_means(
        (item("a1", float("nan")), item("a2", 11, at=START + timedelta(hours=1)),
         item("b1", 20, at=START + timedelta(days=2)), item("b2", 21, at=START + timedelta(days=2, hours=1))),
        first_window=window(START),
        second_window=window(START + timedelta(days=2)),
    )
    assert result.status is MeanComparisonStatus.INVALID_VALUE


def test_comparison_rejects_overlapping_windows():
    first = PerformanceWindow(START, START + timedelta(days=2))
    second = PerformanceWindow(START + timedelta(days=1), START + timedelta(days=3))
    result = compare_historical_means(
        (item("a1", 10), item("a2", 11, at=START + timedelta(hours=1)),
         item("b1", 20, at=START + timedelta(days=1, hours=1)), item("b2", 21, at=START + timedelta(days=1, hours=2))),
        first_window=first,
        second_window=second,
    )
    assert result.status is MeanComparisonStatus.INVALID_CONTEXT


def test_comparison_requires_explicit_applicability():
    result = compare_historical_means(
        (item("a1", 10), item("a2", 11, at=START + timedelta(hours=1)),
         item("b1", 20, at=START + timedelta(days=2)), item("b2", 21, at=START + timedelta(days=2, hours=1))),
        first_window=window(START),
        second_window=window(START + timedelta(days=2)),
        assumptions_satisfied=False,
    )
    assert result.status is MeanComparisonStatus.INAPPLICABLE


def test_comparison_rejects_duplicate_observation_ids():
    with pytest.raises(ValueError, match="observation_ids must be unique"):
        compare_historical_means(
            (item("a1", 10), item("a1", 11, at=START + timedelta(hours=1)),
             item("b1", 20, at=START + timedelta(days=2)), item("b2", 21, at=START + timedelta(days=2, hours=1))),
            first_window=window(START),
            second_window=window(START + timedelta(days=2)),
        )


def test_comparison_rejects_invalid_alpha():
    with pytest.raises(ValueError, match="alpha must be between zero and one"):
        compare_historical_means(
            (item("a1", 10), item("a2", 11, at=START + timedelta(hours=1)),
             item("b1", 20, at=START + timedelta(days=2)), item("b2", 21, at=START + timedelta(days=2, hours=1))),
            first_window=window(START),
            second_window=window(START + timedelta(days=2)),
            alpha=1.0,
        )


def test_welch_comparison_preserves_fractional_degrees_of_freedom():
    result = compare_historical_means(
        (item("a1", 1), item("a2", 2, at=START + timedelta(hours=1)), item("a3", 3, at=START + timedelta(hours=2)),
         item("b1", 10, at=START + timedelta(days=2)), item("b2", 20, at=START + timedelta(days=2, hours=1)),
         item("b3", 40, at=START + timedelta(days=2, hours=2)), item("b4", 80, at=START + timedelta(days=2, hours=3))),
        first_window=window(START),
        second_window=window(START + timedelta(days=2)),
    )
    assert result.status is MeanComparisonStatus.APPLICABLE
    assert result.degrees_of_freedom is not None
    assert result.degrees_of_freedom != int(result.degrees_of_freedom)
    assert result.p_value is not None
    assert 0.0 <= result.p_value <= 1.0

