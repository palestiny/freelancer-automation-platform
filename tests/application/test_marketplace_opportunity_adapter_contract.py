import pytest
from datetime import datetime, timezone

from app.application.marketplace_opportunity_adapter import (
    AuthenticationFailure,
    ExternalOpportunityObservation,
    MarketplaceOpportunityAdapter,
    OpportunityDiscoveryCriteria,
    OpportunityDiscoveryResult,
    ProviderFailure,
    ProviderFailureCode,
)


class FakeMarketplaceAdapter(MarketplaceOpportunityAdapter):
    def discover_opportunities(self, criteria, cursor=None):
        raise NotImplementedError


def test_discovery_contract_requires_provider_neutral_result():
    adapter = FakeMarketplaceAdapter()
    result = adapter.discover_opportunities(
        OpportunityDiscoveryCriteria(query="react")
    )
    assert isinstance(result, OpportunityDiscoveryResult)


def test_external_observation_preserves_provider_and_external_identity():
    observation = ExternalOpportunityObservation(
        provider_key="fake_marketplace",
        external_opportunity_id="opp-1",
        observed_at=datetime.now(timezone.utc),
        title="React dashboard",
        description="Build a dashboard",
    )

    assert observation.provider_key == "fake_marketplace"
    assert observation.external_opportunity_id == "opp-1"


def test_discovery_result_exposes_continuation_and_completeness():
    result = OpportunityDiscoveryResult(
        provider_key="fake_marketplace",
        observed_at=datetime.now(timezone.utc),
        observations=(),
        next_cursor="page-2",
        complete=False,
    )

    assert result.next_cursor == "page-2"
    assert result.complete is False


@pytest.mark.parametrize(
    "failure_code",
    [
        ProviderFailureCode.AUTHENTICATION_FAILURE,
        ProviderFailureCode.AUTHORIZATION_FAILURE,
        ProviderFailureCode.RATE_LIMITED,
        ProviderFailureCode.PROVIDER_UNAVAILABLE,
        ProviderFailureCode.INVALID_REQUEST,
        ProviderFailureCode.MALFORMED_RESPONSE,
        ProviderFailureCode.PARTIAL_RESULT,
    ],
)
def test_provider_failures_are_explicit_and_provider_neutral(failure_code):
    failure = ProviderFailure(code=failure_code, message="provider failure")
    assert failure.code is failure_code


def test_provider_failure_does_not_become_an_execution_or_retry_command():
    failure = AuthenticationFailure(message="credentials rejected")

    assert isinstance(failure, ProviderFailure)
    assert not hasattr(failure, "retry")
    assert not hasattr(failure, "execute")
