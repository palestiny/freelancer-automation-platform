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

    existing_by_id = exposure_repository.get(exposure_id)
    if existing_by_id is not None:
        if (
            existing_by_id.assignment_id == assignment.id
            and existing_by_id.experiment_id == assignment.experiment_id
            and existing_by_id.subject_id == assignment.subject_id
            and existing_by_id.variant == assignment.variant
            and existing_by_id.exposed_at == exposed_at
        ):
            return existing_by_id
        raise ValueError(f"exposure_id {exposure_id!r} conflicts with existing exposure")

    existing_by_assignment = exposure_repository.get_by_assignment(assignment.id)
    if existing_by_assignment is not None:
        raise ValueError(
            f"assignment_id {assignment.id!r} already has exposure "
            f"{existing_by_assignment.id!r}"
        )

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
