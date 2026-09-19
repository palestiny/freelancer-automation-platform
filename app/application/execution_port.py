from abc import ABC, abstractmethod

from app.domain.authorized_execution_request import AuthorizedExecutionRequest, ExecutionRequestStatus
from app.domain.execution_outcome import ExecutionOutcome


class ExecutionPort(ABC):
    @abstractmethod
    def execute(self, request: AuthorizedExecutionRequest) -> dict:
        """Provider adapter contract; implementations live outside the domain."""


def dispatch_execution(*, port: ExecutionPort, request: AuthorizedExecutionRequest) -> ExecutionOutcome:
    if request.status is not ExecutionRequestStatus.PREPARED:
        raise ValueError("execution dispatch requires a prepared execution request")
    raw = port.execute(request)
    return ExecutionOutcome(
        request_id=raw["request_id"],
        idempotency_key=raw["idempotency_key"],
        status=raw["status"],
        outcome_code=raw["outcome_code"],
        observed_at=raw["observed_at"],
        external_reference=raw.get("external_reference"),
    )
