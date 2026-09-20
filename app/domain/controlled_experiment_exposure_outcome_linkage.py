from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class ExposureOutcomeLinkage:
    linkage_id: str
    experiment_id: str
    assignment_id: str
    exposure_id: str
    subject_id: str
    variant_id: str
    outcome_observation_id: str
    exposed_at: datetime
    observed_at: datetime

    def __post_init__(self) -> None:
        for name in (
            "linkage_id",
            "experiment_id",
            "assignment_id",
            "exposure_id",
            "subject_id",
            "variant_id",
            "outcome_observation_id",
        ):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} cannot be empty")

        for name in ("exposed_at", "observed_at"):
            value = getattr(self, name)
            if value.tzinfo is None or value.utcoffset() is None:
                raise ValueError(f"{name} must be timezone-aware")

        if self.observed_at < self.exposed_at:
            raise ValueError("observed_at cannot precede exposed_at")
