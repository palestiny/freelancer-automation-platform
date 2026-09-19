from dataclasses import dataclass
from datetime import datetime

from .economic_performance import EconomicPerformanceHistory, EconomicPerformanceOutcome


@dataclass(frozen=True)
class EconomicPerformanceWindow:
    start: datetime
    end: datetime

    def __post_init__(self) -> None:
        if self.end <= self.start:
            raise ValueError("end must be after start")

    def contains(self, observed_at: datetime) -> bool:
        return self.start <= observed_at < self.end


@dataclass(frozen=True)
class EconomicPerformanceAggregate:
    business_id: str
    window: EconomicPerformanceWindow
    outcome_ids: tuple[str, ...]
    outcome_count: int
    average_actual_revenue: float
    average_actual_cost: float
    average_actual_profit: float
    average_actual_effort_hours: float
    average_revenue_variance: float
    average_cost_variance: float
    average_profit_variance: float
    average_effort_variance: float

    def __post_init__(self) -> None:
        if not self.business_id.strip():
            raise ValueError("business_id cannot be empty")
        if not self.outcome_ids:
            raise ValueError("outcome_ids cannot be empty")
        if len(set(self.outcome_ids)) != len(self.outcome_ids):
            raise ValueError("outcome_ids must be unique")
        if self.outcome_count != len(self.outcome_ids):
            raise ValueError("outcome_count must match outcome_ids")


def aggregate_economic_performance(
    history: EconomicPerformanceHistory,
    window: EconomicPerformanceWindow,
) -> EconomicPerformanceAggregate | None:
    selected = tuple(o for o in history.outcomes if window.contains(o.observed_at))
    if not selected:
        return None

    def avg(values):
        return sum(values) / len(selected)

    return EconomicPerformanceAggregate(
        business_id=history.business_id,
        window=window,
        outcome_ids=tuple(o.id for o in selected),
        outcome_count=len(selected),
        average_actual_revenue=avg(o.actual_revenue for o in selected),
        average_actual_cost=avg(o.actual_cost for o in selected),
        average_actual_profit=avg(o.actual_profit for o in selected),
        average_actual_effort_hours=avg(o.actual_effort_hours for o in selected),
        average_revenue_variance=avg(o.revenue_variance for o in selected),
        average_cost_variance=avg(o.cost_variance for o in selected),
        average_profit_variance=avg(o.profit_variance for o in selected),
        average_effort_variance=avg(o.effort_variance for o in selected),
    )
