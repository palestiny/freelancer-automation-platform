from dataclasses import dataclass
from datetime import datetime
from math import isfinite

from .business_economics import EconomicEstimate


@dataclass(frozen=True)
class EconomicPerformanceOutcome:
    id: str
    business_id: str
    estimate_id: str
    estimate: EconomicEstimate
    observed_at: datetime
    actual_revenue: float
    actual_cost: float
    actual_effort_hours: float

    def __post_init__(self) -> None:
        for name in ("id", "business_id", "estimate_id"):
            if not getattr(self, name).strip():
                raise ValueError(f"{name} cannot be empty")
        for name in ("actual_revenue", "actual_cost", "actual_effort_hours"):
            value = getattr(self, name)
            if not isfinite(value):
                raise ValueError(f"{name} must be finite")
            if value < 0:
                raise ValueError(f"{name} cannot be negative")

    @property
    def actual_profit(self) -> float:
        return self.actual_revenue - self.actual_cost

    @property
    def actual_margin(self) -> float | None:
        if self.actual_revenue == 0:
            return None
        return self.actual_profit / self.actual_revenue

    @property
    def revenue_variance(self) -> float:
        return self.actual_revenue - self.estimate.expected_revenue

    @property
    def cost_variance(self) -> float:
        return self.actual_cost - self.estimate.expected_cost

    @property
    def profit_variance(self) -> float:
        return self.actual_profit - self.estimate.expected_profit

    @property
    def effort_variance(self) -> float:
        return self.actual_effort_hours - self.estimate.expected_effort_hours


@dataclass(frozen=True)
class EconomicPerformanceHistory:
    business_id: str
    outcomes: tuple[EconomicPerformanceOutcome, ...] = ()

    def __post_init__(self) -> None:
        if not self.business_id.strip():
            raise ValueError("business_id cannot be empty")
        if any(o.business_id != self.business_id for o in self.outcomes):
            raise ValueError("all outcomes must belong to the history business")
        ids = [o.id for o in self.outcomes]
        if len(ids) != len(set(ids)):
            raise ValueError("outcome ids must be unique")

    @property
    def ordered_outcomes(self) -> tuple[EconomicPerformanceOutcome, ...]:
        return tuple(sorted(self.outcomes, key=lambda o: o.observed_at))

    @property
    def latest_outcome(self) -> EconomicPerformanceOutcome | None:
        if not self.outcomes:
            return None
        return self.ordered_outcomes[-1]
