from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class PerformanceSourceType(str, Enum):
    OPERATIONAL = "operational"
    REVENUE = "revenue"
    CAMPAIGN = "campaign"


@dataclass(frozen=True)
class BusinessPerformanceObservation:
    """Normalized business performance evidence from a bounded source."""

    id: str
    business_id: str
    source_type: PerformanceSourceType
    source_id: str
    metric_name: str
    unit: str
    expected_value: float | None
    actual_value: float
    observed_at: datetime
    evidence_quality: int = 50

    def __post_init__(self) -> None:
        for name in (
            "id",
            "business_id",
            "source_id",
            "metric_name",
            "unit",
        ):
            if not getattr(self, name).strip():
                raise ValueError(f"{name} cannot be empty")

        if self.expected_value is not None and (
            isinstance(self.expected_value, bool)
            or not isinstance(self.expected_value, (int, float))
        ):
            raise TypeError("expected_value must be numeric or None")

        if isinstance(self.actual_value, bool) or not isinstance(
            self.actual_value, (int, float)
        ):
            raise TypeError("actual_value must be numeric")

        if not isinstance(self.observed_at, datetime):
            raise TypeError("observed_at must be a datetime")
        if self.observed_at.tzinfo is None or self.observed_at.utcoffset() is None:
            raise ValueError("observed_at must be timezone-aware")

        if not isinstance(self.evidence_quality, int) or isinstance(
            self.evidence_quality, bool
        ):
            raise TypeError("evidence_quality must be an integer")
        if not 0 <= self.evidence_quality <= 100:
            raise ValueError("evidence_quality must be between 0 and 100")

    @property
    def variance(self) -> float | None:
        if self.expected_value is None:
            return None
        return self.actual_value - self.expected_value

    @property
    def relative_variance(self) -> float | None:
        if self.expected_value in (None, 0):
            return None
        return self.variance / self.expected_value


@dataclass(frozen=True)
class BusinessPerformanceHistory:
    """Chronological performance observations for exactly one business."""

    business_id: str
    observations: tuple[BusinessPerformanceObservation, ...] = ()

    def __post_init__(self) -> None:
        if not self.business_id.strip():
            raise ValueError("business_id cannot be empty")

        if any(
            observation.business_id != self.business_id
            for observation in self.observations
        ):
            raise ValueError(
                "all observations must belong to the history business"
            )

    @property
    def ordered_observations(
        self,
    ) -> tuple[BusinessPerformanceObservation, ...]:
        return tuple(
            sorted(self.observations, key=lambda observation: observation.observed_at)
        )

    def for_metric(
        self,
        metric_name: str,
        unit: str,
    ) -> tuple[BusinessPerformanceObservation, ...]:
        if not metric_name.strip() or not unit.strip():
            raise ValueError("metric_name and unit cannot be empty")

        return tuple(
            observation
            for observation in self.ordered_observations
            if observation.metric_name == metric_name and observation.unit == unit
        )

    @property
    def latest_observation(self) -> BusinessPerformanceObservation | None:
        if not self.observations:
            return None
        return self.ordered_observations[-1]
