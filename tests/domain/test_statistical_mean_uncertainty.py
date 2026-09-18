from datetime import datetime, timedelta
from math import isclose

import pytest

from app.domain.business_performance import BusinessPerformanceObservation, PerformanceSourceType
from app.domain.performance_history import PerformanceWindow
from app.domain.statistical_mean_uncertainty import MeanUncertaintyStatus, calculate_mean_uncertainty

START = datetime(2026, 1, 1)

def item(id: str, actual: float, *, at: datetime = START) -> BusinessPerformanceObservation:
    return BusinessPerformanceObservation(
        id=id, business_id="business-1", source_type=PerformanceSourceType.OPERATIONAL,
        source_id=f"source-{id}", metric_name="delivery_hours", unit="hours",
        expected_value=None, actual_value=actual, observed_at=at,
    )

def window() -> PerformanceWindow:
    return PerformanceWindow(START, START + timedelta(days=1))

def test_mean_uncertainty_rejects_fewer_than_two_observations():
    result = calculate_mean_uncertainty((item("o1", 10),), window=window())
    assert result.status is MeanUncertaintyStatus.INSUFFICIENT_OBSERVATIONS
    assert result.sample_size == 1
    assert result.observation_ids == ("o1",)
    assert result.interval_lower is None
    assert result.interval_upper is None

def test_mean_uncertainty_calculates_t_interval_and_preserves_lineage():
    result = calculate_mean_uncertainty(
        (item("o1", 8), item("o2", 10, at=START + timedelta(hours=1)), item("o3", 12, at=START + timedelta(hours=2))),
        window=window(),
    )
    assert result.status is MeanUncertaintyStatus.APPLICABLE
    assert result.method == "student_t_mean_ci"
    assert result.confidence_level == 0.95
    assert result.sample_size == 3
    assert result.observation_ids == ("o1", "o2", "o3")
    assert result.sample_mean == 10
    assert isclose(result.sample_standard_deviation, 2.0, rel_tol=1e-12)
    assert result.interval_lower is not None
    assert result.interval_upper is not None
    assert isclose(result.interval_lower, -0.205, abs_tol=0.02)
    assert isclose(result.interval_upper, 20.205, abs_tol=0.02)

def test_mean_uncertainty_uses_explicit_window():
    result = calculate_mean_uncertainty(
        (item("before", 100, at=START - timedelta(seconds=1)), item("inside", 10), item("at-end", 100, at=START + timedelta(days=1))),
        window=window(),
    )
    assert result.observation_ids == ("inside",)
    assert result.status is MeanUncertaintyStatus.INSUFFICIENT_OBSERVATIONS

def test_mean_uncertainty_rejects_mixed_context():
    other = BusinessPerformanceObservation(
        id="o2", business_id="business-2", source_type=PerformanceSourceType.OPERATIONAL,
        source_id="source-o2", metric_name="delivery_hours", unit="hours",
        expected_value=None, actual_value=12, observed_at=START + timedelta(hours=1),
    )
    result = calculate_mean_uncertainty((item("o1", 10), other), window=window())
    assert result.status is MeanUncertaintyStatus.INVALID_CONTEXT

def test_mean_uncertainty_rejects_non_finite_values():
    result = calculate_mean_uncertainty((item("o1", float("nan")), item("o2", 10)), window=window())
    assert result.status is MeanUncertaintyStatus.INVALID_VALUE
