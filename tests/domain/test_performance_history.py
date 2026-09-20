from datetime import datetime, timedelta, timezone

import pytest

from app.domain.business_performance import BusinessPerformanceHistory, BusinessPerformanceObservation, PerformanceSourceType
from app.domain.performance_history import PerformanceWindow, observations_in_window, rolling_window


def item(id: str, at: datetime) -> BusinessPerformanceObservation:
    return BusinessPerformanceObservation(
        id=id,
        business_id="business-1",
        source_type=PerformanceSourceType.OPERATIONAL,
        source_id=f"source-{id}",
        metric_name="delivery_hours",
        unit="hours",
        expected_value=10,
        actual_value=12,
        observed_at=at,
    )


def test_window_is_start_inclusive_and_end_exclusive():
    start = datetime(2026, 1, 1, tzinfo=timezone.utc)
    window = PerformanceWindow(start=start, end=start + timedelta(days=1))

    assert window.contains(start)
    assert not window.contains(start + timedelta(days=1))


def test_window_rejects_invalid_period():
    at = datetime(2026, 1, 1)
    with pytest.raises(ValueError):
        PerformanceWindow(start=at, end=at)


def test_history_can_be_scoped_to_a_time_window():
    start = datetime(2026, 1, 1, tzinfo=timezone.utc)
    history = BusinessPerformanceHistory(
        business_id="business-1",
        observations=(
            item("before", start - timedelta(seconds=1)),
            item("inside", start + timedelta(hours=1)),
            item("at-end", start + timedelta(days=1)),
        ),
    )
    window = PerformanceWindow(start=start, end=start + timedelta(days=1))

    assert [x.id for x in observations_in_window(history, window)] == ["inside"]


def test_rolling_window_ends_at_requested_time():
    end = datetime(2026, 1, 10, tzinfo=timezone.utc)
    window = rolling_window(end=end, duration=timedelta(days=7))

    assert window.start == datetime(2026, 1, 3)
    assert window.end == end


def test_rolling_window_rejects_non_positive_duration():
    with pytest.raises(ValueError):
        rolling_window(end=datetime(2026, 1, 10), duration=timedelta(0))
