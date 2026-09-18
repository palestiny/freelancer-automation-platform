from dataclasses import dataclass
from enum import Enum


class ResourceKind(str, Enum):
    HUMAN_TIME = "human_time"
    CAPABILITY_USAGE = "capability_usage"
    INFRASTRUCTURE = "infrastructure"
    COMMUNICATION = "communication"
    MARKETPLACE_FEE = "marketplace_fee"
    REVIEW_TIME = "review_time"


@dataclass(frozen=True)
class ResourceUsage:
    """A measurable consumption of a resource with monetary unit cost."""

    kind: ResourceKind
    quantity: float
    unit_cost: float

    def __post_init__(self) -> None:
        if self.quantity < 0:
            raise ValueError("quantity cannot be negative")
        if self.unit_cost < 0:
            raise ValueError("unit_cost cannot be negative")

    @property
    def total_cost(self) -> float:
        return self.quantity * self.unit_cost
