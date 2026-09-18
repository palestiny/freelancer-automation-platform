from app.domain.opportunity import Opportunity
from app.domain.opportunity_evaluation import (
    CriterionOutcome,
    EvaluationPolicy,
    OpportunityEvaluator,
    OverallOutcome,
)


def test_eligibility_fails_when_required_capability_is_missing():
    opportunity = Opportunity(
        source_platform="example-marketplace",
        source_opportunity_id="opp-002",
        title="React dashboard",
        description="Build a React dashboard.",
        project_type="web_development",
        required_capabilities=frozenset(),
        budget_min=500,
        budget_max=800,
    )

    policy = EvaluationPolicy(
        allowed_project_types=frozenset({"web_development"}),
        required_capabilities=frozenset({"react"}),
    )

    evaluation = OpportunityEvaluator().evaluate(opportunity, policy)

    assert evaluation.overall_outcome is OverallOutcome.NOT_QUALIFIED
    assert evaluation.criteria["eligibility"].outcome is CriterionOutcome.FAIL


def test_missing_eligibility_evidence_requires_review():
    opportunity = Opportunity(
        source_platform="example-marketplace",
        source_opportunity_id="opp-003",
        title="Unclassified project",
        description="Project with no known type.",
        project_type=None,
    )

    policy = EvaluationPolicy(
        allowed_project_types=frozenset({"web_development"}),
    )

    evaluation = OpportunityEvaluator().evaluate(opportunity, policy)

    assert evaluation.overall_outcome is OverallOutcome.REVIEW_REQUIRED
    assert (
        evaluation.criteria["eligibility"].outcome
        is CriterionOutcome.INSUFFICIENT_DATA
    )
