from dataclasses import replace

from app.domain.opportunity import Opportunity
from app.domain.opportunity_evaluation import (
    CriterionOutcome,
    EvaluationPolicy,
    OpportunityEvaluator,
    OverallOutcome,
)


def test_criterion_evidence_is_preserved():
    opportunity = Opportunity(
        source_platform="example-marketplace",
        source_opportunity_id="opp-004",
        title="React dashboard",
        description="Build a React dashboard.",
        project_type="web_development",
    )
    policy = EvaluationPolicy(
        allowed_project_types=frozenset({"web_development"}),
    )

    evaluation = OpportunityEvaluator().evaluate(opportunity, policy)

    assert evaluation.criteria["eligibility"].outcome is CriterionOutcome.PASS
    assert "project_type satisfies policy" in evaluation.criteria["eligibility"].evidence


def test_evaluation_does_not_change_opportunity_identity():
    opportunity = Opportunity(
        source_platform="example-marketplace",
        source_opportunity_id="opp-005",
        title="React dashboard",
        description="Build a React dashboard.",
        project_type="web_development",
    )
    before = replace(opportunity)

    policy = EvaluationPolicy(
        allowed_project_types=frozenset({"web_development"}),
    )

    OpportunityEvaluator().evaluate(opportunity, policy)

    assert opportunity == before
    assert opportunity.source_platform == "example-marketplace"
    assert opportunity.source_opportunity_id == "opp-005"


def test_same_opportunity_can_be_evaluated_against_different_policies():
    opportunity = Opportunity(
        source_platform="example-marketplace",
        source_opportunity_id="opp-006",
        title="React dashboard",
        description="Build a React dashboard.",
        project_type="web_development",
    )

    qualifying_policy = EvaluationPolicy(
        allowed_project_types=frozenset({"web_development"}),
    )
    rejecting_policy = EvaluationPolicy(
        allowed_project_types=frozenset({"mobile_development"}),
    )

    evaluator = OpportunityEvaluator()

    first = evaluator.evaluate(opportunity, qualifying_policy)
    second = evaluator.evaluate(opportunity, rejecting_policy)

    assert first.overall_outcome is OverallOutcome.QUALIFIED
    assert second.overall_outcome is OverallOutcome.NOT_QUALIFIED
    assert opportunity.source_opportunity_id == "opp-006"
