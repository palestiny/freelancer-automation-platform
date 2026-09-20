from datetime import datetime

from app.application.ports.experiment_exposure_repository import ExperimentExposureRepository
from app.domain.controlled_experiment_evidence import ExperimentAssignment, ExperimentExposure


def record_experiment_exposure(
    *,
    repository: ExperimentExposureRepository,
    assignment: ExperimentAssignment,
    exposure_id: str,
    exposed_at: datetime,
) -> ExperimentExposure:
    if not exposure_id.strip():
        raise ValueError("exposure_id cannot be empty")
    exposure = ExperimentExposure(
        id=exposure_id,
        assignment_id=assignment.id,
        experiment_id=assignment.experiment_id,
        subject_id=assignment.subject_id,
        variant=assignment.variant,
        exposed_at=exposed_at,
    )
    repository.save(exposure)
    return exposure
