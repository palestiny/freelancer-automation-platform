from datetime import datetime

from app.domain.economic_health import EconomicHealthEvidence
from app.domain.economic_performance_aggregation import EconomicPerformanceWindow
from app.domain.economic_stability_policy import (
    EconomicStabilityEligibilityReason,
    EconomicStabilityPolicy,
    assess_economic_stability,
)


def _health() -> EconomicHealthEvidence:
    return EconomicHealthEvidence(
        business_id="b1",
        window=EconomicPerformanceWindow(datetime(2026, 1, 1), datetime(2026, 2, 1)),
        outcome_ids=("o1", "o2", "o3"),
        outcome_count=3,
        profitable_outcome_count=3,
        loss_outcome_count=0,
        profitable_outcome_rate=1.0,
        average_actual_profit=100.0,
        minimum_actual_profit=80.0,
        maximum_actual_profit=120.0,
        sample_profit_standard_deviation=20.0,
        average_actual_margin=0.2,
        average_actual_profit_per_effort_hour=50.0,
    )


def _policy(**kwargs) -> EconomicStabilityPolicy:
    values = dict(
        minimum_observations=3,
        minimum_profitable_outcome_rate=0.8,
        minimum_average_actual_profit=50.0,
        maximum_profit_stddev_ratio=0.5,
    )
    values.update(kwargs)
    return EconomicStabilityPolicy(**values)


def test_stable_profitability_is_eligible():
    result = assess_economic_stability(health=_health(), policy=_policy())
    assert result.eligible is True
    assert result.reason is EconomicStabilityEligibilityReason.ELIGIBLE
    assert result.profit_stddev_ratio == 0.2


def test_insufficient_observations_is_explicit():
    health = _health()
    health = EconomicHealthEvidence(
        business_id=health.business_id,
        window=health.window,
        outcome_ids=("o1", "o2"),
        outcome_count=2,
        profitable_outcome_count=2,
        loss_outcome_count=0,
        profitable_outcome_rate=1.0,
        average_actual_profit=100.0,
        minimum_actual_profit=80.0,
        maximum_actual_profit=120.0,
        sample_profit_standard_deviation=None,
        average_actual_margin=0.2,
        average_actual_profit_per_effort_hour=50.0,
    )
    result = assess_economic_stability(health=health, policy=_policy())
    assert result.reason is EconomicStabilityEligibilityReason.INSUFFICIENT_OBSERVATIONS


def test_high_variability_is_rejected():
    health = _health()
    health = EconomicHealthEvidence(
        business_id=health.business_id,
        window=health.window,
        outcome_ids=health.outcome_ids,
        outcome_count=health.outcome_count,
        profitable_outcome_count=health.profitable_outcome_count,
        loss_outcome_count=health.loss_outcome_count,
        profitable_outcome_rate=health.profitable_outcome_rate,
        average_actual_profit=100.0,
        minimum_actual_profit=0.0,
        maximum_actual_profit=200.0,
        sample_profit_standard_deviation=60.0,
        average_actual_margin=health.average_actual_margin,
        average_actual_profit_per_effort_hour=health.average_actual_profit_per_effort_hour,
    )
    result = assess_economic_stability(health=health, policy=_policy())
    assert result.reason is EconomicStabilityEligibilityReason.PROFIT_VARIABILITY_ABOVE_THRESHOLD
