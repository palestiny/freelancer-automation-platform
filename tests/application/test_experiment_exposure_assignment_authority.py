from datetime import datetime, timezone

import pytest

from app.application.experiment_exposure_service import record_persisted_experiment_exposure
from app.domain.controlled_experiment_evidence import ExperimentAssignment


class AssignmentRepo:
    def __init__(self, assignment=None):
        self.assignment = assignment

    def get(self, assignment_id):
        return self.assignment if self.assignment and self.assignment.id == assignment_id else None


class ExposureRepo:
    def __init__(self):
        self.saved = []

    def save(self, exposure):
        self.saved.append(exposure)

    def get(self, exposure_id):
        return None

    def get_by_assignment(self, assignment_id):
        return next((x for x in self.saved if x.assignment_id == assignment_id), None)


def _assignment():
    return ExperimentAssignment(
        id="a1",
        experiment_id="exp1",
        subject_id="s1",
        variant="A",
        assigned_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
    )


def test_exposure_uses_authoritative_persisted_assignment():
    exposures = ExposureRepo()
    result = record_persisted_experiment_exposure(
        assignment_repository=AssignmentRepo(_assignment()),
        exposure_repository=exposures,
        assignment_id="a1",
        exposure_id="x1",
        exposed_at=datetime(2026, 1, 2, tzinfo=timezone.utc),
    )
    assert result.assignment_id == "a1"
    assert result.experiment_id == "exp1"
    assert result.subject_id == "s1"
    assert result.variant == "A"
    assert exposures.saved == [result]


def test_missing_assignment_cannot_produce_exposure():
    with pytest.raises(ValueError, match="assignment 'missing' does not exist"):
        record_persisted_experiment_exposure(
            assignment_repository=AssignmentRepo(),
            exposure_repository=ExposureRepo(),
            assignment_id="missing",
            exposure_id="x1",
            exposed_at=datetime(2026, 1, 2, tzinfo=timezone.utc),
        )
