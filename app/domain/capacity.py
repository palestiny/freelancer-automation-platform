from dataclasses import dataclass
from datetime import datetime
from math import isfinite


@dataclass(frozen=True)
class CapacitySnapshot:
    """Human-time capacity for a defined planning period."""

    period_start: datetime
    period_end: datetime
    total_hours: float
    committed_hours: float = 0.0
    reserved_hours: float = 0.0

    def __post_init__(self) -> None:
        for name in ("total_hours", "committed_hours", "reserved_hours"):
            if not isfinite(getattr(self, name)):
                raise ValueError(f"{name} must be finite")
        if self.period_end <= self.period_start:
            raise ValueError("period_end must be after period_start")
        if self.total_hours <= 0:
            raise ValueError("total_hours must be greater than zero")
        if self.committed_hours < 0:
            raise ValueError("committed_hours cannot be negative")
        if self.reserved_hours < 0:
            raise ValueError("reserved_hours cannot be negative")
        if self.committed_hours + self.reserved_hours > self.total_hours:
            raise ValueError(
                "committed_hours plus reserved_hours cannot exceed total_hours"
            )

    @property
    def remaining_hours(self) -> float:
        return self.total_hours - self.committed_hours - self.reserved_hours

    @property
    def utilization(self) -> float:
        return (self.committed_hours + self.reserved_hours) / self.total_hours
