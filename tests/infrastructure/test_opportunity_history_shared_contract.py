"""Run the shared opportunity-history contract against the reference adapter."""
import pytest

from app.infrastructure.persistence.in_memory_opportunity_history_repository import (
    InMemoryOpportunityHistoryRepository,
)
from tests.contracts.opportunity_history_repository_contract_cases import (
    test_decision_history_is_ordered_and_missing_records_are_explicit,
    test_decision_requires_revision_and_is_idempotent_but_immutable,
    test_revision_identity_idempotency_conflict_and_history,
)


@pytest.fixture
def repository_factory():
    # Production adapters can provide the same fixture in their own test module
    # and import the shared contract cases without duplicating their assertions.
    return InMemoryOpportunityHistoryRepository


class TestInMemoryOpportunityHistoryRepositorySharedContract:
    def test_revision_contract(self, repository_factory):
        test_revision_identity_idempotency_conflict_and_history(repository_factory)

    def test_decision_idempotency_and_conflict_contract(self, repository_factory):
        test_decision_requires_revision_and_is_idempotent_but_immutable(repository_factory)

    def test_decision_history_and_not_found_contract(self, repository_factory):
        test_decision_history_is_ordered_and_missing_records_are_explicit(repository_factory)
