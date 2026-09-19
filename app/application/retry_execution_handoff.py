from dataclasses import dataclass
from typing import Protocol

from app.domain.execution_retry import RetryCommand, RetryCommandState


@dataclass(frozen=True)
class RetryExecutionHandoff:
    command_id: str
    request_id: str
    idempotency_key: str
    attempt_number: int
    authorization_policy_id: str
    authorization_policy_version: str
    autonomy_bound: str
    scheduling_id: str

    def __post_init__(self) -> None:
        for name in (
            "command_id", "request_id", "idempotency_key",
            "authorization_policy_id", "authorization_policy_version",
            "autonomy_bound", "scheduling_id",
        ):
            if not getattr(self, name).strip():
                raise ValueError(f"{name} cannot be empty")
        if self.attempt_number <= 0:
            raise ValueError("attempt_number must be greater than zero")


@dataclass(frozen=True)
class RetryExecutionClaimResult:
    command: RetryCommand
    claimed: bool
    handoff: RetryExecutionHandoff | None
    failure: str | None = None


class RetryExecutionClaimStore(Protocol):
    def claim(self, command_id: str) -> RetryCommand | None:
        ...


def claim_retry_for_execution(*, command: RetryCommand, store: RetryExecutionClaimStore) -> RetryExecutionClaimResult:
    if command.state is not RetryCommandState.SCHEDULED:
        return RetryExecutionClaimResult(command=command, claimed=False, handoff=None, failure="command_not_execution_ready")
    try:
        claimed = store.claim(command.command_id)
    except Exception:
        return RetryExecutionClaimResult(command=command, claimed=False, handoff=None, failure="claim_persistence_failed")
    if claimed is None:
        return RetryExecutionClaimResult(command=command, claimed=False, handoff=None, failure="claim_conflict")
    if claimed.state is not RetryCommandState.EXECUTION_IN_PROGRESS:
        return RetryExecutionClaimResult(command=claimed, claimed=False, handoff=None, failure="claim_state_invalid")
    if not claimed.scheduling_id:
        return RetryExecutionClaimResult(command=claimed, claimed=False, handoff=None, failure="missing_scheduling_identity")
    return RetryExecutionClaimResult(
        command=claimed,
        claimed=True,
        handoff=RetryExecutionHandoff(
            command_id=claimed.command_id, request_id=claimed.request_id,
            idempotency_key=claimed.idempotency_key, attempt_number=claimed.attempt_number,
            authorization_policy_id=claimed.authorization_policy_id,
            authorization_policy_version=claimed.authorization_policy_version,
            autonomy_bound=claimed.autonomy_bound, scheduling_id=claimed.scheduling_id,
        ),
    )
