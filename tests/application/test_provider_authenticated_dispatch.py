from datetime import datetime, timezone, timedelta

import pytest

from app.application.provider_capability_registry import ProviderCapability
from app.domain.execution_request_freshness import ExecutionRequestFreshnessPolicy
from app.application.execution_port import ProviderExecutionResult
from app.application.provider_authenticated_dispatch import (
    dispatch_with_credentials,
)
from app.application.provider_capability_registry import ProviderCapabilityRegistry
from app.application.execution_port import ExecutionPort
from app.application.provider_credential_resolution import (
    CredentialResolutionResult,
    CredentialResolutionFailure,
)
from app.domain.authorized_execution_request import AuthorizedExecutionRequest, ExecutionRequestStatus
from app.domain.action_authorization import ActionClass, AutonomyLevel
from app.domain.execution_outcome import ExecutionOutcomeStatus


class Adapter(ExecutionPort):
    def __init__(self):
        self.calls = []

    def execute(self, request):
        raise AssertionError("authenticated dispatch must be used")

    def execute_authenticated(self, request, credential_material):
        self.calls.append((request, credential_material))
        return ProviderExecutionResult(
            request_id=request.request_id,
            idempotency_key=request.idempotency_key,
            status=ExecutionOutcomeStatus.SUCCEEDED,
            outcome_code="ok",
            observed_at=datetime.now(timezone.utc),
        )


class Resolver:
    def __init__(self, result):
        self.result = result
        self.calls = []

    def resolve(self, *, provider_key, credential_reference):
        self.calls.append((provider_key, credential_reference))
        return self.result


def _request():
    return AuthorizedExecutionRequest(
        request_id="req-1",
        idempotency_key="idem-1",
        action_class=ActionClass.REVERSIBLE_EXTERNAL,
        autonomy_level=AutonomyLevel.L3_EXECUTE_WITH_APPROVAL,
        policy_id="policy-1",
        policy_version="1",
        status=ExecutionRequestStatus.PREPARED,
        prepared_at=datetime(2026, 9, 20, 12, tzinfo=timezone.utc),
    )


def _registry(adapter):
    registry = ProviderCapabilityRegistry()
    registry.register(
        "provider-a",
        adapter,
        capabilities={ProviderCapability.SEND_MESSAGE},
    )
    return registry


def test_dispatch_resolves_credential_and_executes_authenticated_adapter():
    adapter = Adapter()
    resolver = Resolver(
        CredentialResolutionResult.success(
            provider_key="provider-a",
            credential_reference="cred-1",
            material="secret",
        )
    )

    result = dispatch_with_credentials(
        capability_registry=_registry(adapter),
        credential_resolver=resolver,
        provider_key="provider-a",
        capability=ProviderCapability.SEND_MESSAGE,
        credential_reference="cred-1",
        request=_request(),
        freshness_policy=ExecutionRequestFreshnessPolicy(maximum_age=timedelta(minutes=30)),
        as_of=datetime(2026, 9, 20, 12, 10, tzinfo=timezone.utc),
    )

    assert result.status is ExecutionOutcomeStatus.SUCCEEDED
    assert resolver.calls == [("provider-a", "cred-1")]
    assert adapter.calls[0][1] == "secret"


def test_unsupported_capability_rejects_before_credential_resolution():
    adapter = Adapter()
    resolver = Resolver(CredentialResolutionResult.failure(CredentialResolutionFailure.NOT_FOUND))

    with pytest.raises(ValueError, match="does not support capability"):
        dispatch_with_credentials(
            capability_registry=_registry(adapter),
            credential_resolver=resolver,
            provider_key="provider-a",
            capability=ProviderCapability.SUBMIT_PROPOSAL,
            credential_reference="cred-1",
            request=_request(),
        freshness_policy=ExecutionRequestFreshnessPolicy(maximum_age=timedelta(minutes=30)),
        as_of=datetime(2026, 9, 20, 12, 10, tzinfo=timezone.utc),
            freshness_policy=ExecutionRequestFreshnessPolicy(maximum_age=timedelta(minutes=30)),
            as_of=datetime(2026, 9, 20, 12, 10, tzinfo=timezone.utc),
        )

    assert resolver.calls == []
    assert adapter.calls == []


def test_failed_credential_resolution_rejects_before_provider_execution():
    adapter = Adapter()
    resolver = Resolver(CredentialResolutionResult.failure(CredentialResolutionFailure.NOT_FOUND))

    with pytest.raises(ValueError, match="credential resolution failed"):
        dispatch_with_credentials(
            capability_registry=_registry(adapter),
            credential_resolver=resolver,
            provider_key="provider-a",
            capability=ProviderCapability.SEND_MESSAGE,
            credential_reference="cred-1",
            request=_request(),
        freshness_policy=ExecutionRequestFreshnessPolicy(maximum_age=timedelta(minutes=30)),
        as_of=datetime(2026, 9, 20, 12, 10, tzinfo=timezone.utc),
        )

    assert resolver.calls == [("provider-a", "cred-1")]
    assert adapter.calls == []


def test_resolution_provider_binding_is_required():
    adapter = Adapter()
    resolver = Resolver(
        CredentialResolutionResult.success(
            provider_key="provider-b",
            credential_reference="cred-1",
            material="secret",
        )
    )

    with pytest.raises(ValueError, match="bound to provider and reference"):
        dispatch_with_credentials(
            capability_registry=_registry(adapter),
            credential_resolver=resolver,
            provider_key="provider-a",
            capability=ProviderCapability.SEND_MESSAGE,
            credential_reference="cred-1",
            request=_request(),
        freshness_policy=ExecutionRequestFreshnessPolicy(maximum_age=timedelta(minutes=30)),
        as_of=datetime(2026, 9, 20, 12, 10, tzinfo=timezone.utc),
        )

    assert adapter.calls == []
