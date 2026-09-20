from app.domain.controlled_experiment_variant_comparison import (
    ExperimentVariantComparison,
    ExperimentVariantComparisonStatus,
)
from app.domain.controlled_experiment_statistical_comparison import (
    ExperimentStatisticalComparisonResult,
    ExperimentStatisticalComparisonStatus,
)
from app.domain.controlled_experiment_evidence_synthesis import (
    ExperimentEvidenceSynthesisStatus,
    synthesize_experiment_evidence,
)


def _comparison():
    return ExperimentVariantComparison(
        experiment_id="exp-1",
        metric_name="revenue",
        first_variant="A",
        second_variant="B",
        first_count=3,
        second_count=3,
        first_average=100.0,
        second_average=120.0,
        average_difference=20.0,
        relative_difference=0.2,
        first_observation_ids=("a1","a2","a3"),
        second_observation_ids=("b1","b2","b3"),
        status=ExperimentVariantComparisonStatus.APPLICABLE,
    )


def _stat(*, rejects_null=True, difference=20.0, status=ExperimentStatisticalComparisonStatus.APPLICABLE):
    return ExperimentStatisticalComparisonResult(
        experiment_id="exp-1",
        metric_name="revenue",
        first_variant="A",
        second_variant="B",
        first_observation_ids=("a1","a2","a3"),
        second_observation_ids=("b1","b2","b3"),
        sample_size_first=3,
        sample_size_second=3,
        mean_first=100.0 if status is ExperimentStatisticalComparisonStatus.APPLICABLE else None,
        mean_second=120.0 if status is ExperimentStatisticalComparisonStatus.APPLICABLE else None,
        mean_difference=difference if status is ExperimentStatisticalComparisonStatus.APPLICABLE else None,
        t_statistic=2.0 if status is ExperimentStatisticalComparisonStatus.APPLICABLE else None,
        degrees_of_freedom=4.0 if status is ExperimentStatisticalComparisonStatus.APPLICABLE else None,
        p_value=0.04 if rejects_null else 0.4 if status is ExperimentStatisticalComparisonStatus.APPLICABLE else None,
        alpha=0.05,
        method="welch_two_sample_t_test",
        rejects_null=rejects_null if status is ExperimentStatisticalComparisonStatus.APPLICABLE else None,
        status=status,
    )


def test_alignment_is_explicit_without_winner_selection():
    result = synthesize_experiment_evidence(comparison=_comparison(), statistical=_stat())
    assert result.status is ExperimentEvidenceSynthesisStatus.DESCRIPTIVE_AND_STATISTICAL_ALIGNMENT
    assert result.descriptive_difference == 20.0
    assert result.statistical_difference == 20.0
    assert result.observation_ids == ("a1","a2","a3","b1","b2","b3")


def test_descriptive_change_without_significance_is_preserved():
    result = synthesize_experiment_evidence(comparison=_comparison(), statistical=_stat(rejects_null=False))
    assert result.status is ExperimentEvidenceSynthesisStatus.DESCRIPTIVE_CHANGE_WITHOUT_STATISTICAL_DETECTION


def test_statistical_direction_conflict_is_explicit():
    result = synthesize_experiment_evidence(comparison=_comparison(), statistical=_stat(difference=-20.0))
    assert result.status is ExperimentEvidenceSynthesisStatus.STATISTICAL_AND_DESCRIPTIVE_DIRECTION_CONFLICT


def test_unavailable_statistical_result_is_not_reinterpreted():
    result = synthesize_experiment_evidence(
        comparison=_comparison(),
        statistical=_stat(status=ExperimentStatisticalComparisonStatus.INSUFFICIENT_OBSERVATIONS),
    )
    assert result.status is ExperimentEvidenceSynthesisStatus.STATISTICAL_EVIDENCE_UNAVAILABLE


def test_context_mismatch_is_explicit():
    statistical = _stat()
    statistical = ExperimentStatisticalComparisonResult(
        experiment_id="other",
        metric_name=statistical.metric_name,
        first_variant=statistical.first_variant,
        second_variant=statistical.second_variant,
        first_observation_ids=statistical.first_observation_ids,
        second_observation_ids=statistical.second_observation_ids,
        sample_size_first=statistical.sample_size_first,
        sample_size_second=statistical.sample_size_second,
        mean_first=statistical.mean_first,
        mean_second=statistical.mean_second,
        mean_difference=statistical.mean_difference,
        t_statistic=statistical.t_statistic,
        degrees_of_freedom=statistical.degrees_of_freedom,
        p_value=statistical.p_value,
        alpha=statistical.alpha,
        method=statistical.method,
        rejects_null=statistical.rejects_null,
        status=statistical.status,
    )
    result = synthesize_experiment_evidence(comparison=_comparison(), statistical=statistical)
    assert result.status is ExperimentEvidenceSynthesisStatus.CONTEXT_INVALID
