from datetime import datetime, timezone

import pytest

from app.domain.business_economics import EconomicEstimate
from app.domain.economic_performance import EconomicPerformanceHistory, EconomicPerformanceOutcome


def estimate():
    return EconomicEstimate(
        expected_revenue=1000,
        expected_effort_hours=10,
        platform_fee=100,
        capability_cost=100,
    )


def outcome(**overrides):
    values = dict(
        id="o1",
        business_id="b1",
        estimate_id="e1",
        estimate=estimate(),
        observed_at=datetime(2026, 9, 1, tzinfo=timezone.utc),
        actual_revenue=1200,
        actual_cost=250,
        actual_effort_hours=12,
    )
    values.update(overrides)
    return EconomicPerformanceOutcome(**values)


def test_derives_actual_profit_and_margin():
    result = outcome()
    assert result.actual_profit == 950
    assert result.actual_margin == 950 / 1200


def test_derives_variances_as_actual_minus_expected():
    result = outcome()
    assert result.revenue_variance == 200
    assert result.cost_variance == 50
    assert result.profit_variance == 150
    assert result.effort_variance == 2


def test_zero_revenue_has_no_margin():
    assert outcome(actual_revenue=0).actual_margin is None


@pytest.mark.parametrize("field", ["actual_revenue", "actual_cost", "actual_effort_hours"])
def test_negative_actual_values_are_rejected(field):
    with pytest.raises(ValueError):
        outcome(**{field: -1})


def test_history_cannot_mix_businesses():
    with pytest.raises(ValueError):
        EconomicPerformanceHistory(
            business_id="b1",
            outcomes=(outcome(), outcome(id="o2", business_id="b2")),
        )


def test_history_orders_outcomes_by_observed_time():
    first = outcome(id="o1", observed_at=datetime(2026, 9, 1, tzinfo=timezone.utc))
    second = outcome(id="o2", observed_at=datetime(2026, 9, 3, tzinfo=timezone.utc))
    history = EconomicPerformanceHistory(business_id="b1", outcomes=(second, first))
    assert tuple(o.id for o in history.ordered_outcomes) == ("o1", "o2")

import pytest

@pytest.mark.parametrize("field", ["actual_revenue", "actual_cost", "actual_effort_hours"])
def test_non_finite_realized_values_are_rejected(field):
    kwargs = {
        "id": "o1",
        "business_id": "b1",
        "estimate_id": "e1",
        "estimate": EconomicEstimate(expected_revenue=100, expected_effort_hours=2),
        "observed_at": datetime(2026, 1, 1),
        "actual_revenue": 100.0,
        "actual_cost": 20.0,
        "actual_effort_hours": 2.0,
    }
    kwargs[field] = float("nan")
    with pytest.raises(ValueError, match="finite"):
        EconomicPerformanceOutcome(**kwargs)
