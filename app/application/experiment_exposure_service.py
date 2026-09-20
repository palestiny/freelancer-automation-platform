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
    if exposed_at < assignment.assigned_at:
        raise ValueError("exposed_at cannot be before assigned_at")
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


from app.application.ports.experiment_assignment_repository import ExperimentAssignmentRepository


def record_persisted_experiment_exposure(
    *,
    assignment_repository: ExperimentAssignmentRepository,
    exposure_repository: ExperimentExposureRepository,
    assignment_id: str,
    exposure_id: str,
    exposed_at: datetime,
) -> ExperimentExposure:
    if not assignment_id.strip():
        raise ValueError("assignment_id cannot be empty")
    if not exposure_id.strip():
        raise ValueError("exposure_id cannot be empty")

    assignment = assignment_repository.get(assignment_id)
    if assignment is None:
        raise ValueError(f"assignment {assignment_id!r} does not exist")
    if exposed_at < assignment.assigned_at:
        raise ValueError("exposed_at cannot be before assigned_at")

    exposure = ExperimentExposure(
        id=exposure_id,
        assignment_id=assignment.id,
        experiment_id=assignment.experiment_id,
        subject_id=assignment.subject_id,
        variant=assignment.variant,
        exposed_at=exposed_at,
    )
    exposure_repository.save(exposure)
    return exposure
