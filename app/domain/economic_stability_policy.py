from dataclasses import dataclass
from enum import Enum

from .economic_health import EconomicHealthEvidence
from .economic_performance_aggregation import EconomicPerformanceWindow


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
    business_id: str | None
    window: EconomicPerformanceWindow | None
    outcome_ids: tuple[str, ...]
    eligible: bool
    reason: EconomicStabilityEligibilityReason
    profit_stddev_ratio: float | None

    def __post_init__(self) -> None:
        if self.business_id is not None and not self.business_id.strip():
            raise ValueError("business_id cannot be empty")
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
            business_id=health.business_id if health is not None else None,
            window=health.window if health is not None else None,
            outcome_ids=health.outcome_ids if health is not None else (),
            eligible=False,
            reason=EconomicStabilityEligibilityReason.INSUFFICIENT_OBSERVATIONS,
            profit_stddev_ratio=None,
        )

    if health.profitable_outcome_rate < policy.minimum_profitable_outcome_rate:
        return _assessment(
            health,
            False,
            EconomicStabilityEligibilityReason.PROFITABILITY_RATE_BELOW_THRESHOLD,
        )

    if health.average_actual_profit < policy.minimum_average_actual_profit:
        return _assessment(
            health,
            False,
            EconomicStabilityEligibilityReason.AVERAGE_PROFIT_BELOW_THRESHOLD,
        )

    if health.sample_profit_standard_deviation is None or health.average_actual_profit <= 0:
        return _assessment(
            health,
            False,
            EconomicStabilityEligibilityReason.INSUFFICIENT_VARIABILITY_DATA,
        )

    ratio = health.sample_profit_standard_deviation / health.average_actual_profit
    if ratio > policy.maximum_profit_stddev_ratio:
        return _assessment(
            health,
            False,
            EconomicStabilityEligibilityReason.PROFIT_VARIABILITY_ABOVE_THRESHOLD,
            ratio,
        )

    return _assessment(
        health,
        True,
        EconomicStabilityEligibilityReason.ELIGIBLE,
        ratio,
    )


def _assessment(
    health: EconomicHealthEvidence,
    eligible: bool,
    reason: EconomicStabilityEligibilityReason,
    ratio: float | None = None,
) -> EconomicStabilityAssessment:
    return EconomicStabilityAssessment(
        business_id=health.business_id,
        window=health.window,
        outcome_ids=health.outcome_ids,
        eligible=eligible,
        reason=reason,
        profit_stddev_ratio=ratio,
    )
