from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class ProviderFailureCode(Enum):
    AUTHENTICATION_FAILURE = "AUTHENTICATION_FAILURE"
    AUTHORIZATION_FAILURE = "AUTHORIZATION_FAILURE"
    RATE_LIMITED = "RATE_LIMITED"
    PROVIDER_UNAVAILABLE = "PROVIDER_UNAVAILABLE"
    INVALID_REQUEST = "INVALID_REQUEST"
    MALFORMED_RESPONSE = "MALFORMED_RESPONSE"
    PARTIAL_RESULT = "PARTIAL_RESULT"


@dataclass(frozen=True)
class ProviderFailure:
    code: ProviderFailureCode
    message: str

    def __post_init__(self) -> None:
        if not isinstance(self.code, ProviderFailureCode):
            raise TypeError("code must be a ProviderFailureCode")
        if not isinstance(self.message, str) or not self.message.strip():
            raise ValueError("message cannot be empty")


class AuthenticationFailure(ProviderFailure):
    def __init__(self, message: str):
        super().__init__(ProviderFailureCode.AUTHENTICATION_FAILURE, message)


@dataclass(frozen=True)
class OpportunityDiscoveryCriteria:
    query: str | None = None

    def __post_init__(self) -> None:
        if self.query is not None and not isinstance(self.query, str):
            raise TypeError("query must be a string or None")


@dataclass(frozen=True)
class ExternalOpportunityObservation:
    provider_key: str
    external_opportunity_id: str
    observed_at: datetime
    title: str | None = None
    description: str | None = None
    project_type: str | None = None
    budget_min: float | None = None
    budget_max: float | None = None
    required_capabilities: frozenset[str] = frozenset()

    def __post_init__(self) -> None:
        for name in ("provider_key", "external_opportunity_id"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} cannot be empty")
        if not isinstance(self.observed_at, datetime):
            raise TypeError("observed_at must be a datetime")
        if self.observed_at.tzinfo is None or self.observed_at.utcoffset() is None:
            raise ValueError("observed_at must be timezone-aware")
        if self.project_type is not None and not isinstance(self.project_type, str):
            raise TypeError("project_type must be a string or None")
        for name in ("budget_min", "budget_max"):
            value = getattr(self, name)
            if value is not None and not isinstance(value, (int, float)):
                raise TypeError(f"{name} must be a number or None")
        if (
            self.budget_min is not None
            and self.budget_max is not None
            and self.budget_min > self.budget_max
        ):
            raise ValueError("budget_min cannot exceed budget_max")
        if not isinstance(self.required_capabilities, frozenset):
            raise TypeError("required_capabilities must be a frozenset")
        for capability in self.required_capabilities:
            if not isinstance(capability, str) or not capability.strip():
                raise ValueError("required_capabilities entries cannot be empty")


@dataclass(frozen=True)
class OpportunityDiscoveryResult:
    provider_key: str
    observed_at: datetime
    observations: tuple[ExternalOpportunityObservation, ...]
    next_cursor: str | None = None
    complete: bool = True
    failure: ProviderFailure | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.provider_key, str) or not self.provider_key.strip():
            raise ValueError("provider_key cannot be empty")
        if not isinstance(self.observed_at, datetime):
            raise TypeError("observed_at must be a datetime")
        if self.observed_at.tzinfo is None or self.observed_at.utcoffset() is None:
            raise ValueError("observed_at must be timezone-aware")
        if not isinstance(self.observations, tuple):
            raise TypeError("observations must be a tuple")
        for observation in self.observations:
            if not isinstance(observation, ExternalOpportunityObservation):
                raise TypeError("observations must contain ExternalOpportunityObservation")
            if observation.provider_key != self.provider_key:
                raise ValueError("observation provider_key must match result provider_key")
        if self.complete and self.next_cursor is not None:
            raise ValueError("complete result cannot contain next_cursor")


class MarketplaceOpportunityAdapter(ABC):
    @abstractmethod
    def discover_opportunities(
        self,
        criteria: OpportunityDiscoveryCriteria,
        cursor: str | None = None,
    ) -> OpportunityDiscoveryResult:
        """Read-only provider adapter contract for opportunity discovery."""
