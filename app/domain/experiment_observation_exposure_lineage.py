from dataclasses import dataclass
from enum import Enum

from .controlled_experiment_evidence import ExperimentExposure, ExperimentObservation


class ExposureLineageStatus(str, Enum):
    VALID = "valid"
    INVALID_CONTEXT = "invalid_context"
    BEFORE_EXPOSURE = "before_exposure"


@dataclass(frozen=True)
class ExposureLineageValidation:
    status: ExposureLineageStatus
    observation_id: str
    exposure_id: str

    def __post_init__(self) -> None:
        if not self.observation_id.strip() or not self.exposure_id.strip():
            raise ValueError("observation_id and exposure_id cannot be empty")

    @property
    def valid(self) -> bool:
        return self.status is ExposureLineageStatus.VALID


def validate_observation_exposure_lineage(
    *,
    observation: ExperimentObservation,
    exposure: ExperimentExposure,
) -> ExposureLineageValidation:
    if (
        observation.experiment_id != exposure.experiment_id
        or observation.assignment_id != exposure.assignment_id
        or observation.subject_id != exposure.subject_id
        or observation.variant != exposure.variant
    ):
        return ExposureLineageValidation(status=ExposureLineageStatus.INVALID_CONTEXT, observation_id=observation.id, exposure_id=exposure.id)

    if observation.observed_at < exposure.exposed_at:
        return ExposureLineageValidation(status=ExposureLineageStatus.BEFORE_EXPOSURE, observation_id=observation.id, exposure_id=exposure.id)

    return ExposureLineageValidation(status=ExposureLineageStatus.VALID, observation_id=observation.id, exposure_id=exposure.id)
