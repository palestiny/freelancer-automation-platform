from app.domain.opportunity import Opportunity
from app.domain.opportunity_evaluation import (
    CriterionOutcome,
    EvaluationPolicy,
    OpportunityEvaluator,
    OverallOutcome,
)


def test_budget_below_minimum_fails_eligibility():
    opportunity = Opportunity(
        source_platform="example-marketplace",
        source_opportunity_id="opp-007",
        title="Backend API",
        description="Build an API.",
        budget_min=200,
        budget_max=300,
    )
    policy = EvaluationPolicy(minimum_budget=400)

    evaluation = OpportunityEvaluator().evaluate(opportunity, policy)

    assert evaluation.criteria["eligibility"].outcome is CriterionOutcome.FAIL
    assert evaluation.overall_outcome is OverallOutcome.NOT_QUALIFIED


def test_budget_above_maximum_fails_eligibility():
    opportunity = Opportunity(
        source_platform="example-marketplace",
        source_opportunity_id="opp-008",
        title="Backend API",
        description="Build an API.",
        budget_min=1200,
        budget_max=1500,
    )
    policy = EvaluationPolicy(maximum_budget=1000)

    evaluation = OpportunityEvaluator().evaluate(opportunity, policy)

    assert evaluation.criteria["eligibility"].outcome is CriterionOutcome.FAIL
    assert evaluation.overall_outcome is OverallOutcome.NOT_QUALIFIED
