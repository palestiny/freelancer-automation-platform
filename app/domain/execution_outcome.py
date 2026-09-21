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
        if not isinstance(self.status, ExecutionOutcomeStatus):
            raise TypeError("status must be an ExecutionOutcomeStatus")
        if not isinstance(self.observed_at, datetime):
            raise TypeError("observed_at must be a datetime")
        for name in ("request_id", "idempotency_key", "outcome_code"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} cannot be empty")
        if self.external_reference is not None and not isinstance(self.external_reference, str):
            raise TypeError("external_reference must be a string or None")
        if self.external_reference is not None and not self.external_reference.strip():
            raise ValueError("external_reference cannot be empty")
        if self.observed_at.tzinfo is None or self.observed_at.utcoffset() is None:
            raise ValueError("observed_at must be timezone-aware")


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
    if not isinstance(status, ExecutionOutcomeStatus):
        raise TypeError("status must be an ExecutionOutcomeStatus")
    if not isinstance(observed_at, datetime):
        raise TypeError("observed_at must be a datetime")
    if observed_at.tzinfo is None or observed_at.utcoffset() is None:
        raise ValueError("observed_at must be timezone-aware")
    if external_reference is not None and not isinstance(external_reference, str):
        raise TypeError("external_reference must be a string or None")
    if external_reference is not None and not external_reference.strip():
        raise ValueError("external_reference cannot be empty")
    if request.prepared_at is not None and (
        request.prepared_at.tzinfo is None or request.prepared_at.utcoffset() is None
    ):
        raise ValueError("prepared_at must be timezone-aware")
    if request.prepared_at is not None and observed_at < request.prepared_at:
        raise ValueError("observed_at cannot precede prepared_at")
    return ExecutionOutcome(
        request_id=request.request_id,
        idempotency_key=request.idempotency_key,
        status=status,
        outcome_code=outcome_code,
        observed_at=observed_at,
        external_reference=external_reference,
    )
