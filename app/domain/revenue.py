from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class RevenueType(Enum):
    ONE_TIME = "ONE_TIME"
    RECURRING = "RECURRING"


class RecurringPeriod(Enum):
    WEEKLY = "WEEKLY"
    MONTHLY = "MONTHLY"
    QUARTERLY = "QUARTERLY"
    YEARLY = "YEARLY"


class RevenueContractStatus(Enum):
    PROPOSED = "PROPOSED"
    ACTIVE = "ACTIVE"
    PAUSED = "PAUSED"
    ENDED = "ENDED"


@dataclass(frozen=True)
class RevenueContract:
    id: str
    model_id: str
    revenue_type: RevenueType
    amount: float
    currency: str
    recurring_period: RecurringPeriod | None = None
    status: RevenueContractStatus = RevenueContractStatus.PROPOSED

    def __post_init__(self) -> None:
        for field_name in ("id", "model_id", "currency"):
            if not getattr(self, field_name).strip():
                raise ValueError(f"{field_name} cannot be empty")

        if self.amount < 0:
            raise ValueError("amount cannot be negative")

        if self.revenue_type is RevenueType.RECURRING and self.recurring_period is None:
            raise ValueError("recurring revenue requires a recurring_period")

        if self.revenue_type is RevenueType.ONE_TIME and self.recurring_period is not None:
            raise ValueError("one-time revenue cannot have a recurring_period")


@dataclass(frozen=True)
class RevenueEvent:
    contract_id: str
    amount: float
    currency: str
    recognized_at: datetime

    def __post_init__(self) -> None:
        if not self.contract_id.strip():
            raise ValueError("contract_id cannot be empty")

        if self.amount < 0:
            raise ValueError("amount cannot be negative")

        if not self.currency.strip():
            raise ValueError("currency cannot be empty")
