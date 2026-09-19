from dataclasses import dataclass
from enum import Enum
from datetime import datetime

from .economic_performance_aggregation import EconomicPerformanceWindow

from .economic_health import EconomicHealthEvidence


class EconomicStabilityEligibilityReason(str, Enum):
    ELIGIBLE = "eligible"
    INSUFFICIENT_OBSERVATIONS = "insufficient_observations"
    PROFITABILITY_RATE_BELOW_THRESHOLD = "profitability_rate_below_threshold"
    AVERAGE_PROFIT_BELOW_THRESHOLD = "average_profit_below_threshold"
    INSUFFICIENT_VARIABILITY_DATA = "insufficient_variability_data"
    PROFIT_VARIABILITY_ABOVE_THRESHOLD = "profit_variability_above_threshold"


@dataclass(frozen=True)
class EconomicStabilityPolicy:
    minimum_observations: int
    minimum_profitable_outcome_rate: float
    minimum_average_actual_profit: float
    maximum_profit_stddev_ratio: float

    def __post_init__(self) -> None:
        if self.minimum_observations <= 0:
            raise ValueError("minimum_observations must be greater than zero")
        if not 0 <= self.minimum_profitable_outcome_rate <= 1:
            raise ValueError("minimum_profitable_outcome_rate must be between 0 and 1")
        if self.minimum_average_actual_profit < 0:
            raise ValueError("minimum_average_actual_profit cannot be negative")
        if self.maximum_profit_stddev_ratio < 0:
            raise ValueError("maximum_profit_stddev_ratio cannot be negative")


@dataclass(frozen=True)
class EconomicStabilityAssessment:
    business_id: str
    window: EconomicPerformanceWindow
    outcome_ids: tuple[str, ...]
    eligible: bool
    reason: EconomicStabilityEligibilityReason
    profit_stddev_ratio: float | None

    def __post_init__(self) -> None:
        if not self.business_id.strip():
            raise ValueError("business_id cannot be empty")
        if not self.outcome_ids:
            raise ValueError("outcome_ids cannot be empty")
        if len(set(self.outcome_ids)) != len(self.outcome_ids):
            raise ValueError("outcome_ids must be unique")
        if self.eligible != (self.reason is EconomicStabilityEligibilityReason.ELIGIBLE):
            raise ValueError("eligible state must match reason")
        if self.profit_stddev_ratio is not None and self.profit_stddev_ratio < 0:
            raise ValueError("profit_stddev_ratio cannot be negative")


def assess_economic_stability(
    *,
    health: EconomicHealthEvidence | None,
    policy: EconomicStabilityPolicy,
) -> EconomicStabilityAssessment:
    if health is None or health.outcome_count < policy.minimum_observations:
        return EconomicStabilityAssessment(
            business_id=health.business_id if health is not None else "unknown",
            window=health.window if health is not None else EconomicPerformanceWindow(datetime.min, datetime.min),
            outcome_ids=health.outcome_ids if health is not None else ("unknown",),
            eligible=False,
            reason=EconomicStabilityEligibilityReason.INSUFFICIENT_OBSERVATIONS,
            profit_stddev_ratio=None,
        )

    if health.profitable_outcome_rate < policy.minimum_profitable_outcome_rate:
        return EconomicStabilityAssessment(
            eligible=False,
            reason=EconomicStabilityEligibilityReason.PROFITABILITY_RATE_BELOW_THRESHOLD,
            profit_stddev_ratio=None,
        )

    if health.average_actual_profit < policy.minimum_average_actual_profit:
        return EconomicStabilityAssessment(
            eligible=False,
            reason=EconomicStabilityEligibilityReason.AVERAGE_PROFIT_BELOW_THRESHOLD,
            profit_stddev_ratio=None,
        )

    if health.sample_profit_standard_deviation is None or health.average_actual_profit <= 0:
        return EconomicStabilityAssessment(
            eligible=False,
            reason=EconomicStabilityEligibilityReason.INSUFFICIENT_VARIABILITY_DATA,
            profit_stddev_ratio=None,
        )

    ratio = health.sample_profit_standard_deviation / health.average_actual_profit
    if ratio > policy.maximum_profit_stddev_ratio:
        return EconomicStabilityAssessment(
            eligible=False,
            reason=EconomicStabilityEligibilityReason.PROFIT_VARIABILITY_ABOVE_THRESHOLD,
            profit_stddev_ratio=ratio,
        )

    return EconomicStabilityAssessment(
        business_id=health.business_id,
        window=health.window,
        outcome_ids=health.outcome_ids,
        eligible=True,
        reason=EconomicStabilityEligibilityReason.ELIGIBLE,
        profit_stddev_ratio=ratio,
    )
