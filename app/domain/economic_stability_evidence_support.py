from dataclasses import dataclass

from .economic_health import EconomicHealthEvidence
from .economic_stability_policy import EconomicStabilityAssessment


@dataclass(frozen=True)
class EconomicStabilityEvidenceSupport:
    business_id: str
    window: object
    outcome_ids: tuple[str, ...]
    profitable_outcome_rate: float
    average_actual_profit: float
    minimum_actual_profit: float
    maximum_actual_profit: float
    profit_stddev_ratio: float | None
    stability_eligible: bool

    def __post_init__(self) -> None:
        if not self.business_id.strip():
            raise ValueError("business_id cannot be empty")
        if not self.outcome_ids:
            raise ValueError("outcome_ids cannot be empty")
        if len(set(self.outcome_ids)) != len(self.outcome_ids):
            raise ValueError("outcome_ids must be unique")
        if not 0 <= self.profitable_outcome_rate <= 1:
            raise ValueError("profitable_outcome_rate must be between 0 and 1")
        if self.profit_stddev_ratio is not None and self.profit_stddev_ratio < 0:
            raise ValueError("profit_stddev_ratio cannot be negative")


def compose_economic_stability_evidence(
    *,
    health: EconomicHealthEvidence,
    stability: EconomicStabilityAssessment,
) -> EconomicStabilityEvidenceSupport:
    if (
        health.business_id != stability.business_id
        or health.window != stability.window
        or health.outcome_ids != stability.outcome_ids
    ):
        raise ValueError("health and stability context must match")

    return EconomicStabilityEvidenceSupport(
        business_id=health.business_id,
        window=health.window,
        outcome_ids=health.outcome_ids,
        profitable_outcome_rate=health.profitable_outcome_rate,
        average_actual_profit=health.average_actual_profit,
        minimum_actual_profit=health.minimum_actual_profit,
        maximum_actual_profit=health.maximum_actual_profit,
        profit_stddev_ratio=stability.profit_stddev_ratio,
        stability_eligible=stability.eligible,
    )
