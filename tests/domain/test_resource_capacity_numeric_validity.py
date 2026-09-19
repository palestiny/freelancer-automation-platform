import math
from datetime import datetime, timezone

import pytest

from app.domain.capacity import CapacitySnapshot
from app.domain.resource_economics import ResourceKind, ResourceUsage


@pytest.mark.parametrize("value", [math.nan, math.inf, -math.inf])
def test_resource_usage_rejects_non_finite_quantity(value):
    with pytest.raises(ValueError, match="quantity must be finite"):
        ResourceUsage(kind=ResourceKind.HUMAN_TIME, quantity=value, unit_cost=10)


@pytest.mark.parametrize("value", [math.nan, math.inf, -math.inf])
def test_resource_usage_rejects_non_finite_unit_cost(value):
    with pytest.raises(ValueError, match="unit_cost must be finite"):
        ResourceUsage(kind=ResourceKind.HUMAN_TIME, quantity=1, unit_cost=value)


@pytest.mark.parametrize("field", ["total_hours", "committed_hours", "reserved_hours"])
def test_capacity_rejects_non_finite_hours(field):
    values = {
        "total_hours": 10.0,
        "committed_hours": 0.0,
        "reserved_hours": 0.0,
    }
    values[field] = math.inf
    with pytest.raises(ValueError, match=f"{field} must be finite"):
        CapacitySnapshot(
            period_start=datetime(2026, 1, 1, tzinfo=timezone.utc),
            period_end=datetime(2026, 1, 2, tzinfo=timezone.utc),
            **values,
        )
