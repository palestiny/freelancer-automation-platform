import pytest

from app.application.execution_port import ExecutionPort, ProviderExecutionResult
from app.application.provider_capability_registry import (
    ProviderCapability,
    ProviderCapabilityRegistry,
)


class FakeAdapter(ExecutionPort):
    def execute(self, request):
        raise AssertionError("registry tests must not execute providers")


def test_register_and_resolve_provider_capabilities():
    registry = ProviderCapabilityRegistry()
    adapter = FakeAdapter()

    registry.register(
        "market-a",
        adapter,
        capabilities={
            ProviderCapability.SEARCH_OPPORTUNITIES,
            ProviderCapability.SUBMIT_PROPOSAL,
        },
    )

    assert registry.resolve("market-a") is adapter
    assert registry.capabilities("market-a") == frozenset(
        {
            ProviderCapability.SEARCH_OPPORTUNITIES,
            ProviderCapability.SUBMIT_PROPOSAL,
        }
    )
    assert registry.supports("market-a", ProviderCapability.SEARCH_OPPORTUNITIES)
    assert not registry.supports("market-a", ProviderCapability.SEND_MESSAGE)


def test_duplicate_provider_is_rejected():
    registry = ProviderCapabilityRegistry()
    adapter = FakeAdapter()
    registry.register("market-a", adapter, capabilities={ProviderCapability.READ_OPPORTUNITY})

    with pytest.raises(ValueError, match="already registered"):
        registry.register(
            "market-a",
            adapter,
            capabilities={ProviderCapability.READ_OPPORTUNITY},
        )


def test_empty_capability_declaration_is_rejected():
    registry = ProviderCapabilityRegistry()

    with pytest.raises(ValueError, match="capabilities"):
        registry.register("market-a", FakeAdapter(), capabilities=set())


def test_unknown_capability_value_is_rejected():
    registry = ProviderCapabilityRegistry()

    with pytest.raises(ValueError, match="unknown capability"):
        registry.register("market-a", FakeAdapter(), capabilities={"not-a-capability"})


def test_unknown_provider_lookup_is_explicit():
    registry = ProviderCapabilityRegistry()

    with pytest.raises(KeyError, match="unknown provider"):
        registry.resolve("missing")

    with pytest.raises(KeyError, match="unknown provider"):
        registry.capabilities("missing")

    with pytest.raises(KeyError, match="unknown provider"):
        registry.supports("missing", ProviderCapability.SEND_MESSAGE)


def test_invalid_adapter_is_rejected():
    registry = ProviderCapabilityRegistry()

    with pytest.raises(TypeError, match="ExecutionPort"):
        registry.register(
            "market-a",
            object(),
            capabilities={ProviderCapability.READ_OPPORTUNITY},
        )
