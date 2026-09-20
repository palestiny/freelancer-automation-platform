from datetime import datetime, timezone

import pytest

from app.application.experiment_exposure_service import record_experiment_exposure
from app.application.ports.experiment_exposure_repository import ExperimentExposureRepository
from app.domain.controlled_experiment_evidence import ExperimentAssignment, ExperimentExposure
from app.infrastructure.experiment_exposure_repository import SQLiteExperimentExposureRepository


def _assignment():
    return ExperimentAssignment(
        id="assignment-1",
        experiment_id="exp-1",
        subject_id="subject-1",
        variant="A",
        assigned_at=datetime(2026, 9, 20, tzinfo=timezone.utc),
    )


def _exposure():
    return ExperimentExposure(
        id="exposure-1",
        assignment_id="assignment-1",
        experiment_id="exp-1",
        subject_id="subject-1",
        variant="A",
        exposed_at=datetime(2026, 9, 20, 1, tzinfo=timezone.utc),
    )


def test_repository_conforms_to_port():
    repository = SQLiteExperimentExposureRepository(":memory:")
    assert isinstance(repository, ExperimentExposureRepository)
    repository.close()


def test_save_get_and_list_by_assignment():
    repository = SQLiteExperimentExposureRepository(":memory:")
    exposure = _exposure()
    repository.save(exposure)

    assert repository.get(exposure.id) == exposure
    assert repository.get_by_assignment(exposure.assignment_id) == exposure
    repository.close()


def test_duplicate_exposure_identity_is_rejected():
    repository = SQLiteExperimentExposureRepository(":memory:")
    exposure = _exposure()
    repository.save(exposure)

    with pytest.raises(ValueError, match="exposure .* already exists"):
        repository.save(exposure)
    repository.close()


def test_second_exposure_for_assignment_is_rejected():
    repository = SQLiteExperimentExposureRepository(":memory:")
    repository.save(_exposure())
    conflicting = ExperimentExposure(
        id="exposure-2",
        assignment_id="assignment-1",
        experiment_id="exp-1",
        subject_id="subject-1",
        variant="A",
        exposed_at=datetime(2026, 9, 20, 2, tzinfo=timezone.utc),
    )

    with pytest.raises(ValueError, match="assignment .* already has exposure"):
        repository.save(conflicting)
    repository.close()


def test_record_exposure_preserves_assignment_context():
    repository = SQLiteExperimentExposureRepository(":memory:")
    exposure = record_experiment_exposure(
        repository=repository,
        assignment=_assignment(),
        exposure_id="exposure-1",
        exposed_at=datetime(2026, 9, 20, 1, tzinfo=timezone.utc),
    )

    assert exposure.assignment_id == "assignment-1"
    assert exposure.variant == "A"
    assert repository.get_by_assignment("assignment-1") == exposure
    repository.close()


def test_record_exposure_rejects_empty_identity():
    repository = SQLiteExperimentExposureRepository(":memory:")

    with pytest.raises(ValueError, match="exposure_id cannot be empty"):
        record_experiment_exposure(
            repository=repository,
            assignment=_assignment(),
            exposure_id="",
            exposed_at=datetime(2026, 9, 20, tzinfo=timezone.utc),
        )
    repository.close()
