from dataclasses import dataclass
from enum import Enum
from math import exp, isfinite, lgamma, log, pi, sqrt
from statistics import mean
from typing import Iterable

from .business_performance import BusinessPerformanceObservation
from .performance_history import PerformanceWindow


class MeanUncertaintyStatus(str, Enum):
    APPLICABLE = "applicable"
    INSUFFICIENT_OBSERVATIONS = "insufficient_observations"
    INVALID_CONTEXT = "invalid_context"
    INVALID_VALUE = "invalid_value"
    INAPPLICABLE = "inapplicable"


@dataclass(frozen=True)
class MeanUncertaintyResult:
    business_id: str
    metric_name: str
    unit: str
    window: PerformanceWindow
    observation_ids: tuple[str, ...]
    sample_size: int
    sample_mean: float | None
    sample_standard_deviation: float | None
    confidence_level: float
    interval_lower: float | None
    interval_upper: float | None
    method: str
    status: MeanUncertaintyStatus

    def __post_init__(self) -> None:
        if not self.business_id.strip() or not self.metric_name.strip() or not self.unit.strip():
            raise ValueError("business_id, metric_name, and unit cannot be empty")
        if not 0 < self.confidence_level < 1:
            raise ValueError("confidence_level must be between zero and one")
        if self.sample_size != len(self.observation_ids):
            raise ValueError("sample_size must match observation_ids")
        if self.status is MeanUncertaintyStatus.APPLICABLE:
            if self.sample_size < 2:
                raise ValueError("applicable result requires at least two observations")
            if self.sample_mean is None or self.sample_standard_deviation is None:
                raise ValueError("applicable result requires sample statistics")
            if self.interval_lower is None or self.interval_upper is None:
                raise ValueError("applicable result requires an interval")
        elif self.interval_lower is not None or self.interval_upper is not None:
            raise ValueError("non-applicable result cannot contain an interval")


def calculate_mean_uncertainty(
    observations: Iterable[BusinessPerformanceObservation],
    *,
    window: PerformanceWindow,
    confidence_level: float = 0.95,
) -> MeanUncertaintyResult:
    if not 0 < confidence_level < 1:
        raise ValueError("confidence_level must be between zero and one")

    selected = tuple(
        observation for observation in observations if window.contains(observation.observed_at)
    )
    if not selected:
        return MeanUncertaintyResult(
            business_id="unknown",
            metric_name="unknown",
            unit="unknown",
            window=window,
            observation_ids=(),
            sample_size=0,
            sample_mean=None,
            sample_standard_deviation=None,
            confidence_level=confidence_level,
            interval_lower=None,
            interval_upper=None,
            method="student_t_mean_ci",
            status=MeanUncertaintyStatus.INSUFFICIENT_OBSERVATIONS,
        )

    first = selected[0]
    if any(
        observation.business_id != first.business_id
        or observation.metric_name != first.metric_name
        or observation.unit != first.unit
        for observation in selected
    ):
        return _result(first, selected, window, confidence_level, MeanUncertaintyStatus.INVALID_CONTEXT)

    if any(not isfinite(observation.actual_value) for observation in selected):
        return _result(first, selected, window, confidence_level, MeanUncertaintyStatus.INVALID_VALUE)

    values = tuple(float(observation.actual_value) for observation in selected)
    n = len(values)
    sample_mean = mean(values)

    if n < 2:
        return _result(
            first, selected, window, confidence_level,
            MeanUncertaintyStatus.INSUFFICIENT_OBSERVATIONS,
            sample_mean=sample_mean,
        )

    variance = sum((value - sample_mean) ** 2 for value in values) / (n - 1)
    standard_deviation = sqrt(variance)
    critical = _student_t_critical(confidence_level, n - 1)
    margin = critical * standard_deviation / sqrt(n)

    return _result(
        first, selected, window, confidence_level, MeanUncertaintyStatus.APPLICABLE,
        sample_mean=sample_mean,
        sample_standard_deviation=standard_deviation,
        interval_lower=sample_mean - margin,
        interval_upper=sample_mean + margin,
    )


def _result(
    first: BusinessPerformanceObservation,
    selected: tuple[BusinessPerformanceObservation, ...],
    window: PerformanceWindow,
    confidence_level: float,
    status: MeanUncertaintyStatus,
    *,
    sample_mean: float | None = None,
    sample_standard_deviation: float | None = None,
    interval_lower: float | None = None,
    interval_upper: float | None = None,
) -> MeanUncertaintyResult:
    return MeanUncertaintyResult(
        business_id=first.business_id,
        metric_name=first.metric_name,
        unit=first.unit,
        window=window,
        observation_ids=tuple(observation.id for observation in selected),
        sample_size=len(selected),
        sample_mean=sample_mean,
        sample_standard_deviation=sample_standard_deviation,
        confidence_level=confidence_level,
        interval_lower=interval_lower,
        interval_upper=interval_upper,
        method="student_t_mean_ci",
        status=status,
    )


def _student_t_critical(confidence_level: float, degrees_of_freedom: int) -> float:
    if degrees_of_freedom < 1:
        raise ValueError("degrees_of_freedom must be positive")
    target = (1 + confidence_level) / 2
    low, high = 0.0, 1.0
    while _student_t_cdf(high, degrees_of_freedom) < target:
        high *= 2
    for _ in range(70):
        midpoint = (low + high) / 2
        if _student_t_cdf(midpoint, degrees_of_freedom) < target:
            low = midpoint
        else:
            high = midpoint
    return (low + high) / 2


def _student_t_cdf(x: float, degrees_of_freedom: int) -> float:
    if x == 0:
        return 0.5
    sign = 1 if x > 0 else -1
    area = _integrate_student_t_pdf(0.0, abs(x), degrees_of_freedom)
    return 0.5 + sign * area


def _integrate_student_t_pdf(start: float, end: float, degrees_of_freedom: int) -> float:
    intervals = 2048
    h = (end - start) / intervals
    total = _student_t_pdf(start, degrees_of_freedom) + _student_t_pdf(end, degrees_of_freedom)
    total += 4 * sum(
        _student_t_pdf(start + i * h, degrees_of_freedom)
        for i in range(1, intervals, 2)
    )
    total += 2 * sum(
        _student_t_pdf(start + i * h, degrees_of_freedom)
        for i in range(2, intervals, 2)
    )
    return total * h / 3


def _student_t_pdf(x: float, degrees_of_freedom: int) -> float:
    coefficient = exp(
        lgamma((degrees_of_freedom + 1) / 2)
        - lgamma(degrees_of_freedom / 2)
        - 0.5 * (log(degrees_of_freedom) + log(pi))
    )
    return coefficient * (1 + (x * x) / degrees_of_freedom) ** (-(degrees_of_freedom + 1) / 2)
