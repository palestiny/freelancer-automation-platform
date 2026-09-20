from app.application.ports.performance_observation_repository import (
    PerformanceObservationRepository,
)
from app.infrastructure.performance_observation_repository import (
    SQLitePerformanceObservationRepository,
)


def test_sqlite_repository_conforms_to_application_port():
    repository = SQLitePerformanceObservationRepository(":memory:")
    assert isinstance(repository, PerformanceObservationRepository)
