from datetime import datetime

from app.domain.business_economics import EconomicEstimate
from app.domain.economic_performance import EconomicPerformanceHistory, EconomicPerformanceOutcome
from app.domain.economic_health import (
    calculate_economic_health,
)


def _outcome(i: str, profit: float, effort: float = 2.0) -> EconomicPerformanceOutcome:
    revenue = 100.0 + profit
    estimate = EconomicEstimate(expected_revenue=100.0, expected_effort_hours=effort)
    return EconomicPerformanceOutcome(
        id=i,
        business_id="b1",
        estimate_id=f"e-{i}",
        estimate=estimate,
        observed_at=datetime(2026, 1, int(i[-1])),
        actual_revenue=revenue,
        actual_cost=100.0,
        actual_effort_hours=effort,
    )


def test_health_preserves_profitability_and_stability_metrics():
    history = EconomicPerformanceHistory(
        business_id="b1",
        outcomes=(_outcome("o1", 20.0), _outcome("o2", -10.0), _outcome("o3", 30.0)),
    )

    result = calculate_economic_health(history)

    assert result is not None
    assert result.outcome_count == 3
    assert result.profitable_outcome_count == 2
    assert result.loss_outcome_count == 1
    assert result.profitable_outcome_rate == 2 / 3
    assert result.average_actual_profit == 40 / 3
    assert result.minimum_actual_profit == -10.0
    assert result.maximum_actual_profit == 30.0
    assert result.sample_profit_standard_deviation is not None


def test_single_outcome_has_no_stability_deviation():
    result = calculate_economic_health(
        EconomicPerformanceHistory(business_id="b1", outcomes=(_outcome("o1", 20.0),))
    )
    assert result.sample_profit_standard_deviation is None


def test_empty_history_returns_no_economic_health():
    assert calculate_economic_health(EconomicPerformanceHistory(business_id="b1")) is None
