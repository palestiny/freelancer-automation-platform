from typing import Protocol, runtime_checkable

from app.domain.controlled_experiment_evidence import ExperimentExposure


@runtime_checkable
class ExperimentExposureRepository(Protocol):
    def save(self, exposure: ExperimentExposure) -> None:
        ...

    def get(self, exposure_id: str) -> ExperimentExposure | None:
        ...

    def get_by_assignment(self, assignment_id: str) -> ExperimentExposure | None:
        ...
