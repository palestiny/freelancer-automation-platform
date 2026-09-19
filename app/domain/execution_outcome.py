from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from .authorized_execution_request import AuthorizedExecutionRequest, ExecutionRequestStatus


class ExecutionOutcomeStatus(str, Enum):
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    REJECTED = "rejected"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class ExecutionOutcome:
    request_id: str
    idempotency_key: str
    status: ExecutionOutcomeStatus
    outcome_code: str
    observed_at: datetime
    external_reference: str | None = None

    def __post_init__(self) -> None:
        for name in ("request_id", "idempotency_key", "outcome_code"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} cannot be empty")
        if self.external_reference is not None and not self.external_reference.strip():
            raise ValueError("external_reference cannot be empty")


def record_execution_outcome(
    *,
    request: AuthorizedExecutionRequest,
    status: ExecutionOutcomeStatus,
    outcome_code: str,
    observed_at: datetime,
    external_reference: str | None = None,
) -> ExecutionOutcome:
    if request.status is not ExecutionRequestStatus.PREPARED:
        raise ValueError("execution outcome requires a prepared execution request")
    return ExecutionOutcome(
        request_id=request.request_id,
        idempotency_key=request.idempotency_key,
        status=status,
        outcome_code=outcome_code,
        observed_at=observed_at,
        external_reference=external_reference,
    )
