import pytest

from app.domain.resource_economics import ResourceKind, ResourceUsage


def test_resource_usage_calculates_total_cost():
    usage = ResourceUsage(
        kind=ResourceKind.HUMAN_TIME,
        quantity=5,
        unit_cost=20,
    )

    assert usage.total_cost == 100


def test_resource_usage_rejects_negative_quantity():
    with pytest.raises(ValueError):
        ResourceUsage(ResourceKind.HUMAN_TIME, -1, 20)


def test_resource_usage_rejects_negative_unit_cost():
    with pytest.raises(ValueError):
        ResourceUsage(ResourceKind.HUMAN_TIME, 5, -1)


def test_resource_kinds_are_explicit():
    assert {kind.value for kind in ResourceKind} == {
        "human_time",
        "capability_usage",
        "infrastructure",
        "communication",
        "marketplace_fee",
        "review_time",
    }
