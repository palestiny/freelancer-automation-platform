from datetime import datetime, timezone

from app.domain.controlled_experiment_evidence import ExperimentAssignment, ExperimentObservation
from app.domain.controlled_experiment_readiness import ExperimentReadinessStatus, assess_experiment_readiness
from app.domain.validation_experiment import ValidationExperiment
from app.domain.controlled_experiment_outcome_summary import summarize_experiment_outcomes


def _experiment():
    return ValidationExperiment(
        id="exp-1",
        hypothesis="h",
        objective="o",
        success_criterion="c",
        variants=("A", "B"),
    )


def _assignment(i, subject, variant):
    return ExperimentAssignment(
        id=i, experiment_id="exp-1", subject_id=subject, variant=variant,
        assigned_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
    )


def _observation(i, assignment, subject, variant, value, quality=80):
    return ExperimentObservation(
        id=i, experiment_id="exp-1", assignment_id=assignment,
        subject_id=subject, variant=variant, metric_name="revenue",
        observed_value=value,
        observed_at=datetime(2026, 1, 2, tzinfo=timezone.utc),
        evidence_quality=quality,
    )


def test_summary_is_descriptive_and_preserves_lineage():
    assignments=(
        _assignment("a1","s1","A"), _assignment("a2","s2","A"),
        _assignment("b1","s3","B"), _assignment("b2","s4","B"),
    )
    observations=(
        _observation("o1","a1","s1","A",10),
        _observation("o2","a2","s2","A",20),
        _observation("o3","b1","s3","B",30),
        _observation("o4","b2","s4","B",40),
    )
    readiness=assess_experiment_readiness(
        experiment=_experiment(), assignments=assignments, observations=observations,
        minimum_observations_per_variant=2, minimum_evidence_quality=60,
    )
    assert readiness.status is ExperimentReadinessStatus.READY
    result=summarize_experiment_outcomes(
        experiment=_experiment(), observations=observations, readiness=readiness,
        metric_name="revenue", minimum_evidence_quality=60,
    )
    assert result.experiment_id=="exp-1"
    assert result.metric_name=="revenue"
    assert result.variants["A"].count==2
    assert result.variants["A"].average==15
    assert result.variants["A"].observation_ids==("o1","o2")
    assert result.variants["B"].average==35


def test_low_quality_observations_are_not_silently_used():
    assignments=(_assignment("a1","s1","A"),_assignment("a2","s2","A"))
    observations=(
        _observation("o1","a1","s1","A",10,80),
        _observation("o2","a2","s2","A",20,40),
    )
    readiness=assess_experiment_readiness(
        experiment=_experiment(), assignments=assignments, observations=observations,
        minimum_observations_per_variant=1, minimum_evidence_quality=60,
    )
    result=summarize_experiment_outcomes(
        experiment=_experiment(), observations=observations, readiness=readiness,
        metric_name="revenue", minimum_evidence_quality=60,
    )
    assert result.variants["A"].count==1
    assert result.variants["A"].observation_ids==("o1",)


def test_wrong_metric_is_rejected():
    assignments=(_assignment("a1","s1","A"),)
    observations=(_observation("o1","a1","s1","A",10),)
    readiness=assess_experiment_readiness(
        experiment=_experiment(), assignments=assignments, observations=observations,
        minimum_observations_per_variant=1, minimum_evidence_quality=60,
    )
    import pytest
    with pytest.raises(ValueError):
        summarize_experiment_outcomes(
            experiment=_experiment(), observations=observations, readiness=readiness,
            metric_name="profit", minimum_evidence_quality=60,
        )
