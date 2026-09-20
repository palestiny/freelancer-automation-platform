from dataclasses import dataclass
from enum import Enum
from typing import Callable

from app.application.retry_worker_dispatch import RetryWorkerDispatchResult
from app.application.retry_worker_runtime import (
    RetryWorkerRuntimeOutcome,
    RetryWorkerRuntimeResult,
    RetryWorkerWorkSource,
    run_retry_worker_once,
)
from app.domain.execution_retry import RetryCommand


class RetryWorkerBatchStopReason(str, Enum):
    IDLE = "idle"
    BLOCKED = "blocked"
    FAILED = "failed"
    MAX_INVOCATIONS = "max_invocations"


@dataclass(frozen=True)
class RetryWorkerBatchResult:
    invocations: tuple[RetryWorkerRuntimeResult, ...]
    stop_reason: RetryWorkerBatchStopReason

    @property
    def invocation_count(self) -> int:
        return len(self.invocations)

    @property
    def dispatched_count(self) -> int:
        return sum(
            result.outcome is RetryWorkerRuntimeOutcome.DISPATCHED
            for result in self.invocations
        )


def run_retry_worker_batch(
    *,
    source: RetryWorkerWorkSource,
    dispatch: Callable[[RetryCommand], RetryWorkerDispatchResult],
    max_invocations: int,
) -> RetryWorkerBatchResult:
    if isinstance(max_invocations, bool) or not isinstance(max_invocations, int):
        raise TypeError("max_invocations must be an integer")
    if max_invocations <= 0:
        raise ValueError("max_invocations must be greater than zero")

    results: list[RetryWorkerRuntimeResult] = []

    for _ in range(max_invocations):
        result = run_retry_worker_once(source=source, dispatch=dispatch)
        results.append(result)

        if result.outcome is RetryWorkerRuntimeOutcome.IDLE:
            return RetryWorkerBatchResult(tuple(results), RetryWorkerBatchStopReason.IDLE)
        if result.outcome is RetryWorkerRuntimeOutcome.BLOCKED:
            return RetryWorkerBatchResult(tuple(results), RetryWorkerBatchStopReason.BLOCKED)
        if result.outcome is RetryWorkerRuntimeOutcome.FAILED:
            return RetryWorkerBatchResult(tuple(results), RetryWorkerBatchStopReason.FAILED)

    return RetryWorkerBatchResult(
        tuple(results),
        RetryWorkerBatchStopReason.MAX_INVOCATIONS,
    )
