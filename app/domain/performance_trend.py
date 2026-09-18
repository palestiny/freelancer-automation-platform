from dataclasses import dataclass

from .performance_aggregation import PerformanceAggregate
from .performance_history import PerformanceWindow


@dataclass(frozen=True)
class PerformanceTrend:
    metric_name: str
    unit: str
    current_window: PerformanceWindow
    baseline_window: PerformanceWindow
    current_average: float
    baseline_average: float
    absolute_change: float
    relative_change: float | None
    current_observation_ids: tuple[str, ...]
    baseline_observation_ids: tuple[str, ...]
    current_evidence_quality: float
    baseline_evidence_quality: float

    def __post_init__(self) -> None:
        if not self.metric_name.strip() or not self.unit.strip():
            raise ValueError("metric_name and unit cannot be empty")
        if not self.current_observation_ids or not self.baseline_observation_ids:
            raise ValueError("trend requires observations in both windows")
        if not 0 <= self.current_evidence_quality <= 100:
            raise ValueError("current_evidence_quality must be between 0 and 100")
        if not 0 <= self.baseline_evidence_quality <= 100:
            raise ValueError("baseline_evidence_quality must be between 0 and 100")


def compare_performance(
    *,
    current: PerformanceAggregate | None,
    baseline: PerformanceAggregate | None,
) -> PerformanceTrend | None:
    """Produce a descriptive comparison between two compatible aggregates."""

    if current is None or baseline is None:
        return None

    if (
        current.business_id != baseline.business_id
        or current.metric_name != baseline.metric_name
        or current.unit != baseline.unit
    ):
        raise ValueError("current and baseline must share business, metric, and unit")

    absolute_change = current.actual_average - baseline.actual_average
    relative_change = (
        absolute_change / baseline.actual_average
        if baseline.actual_average != 0
        else None
    )

    return PerformanceTrend(
        metric_name=current.metric_name,
        unit=current.unit,
        current_window=current.window,
        baseline_window=baseline.window,
        current_average=current.actual_average,
        baseline_average=baseline.actual_average,
        absolute_change=absolute_change,
        relative_change=relative_change,
        current_observation_ids=current.observation_ids,
        baseline_observation_ids=baseline.observation_ids,
        current_evidence_quality=current.average_evidence_quality,
        baseline_evidence_quality=baseline.average_evidence_quality,
    )
