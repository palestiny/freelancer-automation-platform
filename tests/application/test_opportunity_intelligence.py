from app.application.opportunity_intelligence import OpportunityIntelligenceEvaluator
from app.domain.opportunity import Opportunity
from app.domain.opportunity_intelligence import (
    CriterionEvaluation,
    CriterionId,
    CriterionOutcome,
    EvaluationPolicy,
    OverallOutcome,
)


def make_opportunity() -> Opportunity:
    return Opportunity(
        source_platform="example_marketplace",
        source_opportunity_id="synthetic-001",
        title="Build a React dashboard",
        description="Create a responsive dashboard.",
    )


def policy_for(*criteria: CriterionId) -> EvaluationPolicy:
    return EvaluationPolicy(
        policy_id="default-v1",
        policy_version="1",
        required_criteria=criteria,
    )


def result(policy: EvaluationPolicy, criterion: CriterionId, outcome: CriterionOutcome):
    return CriterionEvaluation(
        policy_id=policy.policy_id,
        policy_version=policy.policy_version,
        criterion_id=criterion,
        outcome=outcome,
        evidence_refs=("opportunity:synthetic-001",),
    )


def test_evaluates_criteria_against_explicit_policy_and_composes_qualified():
    policy = policy_for(CriterionId.ELIGIBILITY, CriterionId.REQUIREMENT_FIT)

    evaluator = OpportunityIntelligenceEvaluator(
        {
            CriterionId.ELIGIBILITY: lambda opportunity, selected_policy: result(
                selected_policy, CriterionId.ELIGIBILITY, CriterionOutcome.PASS
            ),
            CriterionId.REQUIREMENT_FIT: lambda opportunity, selected_policy: result(
                selected_policy, CriterionId.REQUIREMENT_FIT, CriterionOutcome.PASS
            ),
        }
    )

    evaluation = evaluator.evaluate(make_opportunity(), policy)

    assert evaluation.policy_id == "default-v1"
    assert evaluation.policy_version == "1"
    assert evaluation.overall_outcome is OverallOutcome.QUALIFIED
    assert [item.criterion_id for item in evaluation.criteria] == [
        CriterionId.ELIGIBILITY,
        CriterionId.REQUIREMENT_FIT,
    ]


def test_fail_has_precedence_over_insufficient_data():
    policy = policy_for(
        CriterionId.ELIGIBILITY,
        CriterionId.ECONOMIC_FIT,
        CriterionId.SUCCESS_CONFIDENCE,
    )

    evaluator = OpportunityIntelligenceEvaluator(
        {
            CriterionId.ELIGIBILITY: lambda opportunity, selected_policy: result(
                selected_policy, CriterionId.ELIGIBILITY, CriterionOutcome.PASS
            ),
            CriterionId.ECONOMIC_FIT: lambda opportunity, selected_policy: result(
                selected_policy, CriterionId.ECONOMIC_FIT, CriterionOutcome.INSUFFICIENT_DATA
            ),
            CriterionId.SUCCESS_CONFIDENCE: lambda opportunity, selected_policy: result(
                selected_policy, CriterionId.SUCCESS_CONFIDENCE, CriterionOutcome.FAIL
            ),
        }
    )

    evaluation = evaluator.evaluate(make_opportunity(), policy)

    assert evaluation.overall_outcome is OverallOutcome.NOT_QUALIFIED


def test_insufficient_data_requires_review_when_no_criterion_fails():
    policy = policy_for(
        CriterionId.ELIGIBILITY,
        CriterionId.CLIENT_PROJECT_RISK,
    )

    evaluator = OpportunityIntelligenceEvaluator(
        {
            CriterionId.ELIGIBILITY: lambda opportunity, selected_policy: result(
                selected_policy, CriterionId.ELIGIBILITY, CriterionOutcome.PASS
            ),
            CriterionId.CLIENT_PROJECT_RISK: lambda opportunity, selected_policy: result(
                selected_policy,
                CriterionId.CLIENT_PROJECT_RISK,
                CriterionOutcome.INSUFFICIENT_DATA,
            ),
        }
    )

    evaluation = evaluator.evaluate(make_opportunity(), policy)

    assert evaluation.overall_outcome is OverallOutcome.REVIEW_REQUIRED


def test_not_applicable_does_not_force_review():
    policy = policy_for(
        CriterionId.ELIGIBILITY,
        CriterionId.ESTIMATED_EFFORT,
    )

    evaluator = OpportunityIntelligenceEvaluator(
        {
            CriterionId.ELIGIBILITY: lambda opportunity, selected_policy: result(
                selected_policy, CriterionId.ELIGIBILITY, CriterionOutcome.PASS
            ),
            CriterionId.ESTIMATED_EFFORT: lambda opportunity, selected_policy: result(
                selected_policy,
                CriterionId.ESTIMATED_EFFORT,
                CriterionOutcome.NOT_APPLICABLE,
            ),
        }
    )

    evaluation = evaluator.evaluate(make_opportunity(), policy)

    assert evaluation.overall_outcome is OverallOutcome.QUALIFIED


def test_missing_evidence_is_preserved_in_criterion_result():
    policy = policy_for(CriterionId.ECONOMIC_FIT)

    def evaluate_economic(opportunity, selected_policy):
        return CriterionEvaluation(
            policy_id=selected_policy.policy_id,
            policy_version=selected_policy.policy_version,
            criterion_id=CriterionId.ECONOMIC_FIT,
            outcome=CriterionOutcome.INSUFFICIENT_DATA,
            evidence_refs=(),
            missing_evidence=("budget_currency", "budget_max"),
            uncertainty=("budget is unavailable",),
        )

    evaluator = OpportunityIntelligenceEvaluator(
        {CriterionId.ECONOMIC_FIT: evaluate_economic}
    )

    evaluation = evaluator.evaluate(make_opportunity(), policy)

    criterion = evaluation.criteria[0]
    assert criterion.outcome is CriterionOutcome.INSUFFICIENT_DATA
    assert criterion.missing_evidence == ("budget_currency", "budget_max")
    assert criterion.uncertainty == ("budget is unavailable",)


def test_policy_version_is_part_of_the_evaluation_identity():
    policy = policy_for(CriterionId.ELIGIBILITY)

    evaluator = OpportunityIntelligenceEvaluator(
        {
            CriterionId.ELIGIBILITY: lambda opportunity, selected_policy: result(
                selected_policy, CriterionId.ELIGIBILITY, CriterionOutcome.PASS
            )
        }
    )

    evaluation = evaluator.evaluate(make_opportunity(), policy)

    assert evaluation.policy_id == policy.policy_id
    assert evaluation.policy_version == policy.policy_version


def test_evaluator_rejects_result_for_wrong_policy_or_criterion():
    policy = policy_for(CriterionId.ELIGIBILITY)

    evaluator = OpportunityIntelligenceEvaluator(
        {
            CriterionId.ELIGIBILITY: lambda opportunity, selected_policy: CriterionEvaluation(
                policy_id="other-policy",
                policy_version=selected_policy.policy_version,
                criterion_id=CriterionId.ELIGIBILITY,
                outcome=CriterionOutcome.PASS,
            )
        }
    )

    try:
        evaluator.evaluate(make_opportunity(), policy)
    except ValueError as exc:
        assert "policy identity" in str(exc)
    else:
        raise AssertionError("mismatched policy result must be rejected")
