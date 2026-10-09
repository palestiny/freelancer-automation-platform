"""Reusable provider-neutral conformance cases for opportunity history adapters.

A concrete adapter test module should call these cases with a zero-argument
factory returning a fresh repository. Keep provider-specific concurrency,
transaction, durability, backup, and recovery tests separate.
"""
from datetime import datetime, timezone
from decimal import Decimal
from typing import Callable

import pytest

from app.application.opportunity_decision_pipeline import OpportunityDecisionResult
from app.application.opportunity_history_repository import (
    OpportunityHistoryRepository,
    RecordConflict,
    RecordNotFound,
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

RepositoryFactory = Callable[[], OpportunityHistoryRepository]
UTC = timezone.utc


def make_opportunity(title: str = "Contract fixture") -> Opportunity:
    return Opportunity(
        source_platform="synthetic",
        source_opportunity_id="contract-job-1",
        title=title,
        description="Provider-neutral repository contract fixture",
        budget_min=Decimal("100"),
        budget_max=Decimal("250"),
        budget_currency="USD",
    )


def make_policies() -> tuple[EvaluationPolicy, PrioritizationPolicy]:
    evaluation_policy = EvaluationPolicy(
        policy_id="contract-evaluation-policy",
        policy_version="1",
        required_criteria=(CriterionId.ELIGIBILITY,),
    )
    prioritization_policy = PrioritizationPolicy(
        policy_id="contract-priority-policy",
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


def make_result(
    opportunity_id: str = "contract-opp-1",
    evaluation_ref: str = "contract-eval-1",
) -> OpportunityDecisionResult:
    evaluation_policy, prioritization_policy = make_policies()
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
                rationale="Contract fixture",
            ),
        ),
        overall_outcome=OverallOutcome.QUALIFIED,
    )
    decision = OpportunityPriorityDecision(
        opportunity_ref=opportunity_id,
        evaluation_ref=evaluation_ref,
        evaluation_policy_id=evaluation_policy.policy_id,
        evaluation_policy_version=evaluation_policy.policy_version,
        prioritization_policy_id=prioritization_policy.policy_id,
        prioritization_policy_version=prioritization_policy.policy_version,
        outcome=PrioritizationOutcome.PRIORITIZED,
        tier_id="P1",
        matched_rule_ids=("eligible",),
        reasons=("contract rule matched",),
        evidence_refs=("eligibility.status",),
        criterion_snapshots=(),
        evaluated_at=datetime(2026, 1, 1, tzinfo=UTC),
    )
    return OpportunityDecisionResult(
        opportunity_ref=opportunity_id,
        evaluation_ref=evaluation_ref,
        evaluation=evaluation,
        priority_decision=decision,
    )


def assert_revision_identity_idempotency_conflict_and_history(
    repository_factory: RepositoryFactory,
) -> None:
    repository = repository_factory()
    first = repository.save_opportunity_revision(
        "contract-opp-1", "revision-1", make_opportunity()
    )
    replay = repository.save_opportunity_revision(
        "contract-opp-1", "revision-1", make_opportunity()
    )
    assert replay == first
    assert replay.recorded_at == first.recorded_at
    assert first.recorded_at.tzinfo is not None
    assert first.recorded_at.utcoffset() is not None

    with pytest.raises(RecordConflict):
        repository.save_opportunity_revision(
            "contract-opp-1", "revision-1", make_opportunity("changed")
        )
    assert repository.get_opportunity_revision("contract-opp-1", "revision-1") == first

    second = repository.save_opportunity_revision(
        "contract-opp-1", "revision-0", make_opportunity("second revision")
    )

    # Revision identity is scoped to its parent opportunity.
    other = repository.save_opportunity_revision(
        "contract-opp-2", "revision-1", make_opportunity("other opportunity")
    )
    assert other.revision_id == first.revision_id
    assert other.opportunity_id != first.opportunity_id

    history = repository.list_opportunity_revisions("contract-opp-1")
    assert first in history and second in history
    assert list(history) == sorted(
        history, key=lambda record: (record.recorded_at, record.revision_id)
    )
    # "Latest" follows the documented ordering tuple; an ID is only a
    # deterministic tie-breaker when recorded timestamps are equal.
    assert repository.get_latest_opportunity_revision("contract-opp-1") == max(
        history, key=lambda record: (record.recorded_at, record.revision_id)
    )


def assert_decision_requires_revision_and_is_idempotent_but_immutable(
    repository_factory: RepositoryFactory,
) -> None:
    repository = repository_factory()
    evaluation_policy, prioritization_policy = make_policies()
    result = make_result()

    with pytest.raises(RecordNotFound):
        repository.save_decision(
            "contract-decision-1",
            "contract-opp-1",
            "revision-1",
            evaluation_policy,
            prioritization_policy,
            result,
        )

    repository.save_opportunity_revision(
        "contract-opp-1", "revision-1", make_opportunity()
    )
    first = repository.save_decision(
        "contract-decision-1",
        "contract-opp-1",
        "revision-1",
        evaluation_policy,
        prioritization_policy,
        result,
    )
    replay = repository.save_decision(
        "contract-decision-1",
        "contract-opp-1",
        "revision-1",
        evaluation_policy,
        prioritization_policy,
        result,
    )
    assert replay == first
    assert replay.recorded_at == first.recorded_at
    assert first.recorded_at.tzinfo is not None
    assert first.recorded_at.utcoffset() is not None
    # The persisted decision is a snapshot, not merely a pointer to live policies.
    assert first.evaluation_policy == evaluation_policy
    assert first.prioritization_policy == prioritization_policy
    assert first.result == result

    # Decision IDs are global, even when another opportunity/revision exists.
    repository.save_opportunity_revision(
        "contract-opp-2", "revision-1", make_opportunity("other opportunity")
    )
    with pytest.raises(RecordConflict):
        repository.save_decision(
            "contract-decision-1",
            "contract-opp-2",
            "revision-1",
            evaluation_policy,
            prioritization_policy,
            make_result(opportunity_id="contract-opp-2"),
        )
    assert repository.get_decision("contract-decision-1") == first

    with pytest.raises(RecordConflict):
        repository.save_decision(
            "contract-decision-1",
            "contract-opp-1",
            "revision-1",
            evaluation_policy,
            prioritization_policy,
            make_result(evaluation_ref="contract-eval-different"),
        )
    assert repository.get_decision("contract-decision-1") == first


def assert_decision_history_is_ordered_and_missing_records_are_explicit(
    repository_factory: RepositoryFactory,
) -> None:
    repository = repository_factory()
    with pytest.raises(RecordNotFound):
        repository.get_opportunity_revision("missing", "revision-1")
    with pytest.raises(RecordNotFound):
        repository.get_latest_opportunity_revision("missing")
    with pytest.raises(RecordNotFound):
        repository.get_decision("missing")

    repository.save_opportunity_revision(
        "contract-opp-1", "revision-1", make_opportunity()
    )
    evaluation_policy, prioritization_policy = make_policies()
    first_result = make_result(evaluation_ref="contract-eval-1")
    second_result = make_result(evaluation_ref="contract-eval-2")
    first = repository.save_decision(
        "contract-decision-a",
        "contract-opp-1",
        "revision-1",
        evaluation_policy,
        prioritization_policy,
        first_result,
    )
    second = repository.save_decision(
        "contract-decision-b",
        "contract-opp-1",
        "revision-1",
        evaluation_policy,
        prioritization_policy,
        second_result,
    )
    history = repository.list_decisions("contract-opp-1")
    assert first in history and second in history
    assert list(history) == sorted(
        history, key=lambda record: (record.recorded_at, record.decision_id)
    )

def assert_identity_validation_and_preservation(
    repository_factory: RepositoryFactory,
) -> None:
    repository = repository_factory()
    with pytest.raises(ValueError):
        repository.save_opportunity_revision("", "revision-1", make_opportunity())
    with pytest.raises(ValueError):
        repository.save_opportunity_revision("contract-opp-1", "  ", make_opportunity())

    record = repository.save_opportunity_revision(
        " contract-opp-1 ", "Revision-A", make_opportunity()
    )
    assert record.opportunity_id == " contract-opp-1 "
    assert record.revision_id == "Revision-A"


def assert_decision_policy_and_lineage_are_validated(
    repository_factory: RepositoryFactory,
) -> None:
    repository = repository_factory()
    repository.save_opportunity_revision(
        "contract-opp-1", "revision-1", make_opportunity()
    )
    evaluation_policy, prioritization_policy = make_policies()
    result = make_result()

    wrong_policy = PrioritizationPolicy(
        policy_id="different-policy",
        policy_version="99",
        mandatory_evidence_refs=("eligibility.status",),
        tier_rules=(
            PriorityTierRule(
                rule_id="eligible",
                tier_id="P1",
                required_evidence_refs=("eligibility.status",),
            ),
        ),
    )
    with pytest.raises(ValueError, match="policy"):
        repository.save_decision(
            "contract-decision-policy-mismatch",
            "contract-opp-1",
            "revision-1",
            evaluation_policy,
            wrong_policy,
            result,
        )

    with pytest.raises(ValueError, match="lineage|opportunity"):
        repository.save_decision(
            "contract-decision-lineage-mismatch",
            "different-opportunity",
            "revision-1",
            evaluation_policy,
            prioritization_policy,
            result,
        )

    with pytest.raises(RecordNotFound):
        repository.get_decision("contract-decision-policy-mismatch")
    with pytest.raises(RecordNotFound):
        repository.get_decision("contract-decision-lineage-mismatch")
