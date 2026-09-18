from datetime import datetime, timedelta

import pytest

from app.domain.capacity import CapacitySnapshot


def make_capacity(**overrides):
    values = {
        "period_start": datetime(2026, 1, 1, 9, 0),
        "period_end": datetime(2026, 1, 31, 17, 0),
        "total_hours": 160,
        "committed_hours": 40,
        "reserved_hours": 20,
    }
    values.update(overrides)
    return CapacitySnapshot(**values)


def test_capacity_calculates_remaining_hours():
    capacity = make_capacity()

    assert capacity.remaining_hours == 100


def test_capacity_calculates_utilization():
    capacity = make_capacity()

    assert capacity.utilization == pytest.approx(0.375)


def test_capacity_rejects_invalid_period():
    start = datetime(2026, 1, 10)
    with pytest.raises(ValueError):
        make_capacity(period_start=start, period_end=start)


@pytest.mark.parametrize(
    "field",
    ["total_hours", "committed_hours", "reserved_hours"],
)
def test_capacity_rejects_negative_hours(field):
    values = {"total_hours": 160, "committed_hours": 40, "reserved_hours": 20}
    values[field] = -1

    with pytest.raises(ValueError):
        make_capacity(**values)


def test_capacity_rejects_over_committed_capacity():
    with pytest.raises(ValueError):
        make_capacity(committed_hours=150, reserved_hours=20)


def test_capacity_is_not_overallocated():
    capacity = make_capacity()

    assert capacity.remaining_hours >= 0
