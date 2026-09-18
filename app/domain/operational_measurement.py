from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class WorkOutcome(str, Enum):
    SUCCEEDED = "succeeded"
    PARTIALLY_SUCCEEDED = "partially_succeeded"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ImprovementHandoff(str, Enum):
    POLICY_REVIEW = "policy_review"
    EXPERIMENT = "experiment"


@dataclass(frozen=True)
class WorkItemOutcomeObservation:
    id: str
    business_id: str
    work_item_id: str
    observed_at: datetime
    outcome: WorkOutcome
    evidence_quality: int = 50

    def __post_init__(self) -> None:
        for name in ("id", "business_id", "work_item_id"):
            if not getattr(self, name).strip():
                raise ValueError(f"{name} cannot be empty")

        if not isinstance(self.evidence_quality, int) or isinstance(
            self.evidence_quality, bool
        ):
            raise TypeError("evidence_quality must be an integer")
        if not 0 <= self.evidence_quality <= 100:
            raise ValueError("evidence_quality must be between 0 and 100")


@dataclass(frozen=True)
class OperationalMeasurement:
    id: str
    business_id: str
    metric_name: str
    unit: str
    expected_value: float
    actual_value: float
    measured_at: datetime

    def __post_init__(self) -> None:
        for name in ("id", "business_id", "metric_name", "unit"):
            if not getattr(self, name).strip():
                raise ValueError(f"{name} cannot be empty")

        for name in ("expected_value", "actual_value"):
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise TypeError(f"{name} must be numeric")

    @property
    def variance(self) -> float:
        return self.actual_value - self.expected_value

    @property
    def relative_variance(self) -> float | None:
        if self.expected_value == 0:
            return None
        return self.variance / self.expected_value


@dataclass(frozen=True)
class BusinessPerformanceSnapshot:
    id: str
    business_id: str
    period_start: datetime
    period_end: datetime
    measurements: tuple[OperationalMeasurement, ...] = ()

    def __post_init__(self) -> None:
        for name in ("id", "business_id"):
            if not getattr(self, name).strip():
                raise ValueError(f"{name} cannot be empty")

        if self.period_end <= self.period_start:
            raise ValueError("period_end must be after period_start")

        for measurement in self.measurements:
            if measurement.business_id != self.business_id:
                raise ValueError("all measurements must belong to the snapshot business")


@dataclass(frozen=True)
class LearningSignal:
    id: str
    business_id: str
    source_measurement_id: str
    statement: str
    evidence_quality: int = 50

    def __post_init__(self) -> None:
        for name in ("id", "business_id", "source_measurement_id", "statement"):
            if not getattr(self, name).strip():
                raise ValueError(f"{name} cannot be empty")

        if not isinstance(self.evidence_quality, int) or isinstance(
            self.evidence_quality, bool
        ):
            raise TypeError("evidence_quality must be an integer")
        if not 0 <= self.evidence_quality <= 100:
            raise ValueError("evidence_quality must be between 0 and 100")


@dataclass(frozen=True)
class ImprovementRecommendation:
    id: str
    business_id: str
    learning_signal_id: str
    statement: str
    handoff: ImprovementHandoff

    def __post_init__(self) -> None:
        for name in ("id", "business_id", "learning_signal_id", "statement"):
            if not getattr(self, name).strip():
                raise ValueError(f"{name} cannot be empty")
