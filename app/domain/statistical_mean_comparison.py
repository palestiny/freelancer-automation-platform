from dataclasses import dataclass
from enum import Enum
from math import isfinite, inf
from statistics import mean
from typing import Iterable

from .business_performance import BusinessPerformanceObservation
from .performance_history import PerformanceWindow
from .statistical_mean_uncertainty import _student_t_cdf


class MeanComparisonStatus(str, Enum):
    APPLICABLE = "applicable"
    INSUFFICIENT_OBSERVATIONS = "insufficient_observations"
    INVALID_CONTEXT = "invalid_context"
    INVALID_VALUE = "invalid_value"
    INAPPLICABLE = "inapplicable"


@dataclass(frozen=True)
class MeanComparisonResult:
    business_id: str
    metric_name: str
    unit: str
    first_window: PerformanceWindow
    second_window: PerformanceWindow
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
    status: MeanComparisonStatus

    def __post_init__(self) -> None:
        if not 0 < self.alpha < 1:
            raise ValueError("alpha must be between zero and one")
        if self.sample_size_first != len(self.first_observation_ids):
            raise ValueError("sample_size_first must match first_observation_ids")
        if self.sample_size_second != len(self.second_observation_ids):
            raise ValueError("sample_size_second must match second_observation_ids")
        all_ids = self.first_observation_ids + self.second_observation_ids
        if len(set(all_ids)) != len(all_ids):
            raise ValueError("observation_ids must be unique")
        if self.status is MeanComparisonStatus.APPLICABLE:
            if self.sample_size_first < 2 or self.sample_size_second < 2:
                raise ValueError("applicable result requires at least two observations per window")
            if any(value is None for value in (
                self.mean_first, self.mean_second, self.mean_difference,
                self.t_statistic, self.degrees_of_freedom, self.p_value, self.rejects_null,
            )):
                raise ValueError("applicable result requires complete statistical output")
        elif any(value is not None for value in (
            self.t_statistic, self.degrees_of_freedom, self.p_value, self.rejects_null,
        )):
            raise ValueError("non-applicable result cannot contain test output")


def compare_historical_means(
    observations: Iterable[BusinessPerformanceObservation],
    *,
    first_window: PerformanceWindow,
    second_window: PerformanceWindow,
    alpha: float = 0.05,
    assumptions_satisfied: bool = True,
) -> MeanComparisonResult:
    if not 0 < alpha < 1:
        raise ValueError("alpha must be between zero and one")
    if not isinstance(assumptions_satisfied, bool):
        raise ValueError("assumptions_satisfied must be a boolean")
    if first_window.end <= first_window.start or second_window.end <= second_window.start:
        return _empty_context_result(first_window, second_window, alpha, MeanComparisonStatus.INVALID_CONTEXT)
    if first_window.end > second_window.start and second_window.end > first_window.start:
        return _empty_context_result(first_window, second_window, alpha, MeanComparisonStatus.INVALID_CONTEXT)

    selected = tuple(observations)
    first = tuple(observation for observation in selected if first_window.contains(observation.observed_at))
    second = tuple(observation for observation in selected if second_window.contains(observation.observed_at))

    if not first or not second:
        return _empty_context_result(first_window, second_window, alpha, MeanComparisonStatus.INSUFFICIENT_OBSERVATIONS)

    context = first + second
    first_item = first[0]
    if any(
        observation.business_id != first_item.business_id
        or observation.metric_name != first_item.metric_name
        or observation.unit != first_item.unit
        for observation in context
    ):
        return _result(first_item, first, second, first_window, second_window, alpha, MeanComparisonStatus.INVALID_CONTEXT)

    if any(not isfinite(observation.actual_value) for observation in context):
        return _result(first_item, first, second, first_window, second_window, alpha, MeanComparisonStatus.INVALID_VALUE)

    if len(first) < 2 or len(second) < 2:
        return _result(first_item, first, second, first_window, second_window, alpha, MeanComparisonStatus.INSUFFICIENT_OBSERVATIONS)

    if not assumptions_satisfied:
        return _result(first_item, first, second, first_window, second_window, alpha, MeanComparisonStatus.INAPPLICABLE)

    first_values = tuple(float(observation.actual_value) for observation in first)
    second_values = tuple(float(observation.actual_value) for observation in second)
    mean_first = mean(first_values)
    mean_second = mean(second_values)
    variance_first = _sample_variance(first_values, mean_first)
    variance_second = _sample_variance(second_values, mean_second)
    difference = mean_first - mean_second

    standard_error_squared = variance_first / len(first_values) + variance_second / len(second_values)
    if standard_error_squared == 0:
        t_statistic = 0.0 if difference == 0 else inf if difference > 0 else -inf
        degrees_of_freedom = float("inf")
        p_value = 1.0 if difference == 0 else 0.0
    else:
        standard_error = standard_error_squared ** 0.5
        t_statistic = difference / standard_error
        numerator = standard_error_squared ** 2
        denominator = (
            (variance_first / len(first_values)) ** 2 / (len(first_values) - 1)
            + (variance_second / len(second_values)) ** 2 / (len(second_values) - 1)
        )
        degrees_of_freedom = numerator / denominator
        p_value = 2.0 * (1.0 - _student_t_cdf(abs(t_statistic), degrees_of_freedom))
        p_value = max(0.0, min(1.0, p_value))

    return _result(
        first_item, first, second, first_window, second_window, alpha, MeanComparisonStatus.APPLICABLE,
        mean_first=mean_first,
        mean_second=mean_second,
        mean_difference=difference,
        t_statistic=t_statistic,
        degrees_of_freedom=degrees_of_freedom,
        p_value=p_value,
        rejects_null=p_value < alpha,
    )


def _sample_variance(values: tuple[float, ...], sample_mean: float) -> float:
    return sum((value - sample_mean) ** 2 for value in values) / (len(values) - 1)


def _result(
    first_item: BusinessPerformanceObservation,
    first: tuple[BusinessPerformanceObservation, ...],
    second: tuple[BusinessPerformanceObservation, ...],
    first_window: PerformanceWindow,
    second_window: PerformanceWindow,
    alpha: float,
    status: MeanComparisonStatus,
    *,
    mean_first: float | None = None,
    mean_second: float | None = None,
    mean_difference: float | None = None,
    t_statistic: float | None = None,
    degrees_of_freedom: float | None = None,
    p_value: float | None = None,
    rejects_null: bool | None = None,
) -> MeanComparisonResult:
    return MeanComparisonResult(
        business_id=first_item.business_id,
        metric_name=first_item.metric_name,
        unit=first_item.unit,
        first_window=first_window,
        second_window=second_window,
        first_observation_ids=tuple(observation.id for observation in first),
        second_observation_ids=tuple(observation.id for observation in second),
        sample_size_first=len(first),
        sample_size_second=len(second),
        mean_first=mean_first,
        mean_second=mean_second,
        mean_difference=mean_difference,
        t_statistic=t_statistic,
        degrees_of_freedom=degrees_of_freedom,
        p_value=p_value,
        alpha=alpha,
        method="welch_two_sample_t_test",
        rejects_null=rejects_null,
        status=status,
    )


def _empty_context_result(
    first_window: PerformanceWindow,
    second_window: PerformanceWindow,
    alpha: float,
    status: MeanComparisonStatus,
) -> MeanComparisonResult:
    return MeanComparisonResult(
        business_id="unknown",
        metric_name="unknown",
        unit="unknown",
        first_window=first_window,
        second_window=second_window,
        first_observation_ids=(),
        second_observation_ids=(),
        sample_size_first=0,
        sample_size_second=0,
        mean_first=None,
        mean_second=None,
        mean_difference=None,
        t_statistic=None,
        degrees_of_freedom=None,
        p_value=None,
        alpha=alpha,
        method="welch_two_sample_t_test",
        rejects_null=None,
        status=status,
    )
