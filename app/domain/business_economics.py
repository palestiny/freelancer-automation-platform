from dataclasses import dataclass
from math import isfinite


@dataclass(frozen=True)
class EconomicEstimate:
    """Derived economic assessment for an opportunity.

    Values are estimates, not guaranteed outcomes. The estimate is deliberately
    independent from Opportunity so economics can be recalculated without
    mutating opportunity identity.
    """

    expected_revenue: float
    expected_effort_hours: float
    platform_fee: float = 0.0
    capability_cost: float = 0.0
    operating_cost: float = 0.0
    revision_allowance: float = 0.0
    success_confidence: float = 1.0

    def __post_init__(self) -> None:
        if not isfinite(self.expected_revenue):
            raise ValueError("expected_revenue must be finite")
        if self.expected_revenue < 0:
            raise ValueError("expected_revenue cannot be negative")
        if not isfinite(self.expected_effort_hours):
            raise ValueError("expected_effort_hours must be finite")
        if self.expected_effort_hours <= 0:
            raise ValueError("expected_effort_hours must be greater than zero")
        if self.platform_fee < 0:
            raise ValueError("platform_fee cannot be negative")
        if self.capability_cost < 0:
            raise ValueError("capability_cost cannot be negative")
        if self.operating_cost < 0:
            raise ValueError("operating_cost cannot be negative")
        if self.revision_allowance < 0:
            raise ValueError("revision_allowance cannot be negative")
        if not isfinite(self.success_confidence):
            raise ValueError("success_confidence must be finite")
        if not 0 <= self.success_confidence <= 1:
            raise ValueError("success_confidence must be between 0 and 1")

    @property
    def expected_cost(self) -> float:
        return (
            self.platform_fee
            + self.capability_cost
            + self.operating_cost
            + self.revision_allowance
        )

    @property
    def expected_profit(self) -> float:
        return self.expected_revenue - self.expected_cost

    @property
    def expected_margin(self) -> float | None:
        if self.expected_revenue == 0:
            return None
        return self.expected_profit / self.expected_revenue

    @property
    def expected_profit_per_hour(self) -> float:
        return self.expected_profit / self.expected_effort_hours

    @property
    def risk_adjusted_profit(self) -> float:
        return self.expected_profit * self.success_confidence
