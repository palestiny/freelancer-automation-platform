from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime

from app.domain.execution_outcome import ExecutionOutcomeStatus


@dataclass(frozen=True)
class ProviderExecutionStatusQuery:
    request_id: str
    idempotency_key: str

    def __post_init__(self) -> None:
        for name in ("request_id", "idempotency_key"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} cannot be empty")


@dataclass(frozen=True)
class ProviderExecutionStatusResult:
    request_id: str
    idempotency_key: str
    status: ExecutionOutcomeStatus
    outcome_code: str
    observed_at: datetime
    external_reference: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.status, ExecutionOutcomeStatus):
            raise TypeError("status must be an ExecutionOutcomeStatus")
        if not isinstance(self.observed_at, datetime):
            raise TypeError("observed_at must be a datetime")
        if self.observed_at.tzinfo is None or self.observed_at.utcoffset() is None:
            raise ValueError("observed_at must be timezone-aware")
        for name in ("request_id", "idempotency_key", "outcome_code"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} cannot be empty")
        if self.external_reference is not None and not self.external_reference.strip():
            raise ValueError("external_reference cannot be empty")


class ProviderExecutionStatusPort(ABC):
    @abstractmethod
    def get_status(
        self,
        query: ProviderExecutionStatusQuery,
    ) -> ProviderExecutionStatusResult:
        """Provider adapter contract; implementations remain outside the domain."""


def observe_provider_execution_status(
    *,
    port: ProviderExecutionStatusPort,
    query: ProviderExecutionStatusQuery,
) -> ProviderExecutionStatusResult:
    result = port.get_status(query)
    if not isinstance(result, ProviderExecutionStatusResult):
        raise TypeError("status port must return ProviderExecutionStatusResult")
    if result.request_id != query.request_id:
        raise ValueError("provider status request_id does not match query")
    if result.idempotency_key != query.idempotency_key:
        raise ValueError("provider status idempotency_key does not match query")
    return result
