from datetime import datetime, timedelta, timezone

import pytest

from app.domain.performance_aggregation import aggregate_performance
from app.domain.performance_history import PerformanceWindow
from app.domain.performance_trend import PerformanceTrend, compare_performance
from tests.domain.test_performance_aggregation import item


START = datetime(2026, 1, 1, tzinfo=timezone.utc)


def test_compare_performance_reports_absolute_and_relative_change():
    baseline_window = PerformanceWindow(START, START + timedelta(days=1))
    current_window = PerformanceWindow(
        START + timedelta(days=1), START + timedelta(days=2)
    )
    baseline = aggregate_performance(
        (item("b1", 10, at=START + timedelta(hours=1)),),
        window=baseline_window,
    )
    current = aggregate_performance(
        (item("c1", 15, at=START + timedelta(days=1, hours=1)),),
        window=current_window,
    )

    result = compare_performance(current=current, baseline=baseline)

    assert isinstance(result, PerformanceTrend)
    assert result.baseline_average == 10
    assert result.current_average == 15
    assert result.absolute_change == 5
    assert result.relative_change == 0.5
    assert result.baseline_observation_ids == ("b1",)
    assert result.current_observation_ids == ("c1",)


def test_compare_performance_returns_none_when_a_window_has_no_data():
    window = PerformanceWindow(START, START + timedelta(days=1))
    baseline = aggregate_performance(
        (item("b1", 10),),
        window=window,
    )

    assert compare_performance(current=None, baseline=baseline) is None


def test_compare_performance_does_not_divide_by_zero():
    baseline_window = PerformanceWindow(START, START + timedelta(days=1))
    current_window = PerformanceWindow(
        START + timedelta(days=1), START + timedelta(days=2)
    )
    baseline = aggregate_performance(
        (item("b1", 0),),
        window=baseline_window,
    )
    current = aggregate_performance(
        (item("c1", 5, at=START + timedelta(days=1, hours=1)),),
        window=current_window,
    )

    result = compare_performance(current=current, baseline=baseline)

    assert result.relative_change is None
    assert result.absolute_change == 5


def test_compare_performance_rejects_incompatible_aggregates():
    window = PerformanceWindow(START, START + timedelta(days=1))
    current = aggregate_performance((item("c1", 5),), window=window)
    other_business = aggregate_performance(
        (item("b1", 5, business_id="business-2"),),
        window=window,
    )

    with pytest.raises(ValueError):
        compare_performance(current=current, baseline=other_business)



def test_performance_trend_exposes_explicit_windows():
    baseline_window = PerformanceWindow(START, START + timedelta(days=1))
    current_window = PerformanceWindow(START + timedelta(days=1), START + timedelta(days=2))
    baseline = aggregate_performance(
        (item("b1", 10),),
        window=baseline_window,
    )
    current = aggregate_performance(
        (item("c1", 15, at=START + timedelta(days=1, hours=1)),),
        window=current_window,
    )

    result = compare_performance(current=current, baseline=baseline)

    assert result.current_window == current_window
    assert result.baseline_window == baseline_window
    assert isinstance(result.current_window, PerformanceWindow)
    assert isinstance(result.baseline_window, PerformanceWindow)
