from dataclasses import dataclass
from enum import Enum

from app.domain.marketing_campaign import CampaignPerformanceSnapshot


class CampaignOptimizationAction(str, Enum):
    CONTINUE = "continue"
    INCREASE_BUDGET = "increase_budget"
    DECREASE_BUDGET = "decrease_budget"
    PAUSE = "pause"


@dataclass(frozen=True)
class CampaignOptimizationPolicy:
    minimum_observations: int = 1
    target_roas: float | None = None
    maximum_cac: float | None = None
    maximum_budget_adjustment: float = 0.0
    allowed_actions: tuple[CampaignOptimizationAction, ...] = (
        CampaignOptimizationAction.CONTINUE,
    )

    def __post_init__(self) -> None:
        if self.minimum_observations < 1:
            raise ValueError("minimum_observations must be positive")
        if self.target_roas is not None and self.target_roas < 0:
            raise ValueError("target_roas cannot be negative")
        if self.maximum_cac is not None and self.maximum_cac < 0:
            raise ValueError("maximum_cac cannot be negative")
        if self.maximum_budget_adjustment < 0:
            raise ValueError("maximum_budget_adjustment cannot be negative")
        if not self.allowed_actions:
            raise ValueError("at least one optimization action is required")


@dataclass(frozen=True)
class CampaignOptimizationRecommendation:
    campaign_id: str
    action: CampaignOptimizationAction
    current_budget: float
    recommended_budget: float
    sufficient_evidence: bool
    rationale: str

    def __post_init__(self) -> None:
        if not self.campaign_id:
            raise ValueError("campaign_id cannot be empty")
        if self.current_budget < 0:
            raise ValueError("current_budget cannot be negative")
        if self.recommended_budget < 0:
            raise ValueError("recommended_budget cannot be negative")
        if not self.rationale:
            raise ValueError("rationale cannot be empty")


def recommend_campaign_optimization(
    *,
    campaign_id: str,
    current_budget: float,
    budget_limit: float,
    policy: CampaignOptimizationPolicy,
    observation_count: int,
    performance: CampaignPerformanceSnapshot,
) -> CampaignOptimizationRecommendation:
    if not campaign_id:
        raise ValueError("campaign_id cannot be empty")
    if current_budget < 0 or budget_limit < 0:
        raise ValueError("budgets cannot be negative")
    if current_budget > budget_limit:
        raise ValueError("current_budget cannot exceed budget_limit")
    if observation_count < 0:
        raise ValueError("observation_count cannot be negative")

    if observation_count < policy.minimum_observations:
        return CampaignOptimizationRecommendation(
            campaign_id=campaign_id,
            action=CampaignOptimizationAction.CONTINUE,
            current_budget=current_budget,
            recommended_budget=current_budget,
            sufficient_evidence=False,
            rationale="insufficient observations for optimization",
        )

    action = CampaignOptimizationAction.CONTINUE
    recommended_budget = current_budget
    rationale = "performance remains within the configured optimization policy"

    if (
        policy.target_roas is not None
        and performance.roas is not None
        and performance.roas < policy.target_roas
    ):
        if CampaignOptimizationAction.DECREASE_BUDGET in policy.allowed_actions:
            action = CampaignOptimizationAction.DECREASE_BUDGET
            recommended_budget = max(0.0, current_budget - policy.maximum_budget_adjustment)
            rationale = "ROAS is below the configured target"
        elif CampaignOptimizationAction.PAUSE in policy.allowed_actions:
            action = CampaignOptimizationAction.PAUSE
            rationale = "ROAS is below the configured target"

    if (
        policy.maximum_cac is not None
        and performance.customer_acquisition_cost is not None
        and performance.customer_acquisition_cost > policy.maximum_cac
    ):
        if CampaignOptimizationAction.PAUSE in policy.allowed_actions:
            action = CampaignOptimizationAction.PAUSE
            recommended_budget = current_budget
            rationale = "CAC is above the configured maximum"
        elif CampaignOptimizationAction.DECREASE_BUDGET in policy.allowed_actions:
            action = CampaignOptimizationAction.DECREASE_BUDGET
            recommended_budget = max(0.0, current_budget - policy.maximum_budget_adjustment)
            rationale = "CAC is above the configured maximum"

    if (
        action == CampaignOptimizationAction.CONTINUE
        and policy.target_roas is not None
        and performance.roas is not None
        and performance.roas > policy.target_roas
        and CampaignOptimizationAction.INCREASE_BUDGET in policy.allowed_actions
    ):
        increase = min(policy.maximum_budget_adjustment, budget_limit - current_budget)
        if increase > 0:
            recommended_budget = current_budget + increase
            action = CampaignOptimizationAction.INCREASE_BUDGET
            rationale = "ROAS is above the configured target"
        else:
            rationale = "ROAS is above target but the budget limit prevents an increase"

    return CampaignOptimizationRecommendation(
        campaign_id=campaign_id,
        action=action,
        current_budget=current_budget,
        recommended_budget=recommended_budget,
        sufficient_evidence=True,
        rationale=rationale,
    )
