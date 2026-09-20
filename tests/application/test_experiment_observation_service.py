from datetime import datetime, timezone

import pytest

from app.application.experiment_observation_service import record_experiment_observation
from app.domain.controlled_experiment_evidence import ExperimentAssignment, ExperimentExposure, ExperimentObservation


class FakeExposureRepository:
    def __init__(self, exposure):
        self.exposure = exposure

    def get_by_assignment(self, assignment_id):
        if self.exposure.assignment_id == assignment_id:
            return self.exposure
        return None


class FakeObservationRepository:
    def __init__(self):
        self.items = {}

    def save(self, observation):
        self.items[observation.id] = observation

    def get(self, observation_id):
        return self.items.get(observation_id)

    def list_by_experiment(self, experiment_id):
        return tuple(
            item for item in self.items.values() if item.experiment_id == experiment_id
        )


def _observation():
    assigned_at = datetime(2026, 1, 1, tzinfo=timezone.utc)
    exposed_at = datetime(2026, 1, 2, tzinfo=timezone.utc)
    observed_at = datetime(2026, 1, 3, tzinfo=timezone.utc)
    return (
        ExperimentAssignment("a1", "e1", "s1", "A", assigned_at),
        ExperimentExposure("x1", "a1", "e1", "s1", "A", exposed_at),
        ExperimentObservation("o1", "e1", "a1", "s1", "A", "revenue", 120.0, observed_at, 80),
    )


def test_identical_observation_retry_returns_authoritative_observation():
    _, exposure, observation = _observation()
    exposures = FakeExposureRepository(exposure)
    observations = FakeObservationRepository()

    first = record_experiment_observation(
        repository=observations,
        exposure_repository=exposures,
        observation=observation,
    )
    retry = record_experiment_observation(
        repository=observations,
        exposure_repository=exposures,
        observation=observation,
    )

    assert retry == first
    assert observations.items == {"o1": observation}


def test_conflicting_observation_id_is_rejected():
    _, exposure, observation = _observation()
    exposures = FakeExposureRepository(exposure)
    observations = FakeObservationRepository()
    record_experiment_observation(
        repository=observations,
        exposure_repository=exposures,
        observation=observation,
    )

    conflicting = ExperimentObservation(
        "o1", "e1", "a1", "s1", "A", "revenue", 999.0,
        observation.observed_at, 80,
    )

    with pytest.raises(ValueError, match="conflicts with existing observation"):
        record_experiment_observation(
            repository=observations,
            exposure_repository=exposures,
            observation=conflicting,
        )
