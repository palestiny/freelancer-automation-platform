import pytest

from app.application.capability_aware_provider_dispatch import dispatch_with_capability
from app.application.execution_port import ExecutionPort, ProviderExecutionResult
from app.application.provider_capability_registry import (
    ProviderCapability,
    ProviderCapabilityRegistry,
)


class FakeAdapter(ExecutionPort):
    def __init__(self):
        self.called = False

    def execute(self, request):
        self.called = True
        raise AssertionError("dispatch test must not invoke external execution")


def test_unsupported_capability_is_rejected_before_execution():
    registry = ProviderCapabilityRegistry()
    adapter = FakeAdapter()
    registry.register(
        "market-a",
        adapter,
        capabilities={ProviderCapability.SEARCH_OPPORTUNITIES},
    )

    with pytest.raises(ValueError, match="does not support"):
        dispatch_with_capability(
            registry=registry,
            provider_key="market-a",
            capability=ProviderCapability.SUBMIT_PROPOSAL,
            request=object(),
        )

    assert adapter.called is False


def test_unknown_provider_is_rejected():
    registry = ProviderCapabilityRegistry()

    with pytest.raises(KeyError, match="unknown provider"):
        dispatch_with_capability(
            registry=registry,
            provider_key="missing",
            capability=ProviderCapability.SUBMIT_PROPOSAL,
            request=object(),
        )


def test_supported_capability_reaches_existing_dispatch_boundary(monkeypatch):
    registry = ProviderCapabilityRegistry()
    adapter = FakeAdapter()
    registry.register(
        "market-a",
        adapter,
        capabilities={ProviderCapability.SUBMIT_PROPOSAL},
    )

    sentinel = object()
    observed = {}

    def fake_dispatch(*, port, request):
        observed["port"] = port
        observed["request"] = request
        return sentinel

    monkeypatch.setattr(
        "app.application.capability_aware_provider_dispatch.dispatch_execution",
        fake_dispatch,
    )

    result = dispatch_with_capability(
        registry=registry,
        provider_key="market-a",
        capability=ProviderCapability.SUBMIT_PROPOSAL,
        request=sentinel,
    )

    assert result is sentinel
    assert observed["port"] is adapter
    assert observed["request"] is sentinel
