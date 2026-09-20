from dataclasses import dataclass
from enum import Enum
from math import isfinite, sqrt

from .statistical_mean_comparison import _student_t_cdf


class ExperimentStatisticalComparisonStatus(str, Enum):
    APPLICABLE = "applicable"
    INSUFFICIENT_OBSERVATIONS = "insufficient_observations"
    INVALID_CONTEXT = "invalid_context"
    INVALID_VALUE = "invalid_value"
    INAPPLICABLE = "inapplicable"


@dataclass(frozen=True)
class ExperimentStatisticalComparisonResult:
    experiment_id: str
    metric_name: str
    first_variant: str
    second_variant: str
    first_observation_ids: tuple[str, ...]
    second_observation_ids: tuple[str, ...]
    sample_size_first: int
    sample_size_second: int
    mean_first: float | None
    mean_second: float | None
    mean_difference: float | None
    t_statistic: float | None
    degrees_of_freedom: float | None
    p_value: float | None
    alpha: float
    method: str
    rejects_null: bool | None
    status: ExperimentStatisticalComparisonStatus

    @property
    def observation_ids(self) -> tuple[str, ...]:
        return self.first_observation_ids + self.second_observation_ids


def compare_experiment_variants_statistically(
    *,
    experiment_id: str,
    metric_name: str,
    first_variant: str,
    second_variant: str,
    first_values: tuple[float, ...],
    second_values: tuple[float, ...],
    first_observation_ids: tuple[str, ...],
    second_observation_ids: tuple[str, ...],
    alpha: float = 0.05,
    assumptions_satisfied: bool = True,
) -> ExperimentStatisticalComparisonResult:
    if not experiment_id.strip() or not metric_name.strip() or not first_variant.strip() or not second_variant.strip():
        raise ValueError("experiment and variant context cannot be empty")
    if first_variant == second_variant:
        raise ValueError("variants must be distinct")
    if not 0 < alpha < 1:
        raise ValueError("alpha must be between zero and one")
    if not isinstance(assumptions_satisfied, bool):
        raise TypeError("assumptions_satisfied must be a boolean")
    if len(first_values) != len(first_observation_ids) or len(second_values) != len(second_observation_ids):
        raise ValueError("value and observation-id counts must match")
    if len(set(first_observation_ids + second_observation_ids)) != len(first_observation_ids) + len(second_observation_ids):
        raise ValueError("observation ids must be unique across variants")
    if any(not isinstance(value, (int, float)) or isinstance(value, bool) or not isfinite(value) for value in first_values + second_values):
        return _invalid_value_result(
            experiment_id, metric_name, first_variant, second_variant,
            first_observation_ids, second_observation_ids, alpha
        )
    if len(first_values) < 2 or len(second_values) < 2:
        return _base_result(
            experiment_id, metric_name, first_variant, second_variant,
            first_observation_ids, second_observation_ids, alpha,
            status=ExperimentStatisticalComparisonStatus.INSUFFICIENT_OBSERVATIONS
        )
    if not assumptions_satisfied:
        return _base_result(
            experiment_id, metric_name, first_variant, second_variant,
            first_observation_ids, second_observation_ids, alpha,
            status=ExperimentStatisticalComparisonStatus.INAPPLICABLE
        )

    mean_first = sum(first_values) / len(first_values)
    mean_second = sum(second_values) / len(second_values)
    variance_first = _sample_variance(first_values, mean_first)
    variance_second = _sample_variance(second_values, mean_second)
    se_squared = variance_first / len(first_values) + variance_second / len(second_values)

    if se_squared == 0:
        t_statistic = float("inf") if mean_first != mean_second else 0.0
        p_value = 0.0 if mean_first != mean_second else 1.0
        degrees_of_freedom = float("inf")
    else:
        t_statistic = (mean_first - mean_second) / sqrt(se_squared)
        numerator = se_squared**2
        denominator = (
            (variance_first / len(first_values)) ** 2 / (len(first_values) - 1)
            + (variance_second / len(second_values)) ** 2 / (len(second_values) - 1)
        )
        degrees_of_freedom = numerator / denominator if denominator else float("inf")
        p_value = min(1.0, max(0.0, 2.0 * (1.0 - _student_t_cdf(abs(t_statistic), degrees_of_freedom))))

    return ExperimentStatisticalComparisonResult(
        experiment_id=experiment_id,
        metric_name=metric_name,
        first_variant=first_variant,
        second_variant=second_variant,
        first_observation_ids=first_observation_ids,
        second_observation_ids=second_observation_ids,
        sample_size_first=len(first_values),
        sample_size_second=len(second_values),
        mean_first=mean_first,
        mean_second=mean_second,
        mean_difference=mean_second - mean_first,
        t_statistic=t_statistic,
        degrees_of_freedom=degrees_of_freedom,
        p_value=p_value,
        alpha=alpha,
        method="welch_two_sample_t_test",
        rejects_null=p_value < alpha,
        status=ExperimentStatisticalComparisonStatus.APPLICABLE,
    )


def _base_result(experiment_id, metric_name, first_variant, second_variant, first_ids, second_ids, alpha, *, status):
    return ExperimentStatisticalComparisonResult(
        experiment_id=experiment_id, metric_name=metric_name,
        first_variant=first_variant, second_variant=second_variant,
        first_observation_ids=first_ids, second_observation_ids=second_ids,
        sample_size_first=len(first_ids), sample_size_second=len(second_ids),
        mean_first=None, mean_second=None, mean_difference=None,
        t_statistic=None, degrees_of_freedom=None, p_value=None,
        alpha=alpha, method="welch_two_sample_t_test", rejects_null=None, status=status,
    )


def _invalid_value_result(experiment_id, metric_name, first_variant, second_variant, first_ids, second_ids, alpha):
    return _base_result(
        experiment_id, metric_name, first_variant, second_variant, first_ids, second_ids, alpha,
        status=ExperimentStatisticalComparisonStatus.INVALID_VALUE,
    )


def _sample_variance(values, mean):
    return sum((value - mean) ** 2 for value in values) / (len(values) - 1)
