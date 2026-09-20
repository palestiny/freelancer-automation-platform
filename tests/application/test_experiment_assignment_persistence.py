from datetime import datetime, timezone

import pytest

from app.application.ports.experiment_assignment_repository import (
    ExperimentAssignmentRepository,
)
from app.domain.controlled_experiment_allocation import (
    ExperimentAllocationDecision,
)
from app.domain.controlled_experiment_evidence import ExperimentAssignment
from app.infrastructure.experiment_assignment_repository import (
    SQLiteExperimentAssignmentRepository,
)
from app.application.experiment_assignment_service import persist_experiment_assignment


def _decision():
    return ExperimentAllocationDecision(
        experiment_id="exp-1",
        subject_id="subject-1",
        variant="A",
        bucket=1234,
    )


def _assignment():
    return ExperimentAssignment(
        id="assignment-1",
        experiment_id="exp-1",
        subject_id="subject-1",
        variant="A",
        assigned_at=datetime(2026, 9, 20, tzinfo=timezone.utc),
    )


def test_sqlite_repository_conforms_to_port():
    repository = SQLiteExperimentAssignmentRepository(":memory:")
    assert isinstance(repository, ExperimentAssignmentRepository)
    repository.close()


def test_save_get_and_list_preserve_assignment():
    repository = SQLiteExperimentAssignmentRepository(":memory:")
    assignment = _assignment()
    repository.save(assignment)

    assert repository.get(assignment.id) == assignment
    assert repository.list_by_experiment("exp-1") == (assignment,)
    repository.close()


def test_duplicate_assignment_identity_is_rejected():
    repository = SQLiteExperimentAssignmentRepository(":memory:")
    assignment = _assignment()
    repository.save(assignment)

    with pytest.raises(ValueError, match="assignment .* already exists"):
        repository.save(assignment)
    repository.close()


def test_second_assignment_for_same_subject_is_rejected():
    repository = SQLiteExperimentAssignmentRepository(":memory:")
    repository.save(_assignment())
    conflicting = ExperimentAssignment(
        id="assignment-2",
        experiment_id="exp-1",
        subject_id="subject-1",
        variant="B",
        assigned_at=datetime(2026, 9, 20, tzinfo=timezone.utc),
    )

    with pytest.raises(ValueError, match="subject .* already assigned"):
        repository.save(conflicting)
    repository.close()


def test_assignment_service_requires_allocation_variant_match():
    decision = _decision()
    repository = SQLiteExperimentAssignmentRepository(":memory:")

    assignment = persist_experiment_assignment(
        repository=repository,
        decision=decision,
        assignment_id="assignment-1",
        assigned_at=datetime(2026, 9, 20, tzinfo=timezone.utc),
    )

    assert assignment.variant == decision.variant
    assert repository.get("assignment-1") == assignment
    repository.close()


def test_assignment_service_rejects_empty_identity():
    repository = SQLiteExperimentAssignmentRepository(":memory:")

    with pytest.raises(ValueError, match="assignment_id cannot be empty"):
        persist_experiment_assignment(
            repository=repository,
            decision=_decision(),
            assignment_id="",
            assigned_at=datetime(2026, 9, 20, tzinfo=timezone.utc),
        )
    repository.close()
