import pytest

from app.domain.controlled_experiment_outcome_summary import (
    ControlledExperimentOutcomeSummary,
    ExperimentVariantSummary,
)
from app.domain.controlled_experiment_statistical_comparison import (
    ExperimentStatisticalComparisonStatus,
    compare_experiment_variants_statistically,
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


def test_requires_explicit_observations_for_statistical_comparison():
    result = compare_experiment_variants_statistically(
        experiment_id="exp-1",
        metric_name="revenue",
        first_variant="A",
        second_variant="B",
        first_values=(98.0, 100.0, 102.0),
        second_values=(108.0, 110.0, 112.0),
        first_observation_ids=("a1", "a2", "a3"),
        second_observation_ids=("b1", "b2", "b3"),
    )
    assert result.status is ExperimentStatisticalComparisonStatus.APPLICABLE
    assert result.method == "welch_two_sample_t_test"
    assert result.sample_size_first == 3
    assert result.sample_size_second == 3
    assert result.mean_difference == pytest.approx(10.0)
    assert result.observation_ids == ("a1", "a2", "a3", "b1", "b2", "b3")


def test_insufficient_observations_are_explicit():
    result = compare_experiment_variants_statistically(
        experiment_id="exp-1", metric_name="revenue",
        first_variant="A", second_variant="B",
        first_values=(100.0,), second_values=(110.0, 111.0),
        first_observation_ids=("a1",),
        second_observation_ids=("b1", "b2"),
    )
    assert result.status is ExperimentStatisticalComparisonStatus.INSUFFICIENT_OBSERVATIONS


def test_invalid_values_are_explicit():
    result = compare_experiment_variants_statistically(
        experiment_id="exp-1", metric_name="revenue",
        first_variant="A", second_variant="B",
        first_values=(100.0, float("nan")), second_values=(110.0, 111.0),
        first_observation_ids=("a1", "a2"),
        second_observation_ids=("b1", "b2"),
    )
    assert result.status is ExperimentStatisticalComparisonStatus.INVALID_VALUE


def test_assumptions_can_mark_result_inapplicable():
    result = compare_experiment_variants_statistically(
        experiment_id="exp-1", metric_name="revenue",
        first_variant="A", second_variant="B",
        first_values=(100.0, 101.0), second_values=(110.0, 111.0),
        first_observation_ids=("a1", "a2"),
        second_observation_ids=("b1", "b2"),
        assumptions_satisfied=False,
    )
    assert result.status is ExperimentStatisticalComparisonStatus.INAPPLICABLE


def test_context_validation_precedes_applicability():
    with pytest.raises(ValueError):
        compare_experiment_variants_statistically(
            experiment_id="", metric_name="revenue",
            first_variant="A", second_variant="B",
            first_values=(100.0, 101.0), second_values=(110.0, 111.0),
            first_observation_ids=("a1", "a2"),
            second_observation_ids=("b1", "b2"),
            assumptions_satisfied=False,
        )
