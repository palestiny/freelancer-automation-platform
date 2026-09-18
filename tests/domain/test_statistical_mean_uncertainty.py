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
    assert isclose(result.interval_lower, 5.0317245765, abs_tol=0.000001)
    assert isclose(result.interval_upper, 14.9682754235, abs_tol=0.000001)

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


def test_mean_uncertainty_rejects_duplicate_observation_ids():
    with pytest.raises(ValueError, match="observation_ids must be unique"):
        calculate_mean_uncertainty(
            (item("o1", 8), item("o1", 10, at=START + timedelta(hours=1))),
            window=window(),
        )


def test_mean_uncertainty_rejects_invalid_confidence_level():
    with pytest.raises(ValueError, match="confidence_level must be between zero and one"):
        calculate_mean_uncertainty(
            (item("o1", 8), item("o2", 10, at=START + timedelta(hours=1))),
            window=window(),
            confidence_level=1.0,
        )


def test_mean_uncertainty_empty_window_has_explicit_unknown_context():
    result = calculate_mean_uncertainty((), window=window())
    assert result.status is MeanUncertaintyStatus.INSUFFICIENT_OBSERVATIONS
    assert result.sample_size == 0
    assert result.observation_ids == ()
    assert result.business_id == "unknown"
    assert result.metric_name == "unknown"
    assert result.unit == "unknown"


def test_mean_uncertainty_matches_known_student_t_critical_values():
    # Two-sided 95% critical values from standard t-distribution tables.
    from app.domain.statistical_mean_uncertainty import _student_t_critical

    assert isclose(_student_t_critical(0.95, 1), 12.7062047364, rel_tol=1e-10)
    assert isclose(_student_t_critical(0.95, 2), 4.3026527297, rel_tol=1e-10)
    assert isclose(_student_t_critical(0.95, 10), 2.22813885196, rel_tol=1e-10)
    assert isclose(_student_t_critical(0.95, 30), 2.0422724563, rel_tol=1e-10)


def test_mean_uncertainty_uses_same_interval_for_negative_and_positive_t_values():
    from app.domain.statistical_mean_uncertainty import _student_t_cdf

    for value in (0.5, 1.5, 3.0):
        positive = _student_t_cdf(value, 7)
        negative = _student_t_cdf(-value, 7)
        assert isclose(positive + negative, 1.0, rel_tol=1e-12, abs_tol=1e-12)


def test_mean_uncertainty_supports_non_default_confidence_levels():
    from app.domain.statistical_mean_uncertainty import _student_t_critical

    # Standard two-sided t critical values: 99% confidence.
    assert isclose(_student_t_critical(0.99, 1), 63.6567411629, rel_tol=1e-9)
    assert isclose(_student_t_critical(0.99, 10), 3.169272673, rel_tol=1e-9)


def test_mean_uncertainty_t_cdf_remains_bounded():
    from app.domain.statistical_mean_uncertainty import _student_t_cdf

    for degrees_of_freedom in (1, 2, 10, 100):
        for value in (0.0, 0.1, 1.0, 10.0, 100.0):
            result = _student_t_cdf(value, degrees_of_freedom)
            assert 0.0 <= result <= 1.0


def test_mean_uncertainty_returns_inapplicable_when_assumptions_are_not_satisfied():
    result = calculate_mean_uncertainty(
        (item("o1", 8), item("o2", 10, at=START + timedelta(hours=1))),
        window=window(),
        assumptions_satisfied=False,
    )
    assert result.status is MeanUncertaintyStatus.INAPPLICABLE
    assert result.observation_ids == ("o1", "o2")
    assert result.sample_size == 2
    assert result.interval_lower is None
    assert result.interval_upper is None


def test_mean_uncertainty_rejects_non_boolean_assumption_flag():
    with pytest.raises(ValueError, match="assumptions_satisfied must be a boolean"):
        calculate_mean_uncertainty((), window=window(), assumptions_satisfied=1)
