from dataclasses import dataclass
from .business_performance import BusinessPerformanceHistory, BusinessPerformanceObservation
from .performance_history import PerformanceWindow, observations_in_window


@dataclass(frozen=True)
class PerformanceAggregate:
    """Deterministic summary of one metric inside an explicit time window."""

    business_id: str
    metric_name: str
    unit: str
    window: PerformanceWindow
    observation_ids: tuple[str, ...]
    actual_count: int
    actual_average: float
    actual_min: float
    actual_max: float
    expected_count: int
    expected_average: float | None
    average_variance: float | None
    average_relative_variance: float | None
    average_evidence_quality: float

    def __post_init__(self) -> None:
        if not self.business_id.strip():
            raise ValueError("business_id cannot be empty")
        if not self.metric_name.strip() or not self.unit.strip():
            raise ValueError("metric_name and unit cannot be empty")
        if not self.observation_ids:
            raise ValueError("observation_ids cannot be empty")
        if self.actual_count != len(self.observation_ids):
            raise ValueError("actual_count must match observation_ids")
        if self.actual_count <= 0:
            raise ValueError("actual_count must be greater than zero")
        if not 0 <= self.expected_count <= self.actual_count:
            raise ValueError("expected_count must be between zero and actual_count")
        if self.expected_count == 0 and (
            self.expected_average is not None
            or self.average_variance is not None
            or self.average_relative_variance is not None
        ):
            raise ValueError("expected-derived aggregates require expected observations")
        if not 0 <= self.average_evidence_quality <= 100:
            raise ValueError("average_evidence_quality must be between 0 and 100")


def aggregate_performance(
    observations: tuple[BusinessPerformanceObservation, ...],
    *,
    window: PerformanceWindow,
) -> PerformanceAggregate | None:
    """Aggregate one business/metric/unit within an explicit window."""

    selected = tuple(
        observation
        for observation in observations
        if window.contains(observation.observed_at)
    )
    if not selected:
        return None

    first = selected[0]
    if any(
        observation.business_id != first.business_id
        or observation.metric_name != first.metric_name
        or observation.unit != first.unit
        for observation in selected
    ):
        raise ValueError(
            "all observations must belong to the same business, metric, and unit"
        )

    expected = tuple(
        observation for observation in selected if observation.expected_value is not None
    )
    relative_variances = tuple(
        observation.relative_variance
        for observation in expected
        if observation.relative_variance is not None
    )

    return PerformanceAggregate(
        business_id=first.business_id,
        metric_name=first.metric_name,
        unit=first.unit,
        window=window,
        observation_ids=tuple(observation.id for observation in selected),
        actual_count=len(selected),
        actual_average=sum(o.actual_value for o in selected) / len(selected),
        actual_min=min(o.actual_value for o in selected),
        actual_max=max(o.actual_value for o in selected),
        expected_count=len(expected),
        expected_average=(
            sum(o.expected_value for o in expected) / len(expected)
            if expected
            else None
        ),
        average_variance=(
            sum(o.variance for o in expected if o.variance is not None) / len(expected)
            if expected
            else None
        ),
        average_relative_variance=(
            sum(relative_variances) / len(relative_variances)
            if relative_variances
            else None
        ),
        average_evidence_quality=sum(
            o.evidence_quality for o in selected
        ) / len(selected),
    )


def aggregate_history_metric(
    history: BusinessPerformanceHistory,
    *,
    metric_name: str,
    unit: str,
    window: PerformanceWindow,
) -> PerformanceAggregate | None:
    if not metric_name.strip() or not unit.strip():
        raise ValueError("metric_name and unit cannot be empty")
    selected = observations_in_window(history, window)
    metric_observations = tuple(
        observation
        for observation in selected
        if observation.metric_name == metric_name and observation.unit == unit
    )
    return aggregate_performance(metric_observations, window=window)
