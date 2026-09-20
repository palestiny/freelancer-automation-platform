from app.application.execution_port import ExecutionPort, dispatch_execution
from app.application.provider_adapter_registry import ProviderAdapterRegistry
from app.application.provider_capability_registry import ProviderCapability, ProviderCapabilityRegistry


def dispatch_with_capability(
    *,
    registry: ProviderCapabilityRegistry,
    provider_key: str,
    capability: ProviderCapability,
    request,
):
    if not isinstance(capability, ProviderCapability):
        raise TypeError("capability must be a ProviderCapability")

    port = registry.resolve(provider_key)
    if not registry.supports(provider_key, capability):
        raise ValueError(
            f"provider '{provider_key}' does not support capability '{capability.value}'"
        )

    return dispatch_execution(port=port, request=request)
