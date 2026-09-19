from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime

from app.domain.authorized_execution_request import AuthorizedExecutionRequest, ExecutionRequestStatus
from app.domain.execution_outcome import ExecutionOutcome, ExecutionOutcomeStatus


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
    if not isinstance(raw, ProviderExecutionResult):
        raise TypeError('execution port must return ProviderExecutionResult')
    if raw.request_id != request.request_id:
        raise ValueError("provider result request_id does not match execution request")
    if raw.idempotency_key != request.idempotency_key:
        raise ValueError("provider result idempotency_key does not match execution request")
    return ExecutionOutcome(
        request_id=raw.request_id,
        idempotency_key=raw.idempotency_key,
        status=raw.status,
        outcome_code=raw.outcome_code,
        observed_at=raw.observed_at,
        external_reference=raw.external_reference,
    )
