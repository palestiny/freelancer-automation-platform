from app.application.ports.performance_observation_repository import (
    PerformanceObservationRepository,
)
from app.domain.business_performance import BusinessPerformanceObservation


class PerformanceObservationService:
    def __init__(self, repository: PerformanceObservationRepository) -> None:
        self._repository = repository

    def record(self, observation: BusinessPerformanceObservation) -> None:
        self._repository.save(observation)

    def history(
        self,
        business_id: str,
    ) -> tuple[BusinessPerformanceObservation, ...]:
        if not business_id.strip():
            raise ValueError("business_id cannot be empty")
        return self._repository.list_by_business(business_id)
