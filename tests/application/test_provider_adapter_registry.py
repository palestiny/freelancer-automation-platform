import pytest

from app.application.execution_port import ExecutionPort
from app.application.provider_adapter_registry import ProviderAdapterRegistry


class StubAdapter(ExecutionPort):
    def execute(self, request):
        raise AssertionError("execution must not occur during resolution")


def test_registered_provider_resolves_exact_adapter():
    registry = ProviderAdapterRegistry()
    adapter = StubAdapter()
    registry.register("marketplace_a", adapter)
    assert registry.resolve("marketplace_a") is adapter


def test_duplicate_provider_registration_is_rejected():
    registry = ProviderAdapterRegistry()
    registry.register("marketplace_a", StubAdapter())
    with pytest.raises(ValueError, match="already registered"):
        registry.register("marketplace_a", StubAdapter())


def test_unknown_provider_resolution_is_explicit():
    registry = ProviderAdapterRegistry()
    with pytest.raises(KeyError, match="unknown provider"):
        registry.resolve("missing")


def test_registries_are_isolated():
    first = ProviderAdapterRegistry()
    second = ProviderAdapterRegistry()
    adapter = StubAdapter()
    first.register("marketplace_a", adapter)
    with pytest.raises(KeyError):
        second.resolve("marketplace_a")


def test_provider_key_must_be_non_empty():
    registry = ProviderAdapterRegistry()
    with pytest.raises(ValueError, match="provider_key"):
        registry.register("   ", StubAdapter())
