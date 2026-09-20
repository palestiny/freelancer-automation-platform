from datetime import datetime, timezone

import pytest

from app.domain.business_performance import (
    BusinessPerformanceObservation,
    PerformanceSourceType,
)
from app.infrastructure.performance_observation_repository import (
    SQLitePerformanceObservationRepository,
)


def _observation(*, id="obs-1", business_id="biz-1", expected=100.0):
    return BusinessPerformanceObservation(
        id=id,
        business_id=business_id,
        source_type=PerformanceSourceType.OPERATIONAL,
        source_id="work-1",
        metric_name="profit",
        unit="EGP",
        expected_value=expected,
        actual_value=120.0,
        observed_at=datetime(2026, 9, 20, tzinfo=timezone.utc),
        evidence_quality=77,
    )


def test_round_trip_preserves_authoritative_observation():
    repository = SQLitePerformanceObservationRepository(":memory:")
    observation = _observation()

    repository.save(observation)

    assert repository.get("obs-1") == observation


def test_duplicate_observation_id_is_rejected():
    repository = SQLitePerformanceObservationRepository(":memory:")
    repository.save(_observation())

    with pytest.raises(ValueError, match="already exists"):
        repository.save(_observation())


def test_list_by_business_isolation_is_explicit():
    repository = SQLitePerformanceObservationRepository(":memory:")
    repository.save(_observation(id="obs-1", business_id="biz-1"))
    repository.save(_observation(id="obs-2", business_id="biz-2"))

    result = repository.list_by_business("biz-1")

    assert result == (_observation(id="obs-1", business_id="biz-1"),)


def test_nullable_expected_value_is_preserved():
    repository = SQLitePerformanceObservationRepository(":memory:")
    observation = _observation(expected=None)

    repository.save(observation)

    assert repository.get("obs-1").expected_value is None


def test_get_missing_observation_returns_none():
    repository = SQLitePerformanceObservationRepository(":memory:")

    assert repository.get("missing") is None
