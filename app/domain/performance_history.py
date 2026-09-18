from dataclasses import dataclass
from datetime import datetime, timedelta

from .business_performance import BusinessPerformanceHistory, BusinessPerformanceObservation


@dataclass(frozen=True)
class PerformanceWindow:
    start: datetime
    end: datetime

    def __post_init__(self) -> None:
        if self.end <= self.start:
            raise ValueError("end must be after start")

    def contains(self, observed_at: datetime) -> bool:
        return self.start <= observed_at < self.end


def observations_in_window(
    history: BusinessPerformanceHistory,
    window: PerformanceWindow,
) -> tuple[BusinessPerformanceObservation, ...]:
    return tuple(
        observation
        for observation in history.ordered_observations
        if window.contains(observation.observed_at)
    )


def rolling_window(
    *,
    end: datetime,
    duration: timedelta,
) -> PerformanceWindow:
    if duration <= timedelta(0):
        raise ValueError("duration must be greater than zero")
    return PerformanceWindow(start=end - duration, end=end)
