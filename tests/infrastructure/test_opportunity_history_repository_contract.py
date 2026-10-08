from datetime import datetime, timedelta, timezone
from decimal import Decimal

import pytest

from app.application.opportunity_decision_pipeline import OpportunityDecisionResult
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
    RecordConflict,
    RecordNotFound,
)

UTC = timezone.utc
T0 = datetime(2026, 10, 9, 10, 0, tzinfo=UTC)


def make_opportunity(title="Dashboard"):
    return Opportunity(
        source_platform="synthetic",
        source_opportunity_id="job-17",
        title=title,
        description="Synthetic fixture",
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


def make_result(opportunity_id="opp-17", evaluation_ref="eval-17"):
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
                rationale="Synthetic fixture",
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
        reasons=("tier rule matched: eligible",),
        evidence_refs=("eligibility.status",),
        criterion_snapshots=(),
        evaluated_at=T0,
    )
    return (
        evaluation_policy,
        prioritization_policy,
        OpportunityDecisionResult(
            opportunity_ref=opportunity_id,
            evaluation_ref=evaluation_ref,
            evaluation=evaluation,
            priority_decision=decision,
        ),
    )


class Clock:
    def __init__(self, value):
        self.value = value

    def __call__(self):
        return self.value


def test_revision_save_is_idempotent_and_preserves_original_recorded_at():
    clock = Clock(T0)
    repository = InMemoryOpportunityHistoryRepository(clock=clock)
    opportunity = make_opportunity()

    first = repository.save_opportunity_revision("opp-17", "rev-1", opportunity)
    clock.value = T0 + timedelta(hours=1)
    retry = repository.save_opportunity_revision("opp-17", "rev-1", opportunity)

    assert retry == first
    assert retry.recorded_at == T0
    assert repository.list_opportunity_revisions("opp-17") == (first,)


def test_reusing_revision_identity_with_different_content_conflicts_without_mutation():
    repository = InMemoryOpportunityHistoryRepository(clock=Clock(T0))
    original = repository.save_opportunity_revision(
        "opp-17", "rev-1", make_opportunity("Original")
    )

    with pytest.raises(RecordConflict):
        repository.save_opportunity_revision(
            "opp-17", "rev-1", make_opportunity("Changed")
        )

    assert repository.get_opportunity_revision("opp-17", "rev-1") == original


def test_revision_identity_is_scoped_to_parent_opportunity():
    repository = InMemoryOpportunityHistoryRepository(clock=Clock(T0))
    first = repository.save_opportunity_revision("opp-17", "rev-1", make_opportunity())
    second = repository.save_opportunity_revision(
        "opp-18", "rev-1", make_opportunity("Other opportunity")
    )

    assert first.revision_id == second.revision_id
    assert first.opportunity_id != second.opportunity_id


@pytest.mark.parametrize("identity", ["", " ", "\t", "\n"])
def test_whitespace_only_caller_identities_are_rejected(identity):
    repository = InMemoryOpportunityHistoryRepository(clock=Clock(T0))

    with pytest.raises(ValueError):
        repository.save_opportunity_revision(identity, "rev-1", make_opportunity())
    with pytest.raises(ValueError):
        repository.save_opportunity_revision("opp-17", identity, make_opportunity())


def test_accepted_identity_strings_are_preserved_exactly_without_normalization():
    repository = InMemoryOpportunityHistoryRepository(clock=Clock(T0))
    record = repository.save_opportunity_revision(
        " opp-17 ", "Rev-1", make_opportunity()
    )

    assert record.opportunity_id == " opp-17 "
    assert record.revision_id == "Rev-1"


def test_revision_history_is_deterministic_and_latest_means_latest_recorded():
    clock = Clock(T0)
    repository = InMemoryOpportunityHistoryRepository(clock=clock)
    first = repository.save_opportunity_revision("opp-17", "rev-z", make_opportunity())
    clock.value = T0 + timedelta(minutes=1)
    second = repository.save_opportunity_revision(
        "opp-17", "rev-a", make_opportunity("Second")
    )

    assert repository.list_opportunity_revisions("opp-17") == (first, second)
    assert repository.get_latest_opportunity_revision("opp-17") == second


def test_decision_requires_existing_revision_and_preserves_policy_snapshots():
    repository = InMemoryOpportunityHistoryRepository(clock=Clock(T0))
    evaluation_policy, prioritization_policy, result = make_result()

    with pytest.raises(RecordNotFound):
        repository.save_decision(
            "decision-1",
            "opp-17",
            "rev-1",
            evaluation_policy,
            prioritization_policy,
            result,
        )

    revision = repository.save_opportunity_revision(
        "opp-17", "rev-1", make_opportunity()
    )
    record = repository.save_decision(
        "decision-1",
        "opp-17",
        "rev-1",
        evaluation_policy,
        prioritization_policy,
        result,
    )

    assert record.revision_id == revision.revision_id
    assert record.evaluation_policy == evaluation_policy
    assert record.prioritization_policy == prioritization_policy
    assert record.result == result


def test_decision_policy_or_lineage_mismatch_is_rejected_before_persistence():
    repository = InMemoryOpportunityHistoryRepository(clock=Clock(T0))
    repository.save_opportunity_revision("opp-17", "rev-1", make_opportunity())
    evaluation_policy, prioritization_policy, result = make_result()
    wrong_policy = PrioritizationPolicy(
        policy_id="other-policy",
        policy_version="9",
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
            "decision-1",
            "opp-17",
            "rev-1",
            evaluation_policy,
            wrong_policy,
            result,
        )
    with pytest.raises(ValueError, match="lineage|opportunity"):
        repository.save_decision(
            "decision-2",
            "another-opportunity",
            "rev-1",
            evaluation_policy,
            prioritization_policy,
            result,
        )
    with pytest.raises(RecordNotFound):
        repository.get_decision("decision-1")


def test_decision_identity_collision_conflicts_and_history_is_immutable():
    repository = InMemoryOpportunityHistoryRepository(clock=Clock(T0))
    repository.save_opportunity_revision("opp-17", "rev-1", make_opportunity())
    evaluation_policy, prioritization_policy, result = make_result()
    first = repository.save_decision(
        "decision-1", "opp-17", "rev-1", evaluation_policy, prioritization_policy, result
    )
    assert repository.save_decision(
        "decision-1", "opp-17", "rev-1", evaluation_policy, prioritization_policy, result
    ) == first

    _, _, changed_result = make_result(evaluation_ref="eval-18")
    with pytest.raises(RecordConflict):
        repository.save_decision(
            "decision-1",
            "opp-17",
            "rev-1",
            evaluation_policy,
            prioritization_policy,
            changed_result,
        )
    assert repository.get_decision("decision-1") == first


def test_history_queries_return_explicit_not_found_for_missing_records():
    repository = InMemoryOpportunityHistoryRepository(clock=Clock(T0))

    with pytest.raises(RecordNotFound):
        repository.get_opportunity_revision("missing", "rev-1")
    with pytest.raises(RecordNotFound):
        repository.get_latest_opportunity_revision("missing")
    with pytest.raises(RecordNotFound):
        repository.get_decision("missing")


def test_equal_recorded_timestamps_use_identity_only_as_deterministic_tiebreaker():
    repository = InMemoryOpportunityHistoryRepository(clock=Clock(T0))
    z_record = repository.save_opportunity_revision(
        "opp-17", "rev-z", make_opportunity("Z")
    )
    a_record = repository.save_opportunity_revision(
        "opp-17", "rev-a", make_opportunity("A")
    )

    assert repository.list_opportunity_revisions("opp-17") == (a_record, z_record)
    assert repository.get_latest_opportunity_revision("opp-17") == z_record


def test_decision_retry_preserves_recorded_at_and_history_is_ordered():
    clock = Clock(T0)
    repository = InMemoryOpportunityHistoryRepository(clock=clock)
    repository.save_opportunity_revision("opp-17", "rev-1", make_opportunity())
    evaluation_policy, prioritization_policy, result = make_result()
    first = repository.save_decision(
        "decision-z", "opp-17", "rev-1", evaluation_policy, prioritization_policy, result
    )
    clock.value = T0 + timedelta(minutes=1)
    second_result = make_result(evaluation_ref="eval-18")[2]
    second = repository.save_decision(
        "decision-a", "opp-17", "rev-1", evaluation_policy, prioritization_policy, second_result
    )
    clock.value = T0 + timedelta(hours=1)
    replay = repository.save_decision(
        "decision-z", "opp-17", "rev-1", evaluation_policy, prioritization_policy, result
    )

    assert replay == first
    assert replay.recorded_at == T0
    assert repository.list_decisions("opp-17") == (first, second)
