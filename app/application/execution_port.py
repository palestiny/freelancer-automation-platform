from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime

from app.domain.authorized_execution_request import AuthorizedExecutionRequest, ExecutionRequestStatus
from app.domain.execution_outcome import ExecutionOutcome, ExecutionOutcomeStatus
from app.application.provider_adapter_conformance import validate_provider_execution_result


@dataclass(frozen=True)
class ProviderExecutionResult:
    request_id: str
    idempotency_key: str
    status: ExecutionOutcomeStatus
    outcome_code: str
    observed_at: datetime
    external_reference: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.status, ExecutionOutcomeStatus):
            raise TypeError('status must be an ExecutionOutcomeStatus')
        if not isinstance(self.observed_at, datetime):
            raise TypeError('observed_at must be a datetime')
        if self.observed_at.tzinfo is None or self.observed_at.utcoffset() is None:
            raise ValueError('observed_at must be timezone-aware')
        for name in ("request_id", "idempotency_key", "outcome_code"):
            if not isinstance(getattr(self, name), str) or not getattr(self, name).strip():
                raise ValueError(f"{name} cannot be empty")
        if self.external_reference is not None and not self.external_reference.strip():
            raise ValueError("external_reference cannot be empty")


class ExecutionPort(ABC):
    @abstractmethod
    def execute(self, request: AuthorizedExecutionRequest) -> ProviderExecutionResult:
        """Provider adapter contract; implementations live outside the domain."""


def dispatch_execution(*, port: ExecutionPort, request: AuthorizedExecutionRequest) -> ExecutionOutcome:
    if request.status is not ExecutionRequestStatus.PREPARED:
        raise ValueError("execution dispatch requires a prepared execution request")
    raw = port.execute(request)
    validate_provider_execution_result(request, raw)
    return ExecutionOutcome(
        request_id=raw.request_id,
        idempotency_key=raw.idempotency_key,
        status=raw.status,
        outcome_code=raw.outcome_code,
        observed_at=raw.observed_at,
        external_reference=raw.external_reference,
    )
