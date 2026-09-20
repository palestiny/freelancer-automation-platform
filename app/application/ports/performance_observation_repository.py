from typing import Protocol

from app.domain.business_performance import BusinessPerformanceObservation


class PerformanceObservationRepository(Protocol):
    def save(self, observation: BusinessPerformanceObservation) -> None:
        ...

    def get(self, observation_id: str) -> BusinessPerformanceObservation | None:
        ...

    def list_by_business(
        self,
        business_id: str,
    ) -> tuple[BusinessPerformanceObservation, ...]:
        ...
