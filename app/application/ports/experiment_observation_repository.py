from typing import Protocol, runtime_checkable

from app.domain.controlled_experiment_evidence import ExperimentObservation


@runtime_checkable
class ExperimentObservationRepository(Protocol):
    def save(self, observation: ExperimentObservation) -> None:
        ...

    def get(self, observation_id: str) -> ExperimentObservation | None:
        ...

    def list_by_experiment(
        self,
        experiment_id: str,
    ) -> tuple[ExperimentObservation, ...]:
        ...
