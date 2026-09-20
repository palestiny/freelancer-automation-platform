from datetime import datetime, timezone

import pytest

from app.application.experiment_exposure_service import record_persisted_experiment_exposure
from app.domain.controlled_experiment_evidence import ExperimentAssignment, ExperimentExposure


class AssignmentRepo:
    def __init__(self, assignment):
        self.assignment = assignment

    def get(self, assignment_id):
        return self.assignment if assignment_id == self.assignment.id else None


class ExposureRepo:
    def __init__(self, exposures=()):
        self.exposures = {e.id: e for e in exposures}

    def save(self, exposure):
        self.exposures[exposure.id] = exposure

    def get(self, exposure_id):
        return self.exposures.get(exposure_id)

    def get_by_assignment(self, assignment_id):
        return next((e for e in self.exposures.values() if e.assignment_id == assignment_id), None)


def _assignment():
    return ExperimentAssignment(
        id="a1",
        experiment_id="exp1",
        subject_id="s1",
        variant="A",
        assigned_at=datetime(2026, 1, 1, 10, tzinfo=timezone.utc),
    )


def test_identical_retry_returns_existing_exposure_without_rewrite():
    existing = ExperimentExposure(
        id="x1", assignment_id="a1", experiment_id="exp1",
        subject_id="s1", variant="A",
        exposed_at=datetime(2026, 1, 1, 11, tzinfo=timezone.utc),
    )
    repo = ExposureRepo([existing])

    result = record_persisted_experiment_exposure(
        assignment_repository=AssignmentRepo(_assignment()),
        exposure_repository=repo,
        assignment_id="a1",
        exposure_id="x1",
        exposed_at=existing.exposed_at,
    )

    assert result == existing
    assert len(repo.exposures) == 1


def test_reused_exposure_id_with_different_payload_is_rejected():
    existing = ExperimentExposure(
        id="x1", assignment_id="a1", experiment_id="exp1",
        subject_id="s1", variant="A",
        exposed_at=datetime(2026, 1, 1, 11, tzinfo=timezone.utc),
    )
    repo = ExposureRepo([existing])

    with pytest.raises(ValueError, match="exposure_id"):
        record_persisted_experiment_exposure(
            assignment_repository=AssignmentRepo(_assignment()),
            exposure_repository=repo,
            assignment_id="a1",
            exposure_id="x1",
            exposed_at=datetime(2026, 1, 1, 12, tzinfo=timezone.utc),
        )


def test_assignment_with_different_exposure_id_is_rejected():
    existing = ExperimentExposure(
        id="x1", assignment_id="a1", experiment_id="exp1",
        subject_id="s1", variant="A",
        exposed_at=datetime(2026, 1, 1, 11, tzinfo=timezone.utc),
    )
    repo = ExposureRepo([existing])

    with pytest.raises(ValueError, match="assignment_id"):
        record_persisted_experiment_exposure(
            assignment_repository=AssignmentRepo(_assignment()),
            exposure_repository=repo,
            assignment_id="a1",
            exposure_id="x2",
            exposed_at=existing.exposed_at,
        )
