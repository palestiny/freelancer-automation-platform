from datetime import datetime, timezone
from decimal import Decimal

import pytest

from app.application.opportunity_decision_pipeline import OpportunityDecisionResult
from app.application.opportunity_history_service import OpportunityHistoryService
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
from app.infrastructure.persistence.in_memory_opportunity_history_repository import (
    InMemoryOpportunityHistoryRepository,
    RecordNotFound,
)

NOW = datetime(2026, 10, 9, 10, 0, tzinfo=timezone.utc)


def make_opportunity():
    return Opportunity(
        source_platform="synthetic",
        source_opportunity_id="job-17",
        title="Persisted source snapshot",
        description="Must be the exact object evaluated",
        budget_min=Decimal("100"),
        budget_max=Decimal("250"),
        budget_currency="USD",
    )


def make_policies():
    evaluation_policy = EvaluationPolicy(
        policy_id="evaluation-policy",
        policy_version="3",
        required_criteria=(CriterionId.ELIGIBILITY,),
    )
    prioritization_policy = PrioritizationPolicy(
        policy_id="priority-policy",
        policy_version="1",
        mandatory_evidence_refs=("eligibility.status",),
        tier_rules=(
            PriorityTierRule(
                rule_id="eligible",
                tier_id="P1",
                required_evidence_refs=("eligibility.status",),
            ),
        ),
    )
    return evaluation_policy, prioritization_policy


class RecordingPipeline:
    def __init__(self):
        self.calls = []

    def run(self, **kwargs):
        self.calls.append(kwargs)
        evaluation_policy = kwargs["evaluation_policy"]
        prioritization_policy = kwargs["prioritization_policy"]
        evaluation_ref = kwargs["evaluation_ref"]
        opportunity_ref = kwargs["opportunity_ref"]
        evaluation = OpportunityEvaluation(
            policy_id=evaluation_policy.policy_id,
            policy_version=evaluation_policy.policy_version,
            criteria=(
                CriterionEvaluation(
                    policy_id=evaluation_policy.policy_id,
                    policy_version=evaluation_policy.policy_version,
                    criterion_id=CriterionId.ELIGIBILITY,
                    outcome=CriterionOutcome.PASS,
                    evidence_refs=("eligibility.status",),
                    missing_evidence=(),
                    uncertainty=(),
                    rationale="Synthetic test",
                ),
            ),
            overall_outcome=OverallOutcome.QUALIFIED,
        )
        decision = OpportunityPriorityDecision(
            opportunity_ref=opportunity_ref,
            evaluation_ref=evaluation_ref,
            evaluation_policy_id=evaluation_policy.policy_id,
            evaluation_policy_version=evaluation_policy.policy_version,
            prioritization_policy_id=prioritization_policy.policy_id,
            prioritization_policy_version=prioritization_policy.policy_version,
            outcome=PrioritizationOutcome.PRIORITIZED,
            tier_id="P1",
            matched_rule_ids=("eligible",),
            reasons=("tier rule matched: eligible",),
            evidence_refs=("eligibility.status",),
            criterion_snapshots=(),
            evaluated_at=kwargs["evaluated_at"],
        )
        return OpportunityDecisionResult(
            opportunity_ref=opportunity_ref,
            evaluation_ref=evaluation_ref,
            evaluation=evaluation,
            priority_decision=decision,
        )


def test_service_evaluates_the_exact_persisted_revision_before_saving_decision():
    repository = InMemoryOpportunityHistoryRepository(clock=lambda: NOW)
    persisted_opportunity = make_opportunity()
    revision = repository.save_opportunity_revision(
        "opp-17", "rev-1", persisted_opportunity
    )
    pipeline = RecordingPipeline()
    service = OpportunityHistoryService(repository, pipeline)
    evaluation_policy, prioritization_policy = make_policies()

    record = service.evaluate_revision(
        decision_id="decision-1",
        opportunity_id="opp-17",
        revision_id="rev-1",
        evaluation_ref="eval-17",
        evaluation_policy=evaluation_policy,
        prioritization_policy=prioritization_policy,
        evaluated_at=NOW,
    )

    assert pipeline.calls[0]["opportunity"] is revision.opportunity
    assert pipeline.calls[0]["opportunity"] is persisted_opportunity
    assert record.opportunity_id == "opp-17"
    assert record.revision_id == "rev-1"
    assert record.result.evaluation_ref == "eval-17"


def test_service_does_not_evaluate_when_the_requested_revision_does_not_exist():
    repository = InMemoryOpportunityHistoryRepository(clock=lambda: NOW)
    pipeline = RecordingPipeline()
    service = OpportunityHistoryService(repository, pipeline)
    evaluation_policy, prioritization_policy = make_policies()

    with pytest.raises(RecordNotFound):
        service.evaluate_revision(
            decision_id="decision-1",
            opportunity_id="missing",
            revision_id="rev-1",
            evaluation_ref="eval-17",
            evaluation_policy=evaluation_policy,
            prioritization_policy=prioritization_policy,
            evaluated_at=NOW,
        )

    assert pipeline.calls == []
