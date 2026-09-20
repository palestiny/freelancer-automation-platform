from datetime import datetime, timezone

import pytest

from app.domain.controlled_experiment_evidence import (
    ExperimentAssignment,
    ExperimentObservation,
)


def _at(day: int):
    return datetime(2026, 3, day, tzinfo=timezone.utc)


def test_assignment_preserves_explicit_variant():
    assignment = ExperimentAssignment(
        id="a1",
        experiment_id="exp1",
        subject_id="subject1",
        variant="control",
        assigned_at=_at(1),
    )
    assert assignment.variant == "control"


def test_assignment_rejects_empty_identity():
    with pytest.raises(ValueError):
        ExperimentAssignment(
            id="",
            experiment_id="exp1",
            subject_id="subject1",
            variant="control",
            assigned_at=_at(1),
        )


def test_observation_preserves_assignment_lineage():
    observation = ExperimentObservation(
        id="o1",
        experiment_id="exp1",
        assignment_id="a1",
        subject_id="subject1",
        variant="treatment",
        metric_name="revenue",
        observed_value=120.0,
        observed_at=_at(2),
        evidence_quality=80,
    )
    assert observation.assignment_id == "a1"
    assert observation.variant == "treatment"


@pytest.mark.parametrize("quality", [-1, 101])
def test_observation_rejects_invalid_evidence_quality(quality):
    with pytest.raises(ValueError):
        ExperimentObservation(
            id="o1",
            experiment_id="exp1",
            assignment_id="a1",
            subject_id="subject1",
            variant="control",
            metric_name="revenue",
            observed_value=120.0,
            observed_at=_at(2),
            evidence_quality=quality,
        )


def test_observation_rejects_non_numeric_value():
    with pytest.raises(TypeError):
        ExperimentObservation(
            id="o1",
            experiment_id="exp1",
            assignment_id="a1",
            subject_id="subject1",
            variant="control",
            metric_name="revenue",
            observed_value="120",
            observed_at=_at(2),
        )


def test_observation_requires_non_empty_identity_fields():
    with pytest.raises(ValueError):
        ExperimentObservation(
            id="o1",
            experiment_id="",
            assignment_id="a1",
            subject_id="subject1",
            variant="control",
            metric_name="revenue",
            observed_value=120.0,
            observed_at=_at(2),
        )
