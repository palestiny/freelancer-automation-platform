from dataclasses import dataclass
from math import sqrt

from .economic_performance import EconomicPerformanceHistory


@dataclass(frozen=True)
class EconomicHealthEvidence:
    business_id: str
    outcome_ids: tuple[str, ...]
    outcome_count: int
    profitable_outcome_count: int
    loss_outcome_count: int
    profitable_outcome_rate: float
    average_actual_profit: float
    minimum_actual_profit: float
    maximum_actual_profit: float
    sample_profit_standard_deviation: float | None
    average_actual_margin: float | None
    average_actual_profit_per_effort_hour: float | None

    def __post_init__(self) -> None:
        if not self.business_id.strip():
            raise ValueError("business_id cannot be empty")
        if not self.outcome_ids:
            raise ValueError("outcome_ids cannot be empty")
        if len(set(self.outcome_ids)) != len(self.outcome_ids):
            raise ValueError("outcome_ids must be unique")
        if self.outcome_count != len(self.outcome_ids):
            raise ValueError("outcome_count must match outcome_ids")
        if self.profitable_outcome_count + self.loss_outcome_count != self.outcome_count:
            raise ValueError("profit/loss counts must cover all outcomes")
        if not 0 <= self.profitable_outcome_rate <= 1:
            raise ValueError("profitable_outcome_rate must be between 0 and 1")


def calculate_economic_health(
    history: EconomicPerformanceHistory,
) -> EconomicHealthEvidence | None:
    if not history.outcomes:
        return None

    outcomes = tuple(history.ordered_outcomes)
    profits = tuple(o.actual_profit for o in outcomes)
    margins = tuple(o.actual_margin for o in outcomes if o.actual_margin is not None)
    profit_per_hour = tuple(
        o.actual_profit / o.actual_effort_hours
        for o in outcomes
        if o.actual_effort_hours > 0
    )

    count = len(outcomes)
    profitable = sum(1 for value in profits if value > 0)
    losses = sum(1 for value in profits if value < 0)
    average_profit = sum(profits) / count

    standard_deviation = None
    if count >= 2:
        variance = sum((value - average_profit) ** 2 for value in profits) / (count - 1)
        standard_deviation = sqrt(variance)

    return EconomicHealthEvidence(
        business_id=history.business_id,
        outcome_ids=tuple(o.id for o in outcomes),
        outcome_count=count,
        profitable_outcome_count=profitable,
        loss_outcome_count=losses,
        profitable_outcome_rate=profitable / count,
        average_actual_profit=average_profit,
        minimum_actual_profit=min(profits),
        maximum_actual_profit=max(profits),
        sample_profit_standard_deviation=standard_deviation,
        average_actual_margin=(sum(margins) / len(margins)) if margins else None,
        average_actual_profit_per_effort_hour=(
            sum(profit_per_hour) / len(profit_per_hour)
            if profit_per_hour
            else None
        ),
    )
