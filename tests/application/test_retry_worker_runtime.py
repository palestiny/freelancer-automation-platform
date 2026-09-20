from datetime import datetime, timezone

from app.application.retry_worker_dispatch import RetryWorkerDispatchResult, RetryWorkerDispatchStatus
from app.application.retry_worker_runtime import RetryWorkerRuntimeOutcome, run_retry_worker_once
from app.domain.execution_retry import RetryCommand, RetryCommandAction, RetryCommandState


def command(command_id="cmd-1", state=RetryCommandState.SCHEDULED):
    return RetryCommand(
        command_id=command_id, request_id="req-1", idempotency_key="idem-1",
        attempt_number=1, action=RetryCommandAction.RETRY,
        authorization_policy_id="policy", authorization_policy_version="v1",
        autonomy_bound="L4", created_at=datetime(2026, 9, 20, tzinfo=timezone.utc),
        state=state, scheduling_id="schedule-1",
    )


class Source:
    def __init__(self, value=None, error=None):
        self.value = value
        self.error = error
        self.calls = 0

    def next_scheduled(self):
        self.calls += 1
        if self.error:
            raise self.error
        return self.value


class Dispatcher:
    def __init__(self, result=None, error=None):
        self.result = result
        self.error = error
        self.calls = 0
        self.commands = []

    def __call__(self, command):
        self.calls += 1
        self.commands.append(command)
        if self.error:
            raise self.error
        return self.result


def result(command, status):
    return RetryWorkerDispatchResult(command=command, status=status)


def test_idle_does_not_dispatch():
    source = Source()
    dispatcher = Dispatcher()
    runtime = run_retry_worker_once(source=source, dispatch=dispatcher)

    assert runtime.outcome is RetryWorkerRuntimeOutcome.IDLE
    assert source.calls == 1
    assert dispatcher.calls == 0


def test_one_invocation_dispatches_exactly_one_command():
    cmd = command()
    source = Source(cmd)
    dispatcher = Dispatcher(result(cmd, RetryWorkerDispatchStatus.COMPLETED))

    runtime = run_retry_worker_once(source=source, dispatch=dispatcher)

    assert runtime.outcome is RetryWorkerRuntimeOutcome.DISPATCHED
    assert dispatcher.calls == 1
    assert dispatcher.commands == [cmd]


def test_claim_conflict_is_blocked():
    cmd = command()
    source = Source(cmd)
    dispatcher = Dispatcher(result(cmd, RetryWorkerDispatchStatus.CLAIM_NOT_ACQUIRED))

    runtime = run_retry_worker_once(source=source, dispatch=dispatcher)

    assert runtime.outcome is RetryWorkerRuntimeOutcome.BLOCKED
    assert runtime.dispatch_result is not None


def test_dispatch_failure_is_still_a_dispatched_invocation():
    cmd = command()
    source = Source(cmd)
    dispatcher = Dispatcher(
        result(cmd, RetryWorkerDispatchStatus.PROVIDER_FAILURE)
    )

    runtime = run_retry_worker_once(source=source, dispatch=dispatcher)

    assert runtime.outcome is RetryWorkerRuntimeOutcome.DISPATCHED


def test_source_failure_is_failed_and_not_hidden():
    source = Source(error=RuntimeError("store unavailable"))
    dispatcher = Dispatcher()

    runtime = run_retry_worker_once(source=source, dispatch=dispatcher)

    assert runtime.outcome is RetryWorkerRuntimeOutcome.FAILED
    assert runtime.failure == "work_source_failed"
    assert dispatcher.calls == 0


def test_dispatch_exception_is_failed_and_not_retried():
    cmd = command()
    source = Source(cmd)
    dispatcher = Dispatcher(error=RuntimeError("dispatch unavailable"))

    runtime = run_retry_worker_once(source=source, dispatch=dispatcher)

    assert runtime.outcome is RetryWorkerRuntimeOutcome.FAILED
    assert runtime.failure == "dispatch_failed"
    assert dispatcher.calls == 1


def test_runtime_does_not_accept_non_scheduled_work():
    cmd = command(state=RetryCommandState.COMPLETED)
    source = Source(cmd)
    dispatcher = Dispatcher()

    runtime = run_retry_worker_once(source=source, dispatch=dispatcher)

    assert runtime.outcome is RetryWorkerRuntimeOutcome.FAILED
    assert runtime.failure == "invalid_scheduled_work"
    assert dispatcher.calls == 0


def test_claim_persistence_failure_is_failed_not_blocked():
    cmd = command()
    source = Source(cmd)
    dispatcher = Dispatcher(result=RetryWorkerDispatchResult(command=cmd, status=RetryWorkerDispatchStatus.CLAIM_NOT_ACQUIRED, failure="claim_persistence_failed"))
    runtime = run_retry_worker_once(source=source, dispatch=dispatcher)
    assert runtime.outcome is RetryWorkerRuntimeOutcome.FAILED
    assert runtime.failure == "dispatch_claim_failed"
