from datetime import datetime, timezone

import pytest

from app.application.experiment_observation_service import record_experiment_observation
from app.application.ports.experiment_exposure_repository import ExperimentExposureRepository
from app.application.ports.experiment_observation_repository import ExperimentObservationRepository
from app.domain.controlled_experiment_evidence import ExperimentAssignment, ExperimentExposure, ExperimentObservation
from app.infrastructure.experiment_exposure_repository import SQLiteExperimentExposureRepository
from app.infrastructure.experiment_observation_repository import SQLiteExperimentObservationRepository


def _assignment():
    return ExperimentAssignment(
        id="assignment-1",
        experiment_id="exp-1",
        subject_id="subject-1",
        variant="A",
        assigned_at=datetime(2026, 9, 20, 10, tzinfo=timezone.utc),
    )


def _exposure():
    return ExperimentExposure(
        id="exposure-1",
        assignment_id="assignment-1",
        experiment_id="exp-1",
        subject_id="subject-1",
        variant="A",
        exposed_at=datetime(2026, 9, 20, 11, tzinfo=timezone.utc),
    )


def _observation(**overrides):
    values = dict(
        id="observation-1",
        experiment_id="exp-1",
        assignment_id="assignment-1",
        subject_id="subject-1",
        variant="A",
        metric_name="conversion",
        observed_value=1.0,
        observed_at=datetime(2026, 9, 20, 12, tzinfo=timezone.utc),
        evidence_quality=80,
    )
    values.update(overrides)
    return ExperimentObservation(**values)


def _repositories():
    return (
        SQLiteExperimentObservationRepository(":memory:"),
        SQLiteExperimentExposureRepository(":memory:"),
    )


def test_repository_conforms_to_port():
    observations, exposures = _repositories()
    assert isinstance(observations, ExperimentObservationRepository)
    assert isinstance(exposures, ExperimentExposureRepository)
    observations.close()
    exposures.close()


def test_observation_is_persisted_only_after_matching_exposure():
    observations, exposures = _repositories()
    exposures.save(_exposure())

    saved = record_experiment_observation(
        repository=observations,
        exposure_repository=exposures,
        observation=_observation(),
    )

    assert saved == _observation()
    assert observations.get(saved.id) == saved
    observations.close()
    exposures.close()


def test_missing_exposure_blocks_observation():
    observations, exposures = _repositories()

    with pytest.raises(ValueError, match="no exposure exists"):
        record_experiment_observation(
            repository=observations,
            exposure_repository=exposures,
            observation=_observation(),
        )

    observations.close()
    exposures.close()


def test_observation_before_exposure_blocks_persistence():
    observations, exposures = _repositories()
    exposures.save(_exposure())

    with pytest.raises(ValueError, match="before_exposure"):
        record_experiment_observation(
            repository=observations,
            exposure_repository=exposures,
            observation=_observation(
                observed_at=datetime(2026, 9, 20, 10, 30, tzinfo=timezone.utc)
            ),
        )

    assert observations.get("observation-1") is None
    observations.close()
    exposures.close()


def test_context_mismatch_blocks_persistence():
    observations, exposures = _repositories()
    exposures.save(_exposure())

    with pytest.raises(ValueError, match="invalid_context"):
        record_experiment_observation(
            repository=observations,
            exposure_repository=exposures,
            observation=_observation(variant="B"),
        )

    assert observations.get("observation-1") is None
    observations.close()
    exposures.close()


def test_duplicate_observation_identity_is_rejected():
    observations, exposures = _repositories()
    exposures.save(_exposure())
    observations.save(_observation())

    with pytest.raises(ValueError, match="observation .* already exists"):
        observations.save(_observation())

    observations.close()
    exposures.close()


def test_list_by_experiment_is_chronological():
    observations, exposures = _repositories()
    exposures.save(_exposure())
    observations.save(
        _observation(
            id="observation-2",
            observed_at=datetime(2026, 9, 20, 14, tzinfo=timezone.utc),
        )
    )
    observations.save(_observation())

    assert tuple(o.id for o in observations.list_by_experiment("exp-1")) == (
        "observation-1",
        "observation-2",
    )
    observations.close()
    exposures.close()
