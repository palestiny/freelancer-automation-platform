from datetime import datetime, timezone

from app.domain.controlled_experiment_evidence import ExperimentExposure, ExperimentObservation
from app.domain.experiment_observation_exposure_lineage import (
    ExposureLineageStatus,
    validate_observation_exposure_lineage,
)


def _exposure():
    return ExperimentExposure(
        id="exposure-1",
        assignment_id="assignment-1",
        experiment_id="exp-1",
        subject_id="subject-1",
        variant="A",
        exposed_at=datetime(2026, 9, 20, 10, tzinfo=timezone.utc),
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
        observed_at=datetime(2026, 9, 20, 11, tzinfo=timezone.utc),
    )
    values.update(overrides)
    return ExperimentObservation(**values)


def test_matching_exposure_context_is_valid():
    result = validate_observation_exposure_lineage(
        observation=_observation(),
        exposure=_exposure(),
    )
    assert result.status is ExposureLineageStatus.VALID


def test_observation_before_exposure_is_rejected():
    result = validate_observation_exposure_lineage(
        observation=_observation(
            observed_at=datetime(2026, 9, 20, 9, tzinfo=timezone.utc)
        ),
        exposure=_exposure(),
    )
    assert result.status is ExposureLineageStatus.BEFORE_EXPOSURE


def test_mismatched_experiment_is_rejected():
    result = validate_observation_exposure_lineage(
        observation=_observation(experiment_id="exp-2"),
        exposure=_exposure(),
    )
    assert result.status is ExposureLineageStatus.INVALID_CONTEXT


def test_mismatched_assignment_is_rejected():
    result = validate_observation_exposure_lineage(
        observation=_observation(assignment_id="assignment-2"),
        exposure=_exposure(),
    )
    assert result.status is ExposureLineageStatus.INVALID_CONTEXT


def test_mismatched_variant_is_rejected():
    result = validate_observation_exposure_lineage(
        observation=_observation(variant="B"),
        exposure=_exposure(),
    )
    assert result.status is ExposureLineageStatus.INVALID_CONTEXT

# Regression suite covers context and temporal exposure lineage.
