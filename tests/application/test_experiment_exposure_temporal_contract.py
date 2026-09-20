from datetime import datetime, timezone
import pytest
from app.application.experiment_exposure_service import record_experiment_exposure, record_persisted_experiment_exposure
from app.domain.controlled_experiment_evidence import ExperimentAssignment

class Repository:
    def __init__(self, assignment=None):
        self.assignment = assignment
        self.saved = []
    def get(self, assignment_id):
        return self.assignment
    def save(self, exposure):
        self.saved.append(exposure)

def assignment():
    return ExperimentAssignment(id="a1", experiment_id="e1", subject_id="s1", variant="control", assigned_at=datetime(2026, 9, 21, 10, 0, tzinfo=timezone.utc))

def test_exposure_before_assignment_is_rejected():
    with pytest.raises(ValueError, match="exposed_at cannot be before assigned_at"):
        record_experiment_exposure(repository=Repository(), assignment=assignment(), exposure_id="x1", exposed_at=datetime(2026, 9, 21, 9, 59, tzinfo=timezone.utc))

def test_exposure_at_assignment_time_is_valid():
    exposure = record_experiment_exposure(repository=Repository(), assignment=assignment(), exposure_id="x1", exposed_at=datetime(2026, 9, 21, 10, 0, tzinfo=timezone.utc))
    assert exposure.exposed_at == assignment().assigned_at

def test_persisted_assignment_exposure_before_assignment_is_rejected():
    repository = Repository(assignment=assignment())
    with pytest.raises(ValueError, match="exposed_at cannot be before assigned_at"):
        record_persisted_experiment_exposure(assignment_repository=repository, exposure_repository=repository, assignment_id="a1", exposure_id="x1", exposed_at=datetime(2026, 9, 21, 9, 59, tzinfo=timezone.utc))
