"""Run the shared opportunity-history contract against the reference adapter."""
from datetime import datetime, timedelta, timezone

import pytest

from app.infrastructure.persistence.in_memory_opportunity_history_repository import (
    InMemoryOpportunityHistoryRepository,
)
from tests.contracts.opportunity_history_repository_contract_cases import (
    assert_decision_history_is_ordered_and_missing_records_are_explicit,
    assert_decision_requires_revision_and_is_idempotent_but_immutable,
    assert_revision_identity_idempotency_conflict_and_history,
    assert_identity_validation_and_preservation,
    assert_decision_policy_and_lineage_are_validated,
    assert_equal_timestamp_ordering_tiebreaker,
    assert_equal_timestamp_decision_ordering_tiebreaker,
    assert_revision_latest_uses_recorded_time,
    assert_decision_history_uses_recorded_time,
    assert_revision_retry_preserves_recorded_at_after_time_advances,
    assert_decision_retry_preserves_recorded_at_after_time_advances,
    make_opportunity,
    make_policies,
    make_result,
)


@pytest.fixture
def repository_factory():
    # Production adapters can provide the same fixture in their own test module
    # and import the shared contract cases without duplicating their assertions.
    return InMemoryOpportunityHistoryRepository


class TestInMemoryOpportunityHistoryRepositorySharedContract:
    def test_revision_contract(self, repository_factory):
        assert_revision_identity_idempotency_conflict_and_history(repository_factory)

    def test_decision_idempotency_and_conflict_contract(self, repository_factory):
        assert_decision_requires_revision_and_is_idempotent_but_immutable(repository_factory)

    def test_decision_history_and_not_found_contract(self, repository_factory):
        assert_decision_history_is_ordered_and_missing_records_are_explicit(repository_factory)

    def test_identity_validation_and_preservation_contract(self, repository_factory):
        assert_identity_validation_and_preservation(repository_factory)

    def test_decision_policy_and_lineage_contract(self, repository_factory):
        assert_decision_policy_and_lineage_are_validated(repository_factory)


@pytest.fixture
def equal_timestamp_repository_factory():
    # Separate deterministic fixture: not every production adapter can inject
    # a clock, so its equivalent fixture may seed equal persisted timestamps.
    fixed_time = datetime(2026, 10, 9, 10, 0, tzinfo=timezone.utc)
    return lambda: InMemoryOpportunityHistoryRepository(clock=lambda: fixed_time)


def seed_equal_timestamp_revisions(repository):
    repository.save_opportunity_revision(
        "contract-opp-1", "rev-z", make_opportunity("Z")
    )
    repository.save_opportunity_revision(
        "contract-opp-1", "rev-a", make_opportunity("A")
    )


def test_equal_timestamp_ordering_tiebreaker_contract(
    equal_timestamp_repository_factory,
):
    assert_equal_timestamp_ordering_tiebreaker(
        equal_timestamp_repository_factory, seed_equal_timestamp_revisions
    )


def seed_timestamped_revisions(repository):
    repository.save_opportunity_revision(
        "contract-opp-1", "rev-z", make_opportunity("Earlier")
    )
    repository.save_opportunity_revision(
        "contract-opp-1", "rev-a", make_opportunity("Later")
    )


def test_revision_latest_uses_recorded_time_contract():
    start = datetime(2026, 10, 9, 10, 0, tzinfo=timezone.utc)
    times = iter((start, start + timedelta(minutes=1)))
    def factory():
        return InMemoryOpportunityHistoryRepository(clock=lambda: next(times))

    assert_revision_latest_uses_recorded_time(factory, seed_timestamped_revisions)


def seed_timestamped_decisions(repository):
    # The repository factory supplies revision time, then the two decision times.
    repository.save_opportunity_revision(
        "contract-opp-1", "revision-1", make_opportunity()
    )
    evaluation_policy, prioritization_policy = make_policies()
    repository.save_decision(
        "decision-z", "contract-opp-1", "revision-1",
        evaluation_policy, prioritization_policy,
        make_result(evaluation_ref="evaluation-z"),
    )
    repository.save_decision(
        "decision-a", "contract-opp-1", "revision-1",
        evaluation_policy, prioritization_policy,
        make_result(evaluation_ref="evaluation-a"),
    )


def test_decision_history_uses_recorded_time_contract():
    start = datetime(2026, 10, 9, 10, 0, tzinfo=timezone.utc)
    times = iter((
        start,
        start + timedelta(minutes=1),
        start + timedelta(minutes=2),
    ))

    def factory():
        return InMemoryOpportunityHistoryRepository(clock=lambda: next(times))

    assert_decision_history_uses_recorded_time(factory, seed_timestamped_decisions)


class MutableClock:
    def __init__(self, value):
        self.value = value

    def __call__(self):
        return self.value

    def advance(self):
        self.value += timedelta(minutes=5)


def test_revision_retry_preserves_original_recorded_at_contract():
    clock = MutableClock(datetime(2026, 10, 9, 10, 0, tzinfo=timezone.utc))
    repository = InMemoryOpportunityHistoryRepository(clock=clock)
    assert_revision_retry_preserves_recorded_at_after_time_advances(
        repository, clock.advance
    )


def test_decision_retry_preserves_original_recorded_at_contract():
    clock = MutableClock(datetime(2026, 10, 9, 10, 0, tzinfo=timezone.utc))
    repository = InMemoryOpportunityHistoryRepository(clock=clock)
    assert_decision_retry_preserves_recorded_at_after_time_advances(
        repository, clock.advance
    )



def seed_equal_timestamp_decisions(repository):
    repository.save_opportunity_revision(
        "contract-opp-1", "revision-1", make_opportunity()
    )
    evaluation_policy, prioritization_policy = make_policies()
    # Deliberately insert reverse lexical order; persisted history must use ID
    # as a deterministic tie-breaker only because recorded_at is equal.
    for decision_id, evaluation_ref in (
        ("decision-z", "evaluation-z"),
        ("decision-a", "evaluation-a"),
    ):
        repository.save_decision(
            decision_id,
            "contract-opp-1",
            "revision-1",
            evaluation_policy,
            prioritization_policy,
            make_result(evaluation_ref=evaluation_ref),
        )


def test_equal_timestamp_decision_ordering_tiebreaker_contract():
    fixed_time = datetime(2026, 10, 9, 10, 0, tzinfo=timezone.utc)
    factory = lambda: InMemoryOpportunityHistoryRepository(clock=lambda: fixed_time)
    assert_equal_timestamp_decision_ordering_tiebreaker(
        factory, seed_equal_timestamp_decisions
    )
