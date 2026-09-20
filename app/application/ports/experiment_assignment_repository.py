from typing import Protocol, runtime_checkable

from app.domain.controlled_experiment_evidence import ExperimentAssignment


@runtime_checkable
class ExperimentAssignmentRepository(Protocol):
    def save(self, assignment: ExperimentAssignment) -> None:
        ...

    def get(self, assignment_id: str) -> ExperimentAssignment | None:
        ...

    def list_by_experiment(self, experiment_id: str) -> tuple[ExperimentAssignment, ...]:
        ...
