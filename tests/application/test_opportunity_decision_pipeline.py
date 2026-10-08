from datetime import datetime, timezone

import pytest

from app.application.opportunity_decision_pipeline import (
    OpportunityDecisionPipeline,
)
from app.domain.opportunity import Opportunity
from app.domain.opportunity_intelligence import (
    CriterionEvaluation,
    CriterionId,
    CriterionOutcome,
    EvaluationPolicy,
    OpportunityEvaluation,
    OverallOutcome,
)
from app.domain.opportunity_prioritization import (
    OpportunityPriorityDecision,
    PrioritizationOutcome,
    PrioritizationPolicy,
    PriorityTierRule,
)

NOW = datetime(2026, 10, 9, tzinfo=timezone.utc)


def make_opportunity():
    return Opportunity(
        source_platform="synthetic",
        source_opportunity_id="job-17",
        title="Build a dashboard",
        description="A synthetic test opportunity.",
    )


def evaluation(outcome=OverallOutcome.QUALIFIED):
    return OpportunityEvaluation(
        policy_id="evaluation-policy",
        policy_version="3",
        criteria=(
            CriterionEvaluation(
                policy_id="evaluation-policy",
                policy_version="3",
                criterion_id=CriterionId.ELIGIBILITY,
                outcome=CriterionOutcome.PASS,
                evidence_refs=("eligibility.status", "economic.profit"),
            ),
        ),
        overall_outcome=outcome,
    )


def evaluation_policy():
    return EvaluationPolicy(
        policy_id="evaluation-policy",
        policy_version="3",
        required_criteria=(CriterionId.ELIGIBILITY,),
    )


def prioritization_policy():
    return PrioritizationPolicy(
        policy_id="priority-policy",
        policy_version="1",
        mandatory_evidence_refs=("eligibility.status",),
        tier_rules=(
            PriorityTierRule(
                rule_id="profit-evidence",
                tier_id="P1",
                required_evidence_refs=("eligibility.status", "economic.profit"),
            ),
        ),
    )


class StubEvaluator:
    def __init__(self, result):
        self.result = result
        self.calls = []

    def evaluate(self, opportunity, policy):
        self.calls.append((opportunity, policy))
        return self.result


class StubPrioritizer:
    def __init__(self):
        self.calls = []
        self.result = None

    def prioritize(self, **kwargs):
        from app.application.opportunity_prioritizer import OpportunityPrioritizer

        self.calls.append(kwargs)
        self.result = OpportunityPrioritizer().prioritize(**kwargs)
        return self.result


def test_pipeline_evaluates_once_and_prioritizes_the_exact_evaluation_once():
    source_evaluation = evaluation()
    evaluator = StubEvaluator(source_evaluation)
    prioritizer = StubPrioritizer()
    pipeline = OpportunityDecisionPipeline(evaluator, prioritizer)

    result = pipeline.run(
        opportunity=make_opportunity(),
        evaluation_policy=evaluation_policy(),
        prioritization_policy=prioritization_policy(),
        opportunity_ref="synthetic:job-17",
        evaluation_ref="evaluation:job-17:3",
        evaluated_at=NOW,
    )

    assert len(evaluator.calls) == 1
    assert evaluator.calls[0][0].source_opportunity_id == "job-17"
    assert result.evaluation is source_evaluation
    assert len(prioritizer.calls) == 1
    assert prioritizer.calls[0]["evaluation"] is source_evaluation
    assert prioritizer.calls[0]["opportunity_ref"] == "synthetic:job-17"
    assert prioritizer.calls[0]["evaluation_ref"] == "evaluation:job-17:3"
    assert result.priority_decision is prioritizer.result


@pytest.mark.parametrize(
    ("overall", "expected"),
    [
        (OverallOutcome.NOT_QUALIFIED, PrioritizationOutcome.BLOCKED),
        (OverallOutcome.REVIEW_REQUIRED, PrioritizationOutcome.REVIEW_REQUIRED),
    ],
)
def test_pipeline_preserves_blocked_and_review_only_outcomes(overall, expected):
    from app.application.opportunity_prioritizer import OpportunityPrioritizer

    pipeline = OpportunityDecisionPipeline(
        StubEvaluator(evaluation(overall)),
        OpportunityPrioritizer(),
    )
    result = pipeline.run(
        opportunity=make_opportunity(),
        evaluation_policy=evaluation_policy(),
        prioritization_policy=prioritization_policy(),
        opportunity_ref="synthetic:job-17",
        evaluation_ref="evaluation:job-17:3",
        evaluated_at=NOW,
    )

    assert result.priority_decision.outcome is expected
    assert result.priority_decision.tier_id is None


@pytest.mark.parametrize(
    ("opportunity_ref", "evaluation_ref"),
    [
        ("", "evaluation:job-17:3"),
        ("synthetic:job-17", " "),
    ],
)
def test_pipeline_rejects_empty_identity_references_before_evaluation(
    opportunity_ref, evaluation_ref
):
    evaluator = StubEvaluator(evaluation())
    pipeline = OpportunityDecisionPipeline(evaluator, StubPrioritizer())

    with pytest.raises(ValueError, match="reference"):
        pipeline.run(
            opportunity=make_opportunity(),
            evaluation_policy=evaluation_policy(),
            prioritization_policy=prioritization_policy(),
            opportunity_ref=opportunity_ref,
            evaluation_ref=evaluation_ref,
            evaluated_at=NOW,
        )
    assert evaluator.calls == []


def test_pipeline_rejects_naive_timestamp_before_evaluation():
    evaluator = StubEvaluator(evaluation())
    pipeline = OpportunityDecisionPipeline(evaluator, StubPrioritizer())

    with pytest.raises(ValueError, match="timezone-aware"):
        pipeline.run(
            opportunity=make_opportunity(),
            evaluation_policy=evaluation_policy(),
            prioritization_policy=prioritization_policy(),
            opportunity_ref="synthetic:job-17",
            evaluation_ref="evaluation:job-17:3",
            evaluated_at=datetime(2026, 10, 9),
        )
    assert evaluator.calls == []


def test_pipeline_returns_canonical_evaluation_and_immutable_combined_result():
    from dataclasses import FrozenInstanceError
    from app.application.opportunity_prioritizer import OpportunityPrioritizer

    pipeline = OpportunityDecisionPipeline(
        StubEvaluator(evaluation()),
        OpportunityPrioritizer(),
    )
    result = pipeline.run(
        opportunity=make_opportunity(),
        evaluation_policy=evaluation_policy(),
        prioritization_policy=prioritization_policy(),
        opportunity_ref="synthetic:job-17",
        evaluation_ref="evaluation:job-17:3",
        evaluated_at=NOW,
    )

    assert result.evaluation.policy_id == "evaluation-policy"
    assert result.evaluation.policy_version == "3"
    assert result.priority_decision.evaluation_policy_version == "3"
    assert result.priority_decision.prioritization_policy_version == "1"
    assert result.priority_decision.criterion_snapshots[0].evidence_refs == (
        "eligibility.status",
        "economic.profit",
    )
    with pytest.raises(FrozenInstanceError):
        result.evaluation_ref = "mutated"
