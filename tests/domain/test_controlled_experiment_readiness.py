from datetime import datetime, timezone

import pytest

from app.domain.controlled_experiment_evidence import ExperimentAssignment, ExperimentObservation
from app.domain.validation_experiment import ValidationExperiment
from app.domain.controlled_experiment_readiness import (
    ExperimentReadinessStatus,
    assess_experiment_readiness,
)


def _experiment():
    return ValidationExperiment(
        id="exp1",
        hypothesis="h",
        objective="o",
        success_criterion="c",
        variants=("control", "treatment"),
    )


def _assignment(aid, subject, variant):
    return ExperimentAssignment(
        id=aid,
        experiment_id="exp1",
        subject_id=subject,
        variant=variant,
        assigned_at=datetime(2026, 3, 1, tzinfo=timezone.utc),
    )


def _observation(oid, aid, subject, variant, quality=80):
    return ExperimentObservation(
        id=oid,
        experiment_id="exp1",
        assignment_id=aid,
        subject_id=subject,
        variant=variant,
        metric_name="revenue",
        observed_value=100.0,
        observed_at=datetime(2026, 3, 2, tzinfo=timezone.utc),
        evidence_quality=quality,
    )


def test_readiness_is_ready_when_each_variant_has_enough_evidence():
    result = assess_experiment_readiness(
        experiment=_experiment(),
        assignments=(_assignment("a1", "s1", "control"), _assignment("a2", "s2", "treatment")),
        observations=(
            _observation("o1", "a1", "s1", "control"),
            _observation("o2", "a2", "s2", "treatment"),
        ),
        minimum_observations_per_variant=1,
        minimum_evidence_quality=60,
    )
    assert result.status is ExperimentReadinessStatus.READY


def test_readiness_collects_when_one_variant_is_under_sampled():
    result = assess_experiment_readiness(
        experiment=_experiment(),
        assignments=(_assignment("a1", "s1", "control"),),
        observations=(_observation("o1", "a1", "s1", "control"),),
        minimum_observations_per_variant=1,
        minimum_evidence_quality=60,
    )
    assert result.status is ExperimentReadinessStatus.COLLECTING
    assert result.missing_variants == ("treatment",)


def test_low_quality_observation_does_not_count_as_usable_evidence():
    result = assess_experiment_readiness(
        experiment=_experiment(),
        assignments=(_assignment("a1", "s1", "control"), _assignment("a2", "s2", "treatment")),
        observations=(
            _observation("o1", "a1", "s1", "control", quality=59),
            _observation("o2", "a2", "s2", "treatment", quality=80),
        ),
        minimum_observations_per_variant=1,
        minimum_evidence_quality=60,
    )
    assert result.status is ExperimentReadinessStatus.COLLECTING
    assert result.missing_variants == ("control",)


def test_observation_lineage_mismatch_is_invalid_context():
    with pytest.raises(ValueError):
        assess_experiment_readiness(
            experiment=_experiment(),
            assignments=(_assignment("a1", "s1", "control"), _assignment("a2", "s2", "treatment")),
            observations=(
                _observation("o1", "a1", "other-subject", "control"),
                _observation("o2", "a2", "s2", "treatment"),
            ),
            minimum_observations_per_variant=1,
            minimum_evidence_quality=60,
        )


@pytest.mark.parametrize("minimum", [0, -1])
def test_minimum_observations_must_be_positive(minimum):
    with pytest.raises(ValueError):
        assess_experiment_readiness(
            experiment=_experiment(),
            assignments=(),
            observations=(),
            minimum_observations_per_variant=minimum,
        )
