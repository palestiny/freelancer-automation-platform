from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from .performance_aggregation import PerformanceAggregate
from .performance_baseline import PerformanceBaselinePolicy, assess_baseline
from .performance_reliability import (
    PerformanceSourceReliabilityPolicy,
    SourceReliabilityReason,
    assess_source_reliability,
)
from .performance_trend import PerformanceTrend, compare_performance


class ComparisonRejectionReason(str, Enum):
    BASELINE_NOT_ELIGIBLE = "baseline_not_eligible"
    INSUFFICIENT_CURRENT_OBSERVATIONS = "insufficient_current_observations"
    INSUFFICIENT_CURRENT_EVIDENCE_QUALITY = "insufficient_current_evidence_quality"
    INCOMPATIBLE_CONTEXT = "incompatible_context"
    OVERLAPPING_WINDOWS = "overlapping_windows"
    FUTURE_CURRENT_WINDOW = "future_current_window"
    INSUFFICIENT_CURRENT_SOURCE_RELIABILITY = "insufficient_current_source_reliability"
    MISSING_CURRENT_SOURCE_RELIABILITY_POLICY = "missing_current_source_reliability_policy"


@dataclass(frozen=True)
class PerformanceComparisonPolicy:
    minimum_current_observations: int = 3
    minimum_current_evidence_quality: float = 60
    source_reliability_policy: PerformanceSourceReliabilityPolicy | None = None

    def __post_init__(self) -> None:
        if self.minimum_current_observations <= 0:
            raise ValueError("minimum_current_observations must be greater than zero")
        if not 0 <= self.minimum_current_evidence_quality <= 100:
            raise ValueError(
                "minimum_current_evidence_quality must be between 0 and 100"
            )


@dataclass(frozen=True)
class PerformanceComparisonResult:
    trend: PerformanceTrend | None
    rejection_reason: ComparisonRejectionReason | None

    def __post_init__(self) -> None:
        if (self.trend is None) == (self.rejection_reason is None):
            raise ValueError("result must contain exactly one outcome")


def assess_performance_comparison(
    *,
    current: PerformanceAggregate | None,
    baseline: PerformanceAggregate | None,
    baseline_policy: PerformanceBaselinePolicy,
    comparison_policy: PerformanceComparisonPolicy,
    as_of: datetime,
) -> PerformanceComparisonResult:
    baseline_eligibility = assess_baseline(
        aggregate=baseline,
        policy=baseline_policy,
        as_of=as_of,
    )
    if not baseline_eligibility.eligible:
        return PerformanceComparisonResult(
            trend=None,
            rejection_reason=ComparisonRejectionReason.BASELINE_NOT_ELIGIBLE,
        )

    if current is None or current.actual_count < comparison_policy.minimum_current_observations:
        return PerformanceComparisonResult(
            trend=None,
            rejection_reason=ComparisonRejectionReason.INSUFFICIENT_CURRENT_OBSERVATIONS,
        )

    if current.window.end > as_of:
        return PerformanceComparisonResult(
            trend=None,
            rejection_reason=ComparisonRejectionReason.FUTURE_CURRENT_WINDOW,
        )

    if current.window.start < baseline.window.end:
        return PerformanceComparisonResult(
            trend=None,
            rejection_reason=ComparisonRejectionReason.OVERLAPPING_WINDOWS,
        )

    if current.average_evidence_quality < comparison_policy.minimum_current_evidence_quality:
        return PerformanceComparisonResult(
            trend=None,
            rejection_reason=ComparisonRejectionReason.INSUFFICIENT_CURRENT_EVIDENCE_QUALITY,
        )

    if comparison_policy.source_reliability_policy is not None:
        reliability = assess_source_reliability(
            aggregate=current,
            policy=comparison_policy.source_reliability_policy,
        )
        if reliability.reason is SourceReliabilityReason.INSUFFICIENT_RELIABILITY:
            return PerformanceComparisonResult(
                trend=None,
                rejection_reason=ComparisonRejectionReason.INSUFFICIENT_CURRENT_SOURCE_RELIABILITY,
            )
        if reliability.reason is SourceReliabilityReason.MISSING_SOURCE_POLICY:
            return PerformanceComparisonResult(
                trend=None,
                rejection_reason=ComparisonRejectionReason.MISSING_CURRENT_SOURCE_RELIABILITY_POLICY,
            )

    if (
        current.business_id != baseline.business_id
        or current.metric_name != baseline.metric_name
        or current.unit != baseline.unit
        or frozenset(current.source_types) != frozenset(baseline.source_types)
    ):
        return PerformanceComparisonResult(
            trend=None,
            rejection_reason=ComparisonRejectionReason.INCOMPATIBLE_CONTEXT,
        )

    return PerformanceComparisonResult(
        trend=compare_performance(current=current, baseline=baseline),
        rejection_reason=None,
    )
