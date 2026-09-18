from app.domain.opportunity import Opportunity
from app.domain.opportunity_evaluation import (
    EvaluationPolicy,
    OpportunityEvaluator,
    CriterionOutcome,
    OverallOutcome,
)


def test_eligibility_passes_when_opportunity_satisfies_required_policy():
    opportunity = Opportunity(
        source_platform="example-marketplace",
        source_opportunity_id="opp-001",
        title="React dashboard",
        description="Build a React dashboard.",
        project_type="web_development",
        required_capabilities=frozenset({"react"}),
        budget_min=500,
        budget_max=800,
    )

    policy = EvaluationPolicy(
        allowed_project_types=frozenset({"web_development"}),
        required_capabilities=frozenset({"react"}),
        minimum_budget=400,
        maximum_budget=1000,
    )

    evaluation = OpportunityEvaluator().evaluate(opportunity, policy)

    assert evaluation.overall_outcome is OverallOutcome.QUALIFIED
    assert evaluation.criteria["eligibility"].outcome is CriterionOutcome.PASS
