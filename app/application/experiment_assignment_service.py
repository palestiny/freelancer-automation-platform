from datetime import datetime

from app.application.ports.experiment_assignment_repository import ExperimentAssignmentRepository
from app.domain.controlled_experiment_allocation import ExperimentAllocationDecision
from app.domain.controlled_experiment_evidence import ExperimentAssignment


def persist_experiment_assignment(
    *,
    repository: ExperimentAssignmentRepository,
    decision: ExperimentAllocationDecision,
    assignment_id: str,
    assigned_at: datetime,
) -> ExperimentAssignment:
    if not assignment_id.strip():
        raise ValueError("assignment_id cannot be empty")

    assignment = ExperimentAssignment(
        id=assignment_id,
        experiment_id=decision.experiment_id,
        subject_id=decision.subject_id,
        variant=decision.variant,
        assigned_at=assigned_at,
    )
    repository.save(assignment)
    return assignment
