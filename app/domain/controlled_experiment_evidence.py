from dataclasses import dataclass
from datetime import datetime
import math


@dataclass(frozen=True)
class ExperimentAssignment:
    id: str
    experiment_id: str
    subject_id: str
    variant: str
    assigned_at: datetime

    def __post_init__(self) -> None:
        for name in ("id", "experiment_id", "subject_id", "variant"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} cannot be empty")
        if self.assigned_at.tzinfo is None or self.assigned_at.utcoffset() is None:
            raise ValueError("assigned_at must be timezone-aware")


@dataclass(frozen=True)
class ExperimentObservation:
    id: str
    experiment_id: str
    assignment_id: str
    subject_id: str
    variant: str
    metric_name: str
    observed_value: float
    observed_at: datetime
    evidence_quality: int = 50

    def __post_init__(self) -> None:
        for name in (
            "id",
            "experiment_id",
            "assignment_id",
            "subject_id",
            "variant",
            "metric_name",
        ):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} cannot be empty")

        if isinstance(self.observed_value, bool) or not isinstance(
            self.observed_value, (int, float)
        ):
            raise TypeError("observed_value must be numeric")
        if not math.isfinite(float(self.observed_value)):
            raise ValueError("observed_value must be finite")

        if self.observed_at.tzinfo is None or self.observed_at.utcoffset() is None:
            raise ValueError("observed_at must be timezone-aware")

        if not isinstance(self.evidence_quality, int) or isinstance(
            self.evidence_quality, bool
        ):
            raise TypeError("evidence_quality must be an integer")
        if not 0 <= self.evidence_quality <= 100:
            raise ValueError("evidence_quality must be between 0 and 100")
