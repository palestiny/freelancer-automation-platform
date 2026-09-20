from app.application.execution_port import ExecutionPort


class ProviderAdapterRegistry:
    """Explicit provider-key to execution-adapter resolution boundary."""

    def __init__(self) -> None:
        self._adapters: dict[str, ExecutionPort] = {}

    def register(self, provider_key: str, adapter: ExecutionPort) -> None:
        if not isinstance(provider_key, str) or not provider_key.strip():
            raise ValueError("provider_key must be a non-empty string")
        if not isinstance(adapter, ExecutionPort):
            raise TypeError("adapter must implement ExecutionPort")
        if provider_key in self._adapters:
            raise ValueError(f"provider '{provider_key}' is already registered")
        self._adapters[provider_key] = adapter

    def resolve(self, provider_key: str) -> ExecutionPort:
        if not isinstance(provider_key, str) or not provider_key.strip():
            raise ValueError("provider_key must be a non-empty string")
        try:
            return self._adapters[provider_key]
        except KeyError as exc:
            raise KeyError(f"unknown provider '{provider_key}'") from exc
