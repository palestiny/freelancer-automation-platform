from app.application.ports.experiment_exposure_repository import ExperimentExposureRepository
from app.application.ports.experiment_observation_repository import ExperimentObservationRepository
from app.domain.controlled_experiment_evidence import ExperimentObservation
from app.domain.experiment_observation_exposure_lineage import (
    ExposureLineageStatus,
    validate_observation_exposure_lineage,
)


def record_experiment_observation(
    *,
    repository: ExperimentObservationRepository,
    exposure_repository: ExperimentExposureRepository,
    observation: ExperimentObservation,
) -> ExperimentObservation:
    exposure = exposure_repository.get_by_assignment(observation.assignment_id)
    if exposure is None:
        raise ValueError(
            f"no exposure exists for assignment {observation.assignment_id!r}"
        )

    lineage = validate_observation_exposure_lineage(
        observation=observation,
        exposure=exposure,
    )
    if lineage.status is not ExposureLineageStatus.VALID:
        raise ValueError(
            f"observation {observation.id!r} has invalid exposure lineage: "
            f"{lineage.status.value}"
        )

    repository.save(observation)
    return observation
