from dataclasses import dataclass
from enum import Enum
from typing import Callable, Protocol

from app.application.retry_worker_dispatch import RetryWorkerDispatchResult, RetryWorkerDispatchStatus
from app.domain.execution_retry import RetryCommand, RetryCommandState


class RetryWorkerRuntimeOutcome(str, Enum):
    DISPATCHED = "dispatched"
    IDLE = "idle"
    BLOCKED = "blocked"
    FAILED = "failed"


@dataclass(frozen=True)
class RetryWorkerRuntimeResult:
    outcome: RetryWorkerRuntimeOutcome
    command: RetryCommand | None = None
    dispatch_result: RetryWorkerDispatchResult | None = None
    failure: str | None = None


class RetryWorkerWorkSource(Protocol):
    def next_scheduled(self) -> RetryCommand | None:
        ...


def run_retry_worker_once(
    *,
    source: RetryWorkerWorkSource,
    dispatch: Callable[[RetryCommand], RetryWorkerDispatchResult],
) -> RetryWorkerRuntimeResult:
    try:
        command = source.next_scheduled()
    except Exception:
        return RetryWorkerRuntimeResult(
            outcome=RetryWorkerRuntimeOutcome.FAILED,
            failure="work_source_failed",
        )

    if command is None:
        return RetryWorkerRuntimeResult(outcome=RetryWorkerRuntimeOutcome.IDLE)

    if not isinstance(command, RetryCommand):
        return RetryWorkerRuntimeResult(
            outcome=RetryWorkerRuntimeOutcome.FAILED,
            failure="invalid_scheduled_work",
        )

    if command.state is not RetryCommandState.SCHEDULED:
        return RetryWorkerRuntimeResult(
            outcome=RetryWorkerRuntimeOutcome.FAILED,
            command=command,
            failure="invalid_scheduled_work",
        )

    try:
        dispatch_result = dispatch(command)
    except Exception:
        return RetryWorkerRuntimeResult(
            outcome=RetryWorkerRuntimeOutcome.FAILED,
            command=command,
            failure="dispatch_failed",
        )

    if not isinstance(dispatch_result, RetryWorkerDispatchResult):
        return RetryWorkerRuntimeResult(
            outcome=RetryWorkerRuntimeOutcome.FAILED,
            command=command,
            failure="invalid_dispatch_result",
        )

    if dispatch_result.command.command_id != command.command_id:
        return RetryWorkerRuntimeResult(
            outcome=RetryWorkerRuntimeOutcome.FAILED,
            command=command,
            dispatch_result=dispatch_result,
            failure="dispatch_result_identity_mismatch",
        )

    if dispatch_result.status is RetryWorkerDispatchStatus.CLAIM_NOT_ACQUIRED:
        if dispatch_result.failure == "claim_conflict":
            return RetryWorkerRuntimeResult(
                outcome=RetryWorkerRuntimeOutcome.BLOCKED,
                command=command,
                dispatch_result=dispatch_result,
            )
        return RetryWorkerRuntimeResult(
            outcome=RetryWorkerRuntimeOutcome.FAILED,
            command=command,
            dispatch_result=dispatch_result,
            failure="dispatch_claim_failed",
        )

    return RetryWorkerRuntimeResult(
        outcome=RetryWorkerRuntimeOutcome.DISPATCHED,
        command=command,
        dispatch_result=dispatch_result,
    )
