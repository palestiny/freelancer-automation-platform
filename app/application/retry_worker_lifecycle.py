from dataclasses import dataclass
from enum import Enum
from typing import Callable

from app.application.retry_worker_runtime import RetryWorkerRuntimeOutcome, RetryWorkerRuntimeResult


class RetryWorkerLifecycleState(str, Enum):
    STOPPED = "stopped"
    STARTING = "starting"
    RUNNING = "running"
    STOPPING = "stopping"
    STOPPED_WITH_ERROR = "stopped_with_error"


class RetryWorkerLifecycleStopReason(str, Enum):
    STOP_REQUESTED = "stop_requested"
    WAKEUP_STOPPED = "wakeup_stopped"
    IDLE = "idle"
    BLOCKED = "blocked"
    INVOCATION_FAILED = "invocation_failed"


@dataclass(frozen=True)
class RetryWorkerLifecycleResult:
    state: RetryWorkerLifecycleState
    stop_reason: RetryWorkerLifecycleStopReason
    transitions: tuple[RetryWorkerLifecycleState, ...]
    last_invocation: RetryWorkerRuntimeResult | None = None
    failure: str | None = None


class RetryWorkerLifecycleController:
    def __init__(
        self,
        *,
        invoke_once: Callable[[], RetryWorkerRuntimeResult],
        wait_for_wakeup: Callable[[], bool],
        stop_requested: Callable[[], bool],
    ) -> None:
        self._invoke_once = invoke_once
        self._wait_for_wakeup = wait_for_wakeup
        self._stop_requested = stop_requested

    def run(self) -> RetryWorkerLifecycleResult:
        transitions = [
            RetryWorkerLifecycleState.STOPPED,
            RetryWorkerLifecycleState.STARTING,
        ]

        if self._stop_requested():
            transitions.extend(
                [RetryWorkerLifecycleState.STOPPING, RetryWorkerLifecycleState.STOPPED]
            )
            return RetryWorkerLifecycleResult(
                state=RetryWorkerLifecycleState.STOPPED,
                stop_reason=RetryWorkerLifecycleStopReason.STOP_REQUESTED,
                transitions=tuple(transitions),
            )

        transitions.append(RetryWorkerLifecycleState.RUNNING)
        last_invocation = None

        while True:
            if self._stop_requested():
                transitions.extend(
                    [RetryWorkerLifecycleState.STOPPING, RetryWorkerLifecycleState.STOPPED]
                )
                return RetryWorkerLifecycleResult(
                    state=RetryWorkerLifecycleState.STOPPED,
                    stop_reason=RetryWorkerLifecycleStopReason.STOP_REQUESTED,
                    transitions=tuple(transitions),
                    last_invocation=last_invocation,
                )

            result = self._invoke_once()
            last_invocation = result

            if result.outcome is RetryWorkerRuntimeOutcome.DISPATCHED:
                continue

            if result.outcome is RetryWorkerRuntimeOutcome.FAILED:
                transitions.append(RetryWorkerLifecycleState.STOPPED_WITH_ERROR)
                return RetryWorkerLifecycleResult(
                    state=RetryWorkerLifecycleState.STOPPED_WITH_ERROR,
                    stop_reason=RetryWorkerLifecycleStopReason.INVOCATION_FAILED,
                    transitions=tuple(transitions),
                    last_invocation=result,
                    failure=result.failure,
                )

            if result.outcome is RetryWorkerRuntimeOutcome.BLOCKED:
                transitions.extend(
                    [RetryWorkerLifecycleState.STOPPING, RetryWorkerLifecycleState.STOPPED]
                )
                return RetryWorkerLifecycleResult(
                    state=RetryWorkerLifecycleState.STOPPED,
                    stop_reason=RetryWorkerLifecycleStopReason.BLOCKED,
                    transitions=tuple(transitions),
                    last_invocation=result,
                )

            if self._stop_requested():
                transitions.extend(
                    [RetryWorkerLifecycleState.STOPPING, RetryWorkerLifecycleState.STOPPED]
                )
                return RetryWorkerLifecycleResult(
                    state=RetryWorkerLifecycleState.STOPPED,
                    stop_reason=RetryWorkerLifecycleStopReason.STOP_REQUESTED,
                    transitions=tuple(transitions),
                    last_invocation=result,
                )

            if not self._wait_for_wakeup():
                transitions.extend(
                    [RetryWorkerLifecycleState.STOPPING, RetryWorkerLifecycleState.STOPPED]
                )
                return RetryWorkerLifecycleResult(
                    state=RetryWorkerLifecycleState.STOPPED,
                    stop_reason=RetryWorkerLifecycleStopReason.WAKEUP_STOPPED,
                    transitions=tuple(transitions),
                    last_invocation=result,
                )
