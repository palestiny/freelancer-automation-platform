import pytest

from app.domain.controlled_experiment_summary import (
    ControlledExperimentOutcomeSummary,
    ExperimentVariantSummary,
)
from app.domain.controlled_experiment_variant_comparison import (
    ExperimentVariantComparisonStatus,
    compare_experiment_variants,
)


def _summary() -> ControlledExperimentOutcomeSummary:
    return ControlledExperimentOutcomeSummary(
        experiment_id="exp-1",
        metric_name="revenue",
        variants={
            "A": ExperimentVariantSummary(
                variant="A", count=3, average=100, minimum=80, maximum=120,
                average_evidence_quality=80, observation_ids=("a1", "a2", "a3")
            ),
            "B": ExperimentVariantSummary(
                variant="B", count=3, average=110, minimum=90, maximum=130,
                average_evidence_quality=85, observation_ids=("b1", "b2", "b3")
            ),
        },
        readiness_status="ready",
    )


def test_descriptive_comparison_preserves_neutral_difference():
    result = compare_experiment_variants(
        summary=_summary(), first_variant="A", second_variant="B"
    )
    assert result.status is ExperimentVariantComparisonStatus.APPLICABLE
    assert result.average_difference == 10
    assert result.relative_difference == 0.1
    assert result.first_observation_ids == ("a1", "a2", "a3")
    assert result.second_observation_ids == ("b1", "b2", "b3")


def test_missing_variant_is_explicit():
    result = compare_experiment_variants(
        summary=_summary(), first_variant="A", second_variant="C"
    )
    assert result.status is ExperimentVariantComparisonStatus.VARIANT_NOT_FOUND


def test_same_variant_is_rejected():
    result = compare_experiment_variants(
        summary=_summary(), first_variant="A", second_variant="A"
    )
    assert result.status is ExperimentVariantComparisonStatus.SAME_VARIANT


def test_zero_first_average_has_no_relative_difference():
    summary = _summary()
    summary = ControlledExperimentOutcomeSummary(
        experiment_id=summary.experiment_id,
        metric_name=summary.metric_name,
        variants={
            **summary.variants,
            "A": ExperimentVariantSummary(
                variant="A", count=2, average=0, minimum=-1, maximum=1,
                average_evidence_quality=80, observation_ids=("a4", "a5")
            ),
        },
        readiness_status=summary.readiness_status,
    )
    result = compare_experiment_variants(
        summary=summary, first_variant="A", second_variant="B"
    )
    assert result.relative_difference is None
