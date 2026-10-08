from datetime import datetime

from app.domain.opportunity_intelligence import OpportunityEvaluation
from app.domain.opportunity_prioritization import (
    OpportunityPriorityDecision,
    PrioritizationPolicy,
    prioritize_opportunity,
)


class OpportunityPrioritizer:
    """Deterministic, non-executing prioritization over a canonical evaluation."""

    def prioritize(
        self,
        *,
        opportunity_ref: str,
        evaluation_ref: str,
        evaluation: OpportunityEvaluation,
        policy: PrioritizationPolicy,
        evaluated_at: datetime,
    ) -> OpportunityPriorityDecision:
        return prioritize_opportunity(
            opportunity_ref=opportunity_ref,
            evaluation_ref=evaluation_ref,
            evaluation=evaluation,
            policy=policy,
            evaluated_at=evaluated_at,
        )
