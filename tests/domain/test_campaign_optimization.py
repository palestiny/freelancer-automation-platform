import pytest

from app.domain.campaign_optimization import (
    CampaignOptimizationAction,
    CampaignOptimizationPolicy,
    recommend_campaign_optimization,
)
from app.domain.marketing_campaign import CampaignPerformanceSnapshot


def performance(*, spend=100, revenue=300, conversions=10):
    return CampaignPerformanceSnapshot(
        impressions=1000,
        clicks=100,
        leads=20,
        conversions=conversions,
        spend=spend,
        revenue=revenue,
    )


def test_insufficient_evidence_does_not_change_budget():
    policy = CampaignOptimizationPolicy(
        minimum_observations=3,
        maximum_budget_adjustment=50,
        allowed_actions=(CampaignOptimizationAction.INCREASE_BUDGET,),
    )
    result = recommend_campaign_optimization(
        campaign_id="campaign-1", current_budget=100, budget_limit=500,
        policy=policy, observation_count=2, performance=performance(),
    )
    assert result.action == CampaignOptimizationAction.CONTINUE
    assert result.sufficient_evidence is False
    assert result.recommended_budget == 100


def test_low_roas_can_reduce_budget():
    policy = CampaignOptimizationPolicy(
        target_roas=4, maximum_budget_adjustment=25,
        allowed_actions=(CampaignOptimizationAction.DECREASE_BUDGET,),
    )
    result = recommend_campaign_optimization(
        campaign_id="campaign-1", current_budget=100, budget_limit=500,
        policy=policy, observation_count=1, performance=performance(),
    )
    assert result.action == CampaignOptimizationAction.DECREASE_BUDGET
    assert result.recommended_budget == 75


def test_high_roas_increase_never_exceeds_budget_limit():
    policy = CampaignOptimizationPolicy(
        target_roas=2, maximum_budget_adjustment=100,
        allowed_actions=(CampaignOptimizationAction.INCREASE_BUDGET,),
    )
    result = recommend_campaign_optimization(
        campaign_id="campaign-1", current_budget=450, budget_limit=500,
        policy=policy, observation_count=1, performance=performance(),
    )
    assert result.action == CampaignOptimizationAction.INCREASE_BUDGET
    assert result.recommended_budget == 500


def test_high_cac_can_pause():
    policy = CampaignOptimizationPolicy(
        maximum_cac=8, allowed_actions=(CampaignOptimizationAction.PAUSE,),
    )
    result = recommend_campaign_optimization(
        campaign_id="campaign-1", current_budget=100, budget_limit=500,
        policy=policy, observation_count=1, performance=performance(),
    )
    assert result.action == CampaignOptimizationAction.PAUSE
    assert result.recommended_budget == 100


@pytest.mark.parametrize(
    "kwargs",
    [
        {"minimum_observations": 0},
        {"target_roas": -1},
        {"maximum_cac": -1},
        {"maximum_budget_adjustment": -1},
        {"allowed_actions": ()},
    ],
)
def test_policy_rejects_invalid_values(**kwargs):
    with pytest.raises(ValueError):
        CampaignOptimizationPolicy(**kwargs)


def test_recommendation_requires_budget_within_limit():
    with pytest.raises(ValueError):
        recommend_campaign_optimization(
            campaign_id="campaign-1", current_budget=600, budget_limit=500,
            policy=CampaignOptimizationPolicy(), observation_count=1,
            performance=performance(),
        )
