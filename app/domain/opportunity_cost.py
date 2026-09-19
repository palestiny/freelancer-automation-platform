from dataclasses import dataclass
import math


@dataclass(frozen=True)
class OpportunityCostEvidence:
    quantity: float
    selected_expected_profit: float
    alternative_expected_profit: float
    opportunity_cost: float

    def __post_init__(self) -> None:
        if not math.isfinite(self.quantity) or self.quantity <= 0:
            raise ValueError("quantity must be positive and finite")
        for name, value in (
            ("selected_expected_profit", self.selected_expected_profit),
            ("alternative_expected_profit", self.alternative_expected_profit),
            ("opportunity_cost", self.opportunity_cost),
        ):
            if not math.isfinite(value):
                raise ValueError(f"{name} must be finite")
        if self.opportunity_cost < 0:
            raise ValueError("opportunity_cost cannot be negative")


def calculate_opportunity_cost(
    *,
    quantity: float,
    selected_expected_profit: float,
    alternative_expected_profit: float,
) -> OpportunityCostEvidence:
    if not math.isfinite(quantity) or quantity <= 0:
        raise ValueError("quantity must be positive and finite")
    if not math.isfinite(selected_expected_profit):
        raise ValueError("selected_expected_profit must be finite")
    if not math.isfinite(alternative_expected_profit):
        raise ValueError("alternative_expected_profit must be finite")

    opportunity_cost = max(
        0.0,
        alternative_expected_profit - selected_expected_profit,
    )
    return OpportunityCostEvidence(
        quantity=quantity,
        selected_expected_profit=selected_expected_profit,
        alternative_expected_profit=alternative_expected_profit,
        opportunity_cost=opportunity_cost,
    )
