from typing import Protocol

from .capability_aware_provider_dispatch import ProviderCapability
from .execution_port import ProviderExecutionResult, validate_provider_execution_result
from .provider_capability_registry import ProviderCapabilityRegistry
from .provider_credential_resolution import (
    CredentialResolutionResult,
    ProviderCredentialResolver,
    resolve_provider_credential,
)
from app.domain.authorized_execution_request import AuthorizedExecutionRequest


class AuthenticatedProviderAdapter(Protocol):
    def execute_authenticated(
        self,
        request: AuthorizedExecutionRequest,
        credential_material: str,
    ) -> ProviderExecutionResult:
        ...


def dispatch_with_credentials(
    *,
    capability_registry: ProviderCapabilityRegistry,
    credential_resolver: ProviderCredentialResolver,
    provider_key: str,
    capability: ProviderCapability,
    credential_reference: str,
    request: AuthorizedExecutionRequest,
):
    if not isinstance(capability, ProviderCapability):
        raise TypeError("capability must be a ProviderCapability")

    port = capability_registry.resolve(provider_key)
    if not capability_registry.supports(provider_key, capability):
        raise ValueError(
            f"provider '{provider_key}' does not support capability '{capability.value}'"
        )

    resolution = resolve_provider_credential(
        resolver=credential_resolver,
        provider_key=provider_key,
        credential_reference=credential_reference,
    )

    if not resolution.success:
        raise ValueError(
            f"credential resolution failed: {resolution.failure_reason.value}"
        )

    if resolution.material is None:
        raise ValueError("successful credential resolution requires material")

    adapter = port
    execute_authenticated = getattr(adapter, "execute_authenticated", None)
    if not callable(execute_authenticated):
        raise TypeError(
            "provider adapter does not implement execute_authenticated"
        )

    raw = execute_authenticated(request, resolution.material)
    if not isinstance(raw, ProviderExecutionResult):
        raise TypeError(
            "authenticated provider adapter must return ProviderExecutionResult"
        )

    validate_provider_execution_result(request, raw)
    return raw
