import pytest
from datetime import datetime, timedelta, timezone

from app.application.provider_authenticated_dispatch import dispatch_with_credentials
from app.application.provider_capability_registry import ProviderCapability, ProviderCapabilityRegistry
from app.application.provider_credential_resolution import CredentialResolutionResult
from app.domain.execution_request_freshness import ExecutionRequestFreshnessPolicy
from app.domain.authorized_execution_request import AuthorizedExecutionRequest, ExecutionRequestStatus
from app.domain.action_authorization import ActionClass, AutonomyLevel
from app.domain.execution_outcome import ExecutionOutcomeStatus
from app.application.execution_port import ExecutionPort, ProviderExecutionResult


class Adapter(ExecutionPort):
    def __init__(self):
        self.calls = 0

    def execute(self, request):
        raise AssertionError("authenticated path required")

    def execute_authenticated(self, request, credential_material):
        self.calls += 1
        return ProviderExecutionResult(
            request_id=request.request_id,
            idempotency_key=request.idempotency_key,
            status=ExecutionOutcomeStatus.SUCCEEDED,
            outcome_code="ok",
            observed_at=datetime.now(timezone.utc),
        )


class Resolver:
    def resolve(self, *, provider_key, credential_reference):
        return CredentialResolutionResult.success(
            provider_key=provider_key,
            credential_reference=credential_reference,
            material="secret",
        )


def _registry(adapter):
    registry = ProviderCapabilityRegistry()
    registry.register("provider-a", adapter, capabilities={ProviderCapability.SEND_MESSAGE})
    return registry


def _request(prepared_at):
    return AuthorizedExecutionRequest(
        request_id="req-1",
        idempotency_key="idem-1",
        action_class=ActionClass.REVERSIBLE_EXTERNAL,
        autonomy_level=AutonomyLevel.L3_EXECUTE_WITH_APPROVAL,
        policy_id="policy-1",
        policy_version="1",
        status=ExecutionRequestStatus.PREPARED,
        prepared_at=prepared_at,
    )


def test_freshness_is_required_before_authenticated_provider_invocation():
    adapter = Adapter()
    prepared_at = datetime(2026, 9, 20, 12, tzinfo=timezone.utc)

    result = dispatch_with_credentials(
        capability_registry=_registry(adapter),
        credential_resolver=Resolver(),
        provider_key="provider-a",
        capability=ProviderCapability.SEND_MESSAGE,
        credential_reference="cred-1",
        request=_request(prepared_at),
        freshness_policy=ExecutionRequestFreshnessPolicy(maximum_age=timedelta(minutes=30)),
        as_of=prepared_at + timedelta(minutes=10),
    )

    assert result.status is ExecutionOutcomeStatus.SUCCEEDED
    assert adapter.calls == 1


def test_stale_request_is_rejected_before_provider_invocation():
    adapter = Adapter()
    prepared_at = datetime(2026, 9, 20, 12, tzinfo=timezone.utc)

    with pytest.raises(ValueError, match="stale"):
        dispatch_with_credentials(
            capability_registry=_registry(adapter),
            credential_resolver=Resolver(),
            provider_key="provider-a",
            capability=ProviderCapability.SEND_MESSAGE,
            credential_reference="cred-1",
            request=_request(prepared_at),
            freshness_policy=ExecutionRequestFreshnessPolicy(maximum_age=timedelta(minutes=30)),
            as_of=prepared_at + timedelta(minutes=31),
        )

    assert adapter.calls == 0
