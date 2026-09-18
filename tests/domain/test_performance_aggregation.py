from datetime import datetime, timedelta

import pytest

from app.domain.business_performance import (
    BusinessPerformanceHistory,
    BusinessPerformanceObservation,
    PerformanceSourceType,
)
from app.domain.performance_aggregation import (
    PerformanceAggregate,
    aggregate_history_metric,
    aggregate_performance,
)
from app.domain.performance_history import PerformanceWindow


START = datetime(2026, 1, 1)


def item(
    id: str,
    actual: float,
    *,
    expected: float | None = 10,
    at: datetime = START,
    evidence_quality: int = 50,
    metric_name: str = "delivery_hours",
    unit: str = "hours",
    business_id: str = "business-1",
) -> BusinessPerformanceObservation:
    return BusinessPerformanceObservation(
        id=id,
        business_id=business_id,
        source_type=PerformanceSourceType.OPERATIONAL,
        source_id=f"source-{id}",
        metric_name=metric_name,
        unit=unit,
        expected_value=expected,
        actual_value=actual,
        observed_at=at,
        evidence_quality=evidence_quality,
    )


def window() -> PerformanceWindow:
    return PerformanceWindow(START, START + timedelta(days=1))


def test_aggregate_returns_none_for_empty_window():
    assert aggregate_performance((), window=window()) is None


def test_aggregate_preserves_source_observation_ids_and_basic_actuals():
    result = aggregate_performance(
        (
            item("o1", 8, at=START + timedelta(hours=1)),
            item("o2", 12, at=START + timedelta(hours=2)),
        ),
        window=window(),
    )

    assert isinstance(result, PerformanceAggregate)
    assert result.observation_ids == ("o1", "o2")
    assert result.actual_count == 2
    assert result.actual_average == 10
    assert result.actual_min == 8
    assert result.actual_max == 12


def test_aggregate_keeps_expected_values_separate():
    result = aggregate_performance(
        (
            item("o1", 12, expected=10),
            item("o2", 16, expected=None, at=START + timedelta(hours=1)),
        ),
        window=window(),
    )

    assert result.expected_count == 1
    assert result.expected_average == 10
    assert result.average_variance == 2
    assert result.average_relative_variance == 0.2


def test_aggregate_does_not_invent_expected_values():
    result = aggregate_performance(
        (
            item("o1", 12, expected=None),
            item("o2", 16, expected=None, at=START + timedelta(hours=1)),
        ),
        window=window(),
    )

    assert result.expected_count == 0
    assert result.expected_average is None
    assert result.average_variance is None
    assert result.average_relative_variance is None


def test_zero_expected_values_do_not_create_relative_variance():
    result = aggregate_performance(
        (
            item("o1", 12, expected=0),
            item("o2", 8, expected=10, at=START + timedelta(hours=1)),
        ),
        window=window(),
    )

    assert result.expected_count == 2
    assert result.average_variance == 5
    assert result.average_relative_variance == -0.2


def test_aggregate_uses_selected_window_only():
    result = aggregate_performance(
        (
            item("before", 100, at=START - timedelta(seconds=1)),
            item("inside", 12),
            item("at-end", 100, at=START + timedelta(days=1)),
        ),
        window=window(),
    )

    assert result.observation_ids == ("inside",)


def test_history_metric_aggregation_filters_metric_and_unit():
    history = BusinessPerformanceHistory(
        business_id="business-1",
        observations=(
            item("delivery", 12),
            item("defect", 2, metric_name="defects", unit="count"),
        ),
    )

    result = aggregate_history_metric(
        history,
        metric_name="delivery_hours",
        unit="hours",
        window=window(),
    )

    assert result.observation_ids == ("delivery",)


def test_aggregation_rejects_mixed_business_or_metric_input():
    with pytest.raises(ValueError):
        aggregate_performance(
            (
                item("o1", 12),
                item("o2", 13, business_id="business-2"),
            ),
            window=window(),
        )

    with pytest.raises(ValueError):
        aggregate_performance(
            (
                item("o1", 12),
                item("o2", 13, metric_name="defects", unit="count"),
            ),
            window=window(),
        )


def test_average_evidence_quality_is_deterministic():
    result = aggregate_performance(
        (
            item("o1", 12, evidence_quality=80),
            item("o2", 10, evidence_quality=60, at=START + timedelta(hours=1)),
        ),
        window=window(),
    )

    assert result.average_evidence_quality == 70
