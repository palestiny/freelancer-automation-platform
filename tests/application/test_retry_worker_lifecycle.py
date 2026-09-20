from app.application.retry_worker_lifecycle import (
    RetryWorkerLifecycleState,
    RetryWorkerLifecycleStopReason,
    RetryWorkerLifecycleController,
)
from app.application.retry_worker_runtime import RetryWorkerRuntimeOutcome, RetryWorkerRuntimeResult


def _controller(results, *, wakeups=None, stop=None):
    queue = list(results)
    wakeups = list(wakeups or [])
    stopped = stop if stop is not None else {"value": False}

    def run_once():
        return queue.pop(0)

    def wait():
        return wakeups.pop(0) if wakeups else True

    def is_stop_requested():
        return stopped["value"]

    controller = RetryWorkerLifecycleController(
        invoke_once=run_once,
        wait_for_wakeup=wait,
        stop_requested=is_stop_requested,
    )
    return controller, stopped


def test_starts_runs_and_stops_explicitly():
    controller, stopped = _controller(
        [
            RetryWorkerRuntimeResult(RetryWorkerRuntimeOutcome.DISPATCHED),
        ],
    )

    stopped["value"] = True
    result = controller.run()

    assert result.state is RetryWorkerLifecycleState.STOPPED
    assert result.stop_reason is RetryWorkerLifecycleStopReason.STOP_REQUESTED
    assert result.transitions == (
        RetryWorkerLifecycleState.STOPPED,
        RetryWorkerLifecycleState.STARTING,
        RetryWorkerLifecycleState.RUNNING,
        RetryWorkerLifecycleState.STOPPING,
        RetryWorkerLifecycleState.STOPPED,
    )


def test_idle_waits_instead_of_busy_polling():
    calls = {"wait": 0}
    controller, stopped = _controller(
        [
            RetryWorkerRuntimeResult(RetryWorkerRuntimeOutcome.IDLE),
        ],
        wakeups=[False],
    )

    def wait():
        calls["wait"] += 1
        return False

    controller._wait_for_wakeup = wait
    result = controller.run()

    assert calls["wait"] == 1
    assert result.state is RetryWorkerLifecycleState.STOPPED
    assert result.stop_reason is RetryWorkerLifecycleStopReason.WAKEUP_STOPPED


def test_failed_invocation_stops_with_error():
    controller, _ = _controller(
        [
            RetryWorkerRuntimeResult(
                RetryWorkerRuntimeOutcome.FAILED,
                failure="work_source_failed",
            ),
        ],
    )

    result = controller.run()

    assert result.state is RetryWorkerLifecycleState.STOPPED_WITH_ERROR
    assert result.stop_reason is RetryWorkerLifecycleStopReason.INVOCATION_FAILED
    assert result.failure == "work_source_failed"


def test_blocked_invocation_does_not_implicitly_retry():
    controller, _ = _controller(
        [
            RetryWorkerRuntimeResult(RetryWorkerRuntimeOutcome.BLOCKED),
        ],
        wakeups=[False],
    )

    result = controller.run()

    assert result.state is RetryWorkerLifecycleState.STOPPED
    assert result.stop_reason is RetryWorkerLifecycleStopReason.BLOCKED


def test_start_does_not_execute_after_stop_request():
    stopped = {"value": True}
    invoked = {"value": 0}

    def invoke():
        invoked["value"] += 1
        return RetryWorkerRuntimeResult(RetryWorkerRuntimeOutcome.IDLE)

    controller = RetryWorkerLifecycleController(
        invoke_once=invoke,
        wait_for_wakeup=lambda: True,
        stop_requested=lambda: stopped["value"],
    )

    result = controller.run()

    assert invoked["value"] == 0
    assert result.state is RetryWorkerLifecycleState.STOPPED
    assert result.stop_reason is RetryWorkerLifecycleStopReason.STOP_REQUESTED
