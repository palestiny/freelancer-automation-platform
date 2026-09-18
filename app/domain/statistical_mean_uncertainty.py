from dataclasses import dataclass
from enum import Enum
from math import exp, isfinite, lgamma, log, sqrt
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
        if self.status is MeanUncertaintyStatus.INSUFFICIENT_OBSERVATIONS and self.sample_size == 0:
            if self.observation_ids:
                raise ValueError("empty result cannot contain observation_ids")
        elif not self.business_id.strip() or not self.metric_name.strip() or not self.unit.strip():
            raise ValueError("business_id, metric_name, and unit cannot be empty")
        if not 0 < self.confidence_level < 1:
            raise ValueError("confidence_level must be between zero and one")
        if self.sample_size != len(self.observation_ids):
            raise ValueError("sample_size must match observation_ids")
        if len(set(self.observation_ids)) != len(self.observation_ids):
            raise ValueError("observation_ids must be unique")
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
    assumptions_satisfied: bool = True,
) -> MeanUncertaintyResult:
    if not 0 < confidence_level < 1:
        raise ValueError("confidence_level must be between zero and one")

    if not isinstance(assumptions_satisfied, bool):
        raise ValueError("assumptions_satisfied must be a boolean")

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
    if not assumptions_satisfied:
        return _result(first, selected, window, confidence_level, MeanUncertaintyStatus.INAPPLICABLE)

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
    if degrees_of_freedom < 1:
        raise ValueError("degrees_of_freedom must be positive")
    if x == 0:
        return 0.5

    v = float(degrees_of_freedom)
    a = v / 2.0
    b = 0.5
    z = v / (v + x * x)
    beta = _regularized_incomplete_beta(z, a, b)
    return 1.0 - 0.5 * beta if x > 0 else 0.5 * beta


def _regularized_incomplete_beta(x: float, a: float, b: float) -> float:
    if not 0.0 <= x <= 1.0:
        raise ValueError("beta input must be between zero and one")
    if x == 0.0:
        return 0.0
    if x == 1.0:
        return 1.0

    if x < (a + 1.0) / (a + b + 2.0):
        return _beta_front_factor(x, a, b) * _continued_fraction_beta(x, a, b) / a

    return 1.0 - _beta_front_factor(1.0 - x, b, a) * _continued_fraction_beta(1.0 - x, b, a) / b


def _beta_front_factor(x: float, a: float, b: float) -> float:
    return exp(a * log(x) + b * log(1.0 - x) - lgamma(a) - lgamma(b) + lgamma(a + b))


def _continued_fraction_beta(x: float, a: float, b: float) -> float:
    # Lentz's method for the incomplete-beta continued fraction.
    max_iterations = 200
    epsilon = 3.0e-14
    tiny = 1.0e-300

    c = 1.0
    d = 1.0 - (a + b) * x / (a + 1.0)
    if abs(d) < tiny:
        d = tiny
    d = 1.0 / d
    h = d

    for m in range(1, max_iterations + 1):
        m_float = float(m)
        m2 = 2.0 * m_float
        numerator = m_float * (b - m_float) * x / ((a - 1.0 + m2) * (a + m2))
        d = 1.0 + numerator * d
        if abs(d) < tiny:
            d = tiny
        c = 1.0 + numerator / c
        if abs(c) < tiny:
            c = tiny
        d = 1.0 / d
        h *= d * c

        numerator = -(a + m_float) * (a + b + m_float) * x / ((a + m2) * (a + 1.0 + m2))
        d = 1.0 + numerator * d
        if abs(d) < tiny:
            d = tiny
        c = 1.0 + numerator / c
        if abs(c) < tiny:
            c = tiny
        d = 1.0 / d
        delta = d * c
        h *= delta

        if abs(delta - 1.0) < epsilon:
            return h

    raise ArithmeticError("incomplete beta continued fraction did not converge")
