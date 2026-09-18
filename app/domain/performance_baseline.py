from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum

from .performance_aggregation import PerformanceAggregate


class BaselineEligibilityReason(str, Enum):
    ELIGIBLE = "eligible"
    INSUFFICIENT_OBSERVATIONS = "insufficient_observations"
    INSUFFICIENT_EVIDENCE_QUALITY = "insufficient_evidence_quality"
    STALE_BASELINE = "stale_baseline"
    FUTURE_BASELINE = "future_baseline"


@dataclass(frozen=True)
class PerformanceBaselinePolicy:
    minimum_observations: int = 3
    minimum_average_evidence_quality: float = 60
    maximum_age: timedelta = timedelta(days=30)

    def __post_init__(self) -> None:
        if self.minimum_observations <= 0:
            raise ValueError("minimum_observations must be greater than zero")
        if not 0 <= self.minimum_average_evidence_quality <= 100:
            raise ValueError(
                "minimum_average_evidence_quality must be between 0 and 100"
            )
        if self.maximum_age <= timedelta(0):
            raise ValueError("maximum_age must be greater than zero")


@dataclass(frozen=True)
class BaselineEligibility:
    eligible: bool
    reason: BaselineEligibilityReason


def assess_baseline(
    *,
    aggregate: PerformanceAggregate | None,
    policy: PerformanceBaselinePolicy,
    as_of: datetime,
) -> BaselineEligibility:
    if aggregate is None:
        return BaselineEligibility(
            eligible=False,
            reason=BaselineEligibilityReason.INSUFFICIENT_OBSERVATIONS,
        )

    if aggregate.actual_count < policy.minimum_observations:
        return BaselineEligibility(
            eligible=False,
            reason=BaselineEligibilityReason.INSUFFICIENT_OBSERVATIONS,
        )

    if aggregate.average_evidence_quality < policy.minimum_average_evidence_quality:
        return BaselineEligibility(
            eligible=False,
            reason=BaselineEligibilityReason.INSUFFICIENT_EVIDENCE_QUALITY,
        )

    if aggregate.window.end > as_of:
        return BaselineEligibility(
            eligible=False,
            reason=BaselineEligibilityReason.FUTURE_BASELINE,
        )

    if as_of - aggregate.window.end > policy.maximum_age:
        return BaselineEligibility(
            eligible=False,
            reason=BaselineEligibilityReason.STALE_BASELINE,
        )

    return BaselineEligibility(
        eligible=True,
        reason=BaselineEligibilityReason.ELIGIBLE,
    )
