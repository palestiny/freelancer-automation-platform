from datetime import datetime, timezone

from app.application.performance_observation_service import (
    PerformanceObservationService,
)
from app.domain.business_performance import (
    BusinessPerformanceObservation,
    PerformanceSourceType,
)


class FakeRepository:
    def __init__(self):
        self.saved = []
        self.by_business = {}

    def save(self, observation):
        self.saved.append(observation)

    def get(self, observation_id):
        return next((x for x in self.saved if x.id == observation_id), None)

    def list_by_business(self, business_id):
        return tuple(x for x in self.saved if x.business_id == business_id)


def _observation():
    return BusinessPerformanceObservation(
        id="obs-1",
        business_id="biz-1",
        source_type=PerformanceSourceType.OPERATIONAL,
        source_id="work-1",
        metric_name="profit",
        unit="EGP",
        expected_value=100,
        actual_value=120,
        observed_at=datetime(2026, 9, 20, tzinfo=timezone.utc),
        evidence_quality=80,
    )


def test_record_delegates_authoritative_observation_to_repository():
    repository = FakeRepository()
    service = PerformanceObservationService(repository)

    observation = _observation()
    service.record(observation)

    assert repository.saved == [observation]


def test_history_reads_only_from_repository_boundary():
    repository = FakeRepository()
    service = PerformanceObservationService(repository)

    observation = _observation()
    repository.save(observation)

    assert service.history("biz-1") == (observation,)
