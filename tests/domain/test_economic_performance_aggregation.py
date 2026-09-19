from datetime import datetime, timezone

from app.domain.business_economics import EconomicEstimate
from app.domain.economic_performance import EconomicPerformanceHistory, EconomicPerformanceOutcome
from app.domain.economic_performance_aggregation import (
    EconomicPerformanceWindow,
    aggregate_economic_performance,
)


def _estimate():
    return EconomicEstimate(expected_revenue=1000, expected_effort_hours=10, platform_fee=100)


def _outcome(id, day, revenue, cost, effort):
    return EconomicPerformanceOutcome(
        id=id, business_id="b1", estimate_id="e1", estimate=_estimate(),
        observed_at=datetime(2026, 9, day, tzinfo=timezone.utc),
        actual_revenue=revenue, actual_cost=cost, actual_effort_hours=effort,
    )


def test_aggregates_selected_realized_economics():
    history = EconomicPerformanceHistory(
        business_id="b1",
        outcomes=(
            _outcome("o1", 1, 1200, 250, 12),
            _outcome("o2", 3, 800, 200, 8),
            _outcome("o3", 10, 2000, 500, 20),
        ),
    )
    result = aggregate_economic_performance(
        history,
        EconomicPerformanceWindow(
            start=datetime(2026, 9, 1, tzinfo=timezone.utc),
            end=datetime(2026, 9, 4, tzinfo=timezone.utc),
        ),
    )
    assert result is not None
    assert result.outcome_ids == ("o1", "o2")
    assert result.outcome_count == 2
    assert result.average_actual_revenue == 1000
    assert result.average_actual_cost == 225
    assert result.average_actual_profit == 775
    assert result.average_actual_effort_hours == 10
    assert result.average_profit_variance == -225
    assert result.average_revenue_variance == -100
    assert result.average_cost_variance == 125
    assert result.average_effort_variance == 0


def test_window_is_start_inclusive_and_end_exclusive():
    history = EconomicPerformanceHistory(
        business_id="b1",
        outcomes=(_outcome("o1", 1, 1200, 250, 12), _outcome("o2", 3, 800, 200, 8)),
    )
    window = EconomicPerformanceWindow(
        start=datetime(2026, 9, 1, tzinfo=timezone.utc),
        end=datetime(2026, 9, 3, tzinfo=timezone.utc),
    )
    result = aggregate_economic_performance(history, window)
    assert result is not None
    assert result.outcome_ids == ("o1",)


def test_empty_window_returns_none():
    history = EconomicPerformanceHistory(business_id="b1", outcomes=(_outcome("o1", 1, 1200, 250, 12),))
    result = aggregate_economic_performance(
        history,
        EconomicPerformanceWindow(
            start=datetime(2026, 9, 5, tzinfo=timezone.utc),
            end=datetime(2026, 9, 6, tzinfo=timezone.utc),
        ),
    )
    assert result is None
