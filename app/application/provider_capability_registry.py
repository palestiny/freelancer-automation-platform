from enum import Enum

from app.application.execution_port import ExecutionPort


class ProviderCapability(str, Enum):
    SEARCH_OPPORTUNITIES = "search_opportunities"
    READ_OPPORTUNITY = "read_opportunity"
    SUBMIT_PROPOSAL = "submit_proposal"
    SEND_MESSAGE = "send_message"
    DELIVER_ASSET = "deliver_asset"
    READ_CLIENT_FEEDBACK = "read_client_feedback"


class ProviderCapabilityRegistry:
    """Provider-key registry with explicit, non-executing capability metadata."""

    def __init__(self) -> None:
        self._adapters: dict[str, ExecutionPort] = {}
        self._capabilities: dict[str, frozenset[ProviderCapability]] = {}

    def register(
        self,
        provider_key: str,
        adapter: ExecutionPort,
        *,
        capabilities: set[ProviderCapability] | frozenset[ProviderCapability],
    ) -> None:
        if not isinstance(provider_key, str) or not provider_key.strip():
            raise ValueError("provider_key must be a non-empty string")
        if not isinstance(adapter, ExecutionPort):
            raise TypeError("adapter must implement ExecutionPort")
        if not capabilities:
            raise ValueError("capabilities cannot be empty")

        normalized: set[ProviderCapability] = set()
        for capability in capabilities:
            if not isinstance(capability, ProviderCapability):
                raise ValueError(f"unknown capability '{capability}'")
            normalized.add(capability)

        if provider_key in self._adapters:
            raise ValueError(f"provider '{provider_key}' is already registered")

        self._adapters[provider_key] = adapter
        self._capabilities[provider_key] = frozenset(normalized)

    def resolve(self, provider_key: str) -> ExecutionPort:
        self._validate_provider_key(provider_key)
        try:
            return self._adapters[provider_key]
        except KeyError as exc:
            raise KeyError(f"unknown provider '{provider_key}'") from exc

    def capabilities(self, provider_key: str) -> frozenset[ProviderCapability]:
        self._validate_provider_key(provider_key)
        try:
            return self._capabilities[provider_key]
        except KeyError as exc:
            raise KeyError(f"unknown provider '{provider_key}'") from exc

    def supports(self, provider_key: str, capability: ProviderCapability) -> bool:
        if not isinstance(capability, ProviderCapability):
            raise TypeError("capability must be a ProviderCapability")
        return capability in self.capabilities(provider_key)

    @staticmethod
    def _validate_provider_key(provider_key: str) -> None:
        if not isinstance(provider_key, str) or not provider_key.strip():
            raise ValueError("provider_key must be a non-empty string")
