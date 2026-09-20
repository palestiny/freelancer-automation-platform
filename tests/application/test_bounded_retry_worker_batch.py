from datetime import datetime, timezone

import pytest

from app.application.retry_worker_dispatch import RetryWorkerDispatchResult, RetryWorkerDispatchStatus
from app.application.retry_worker_runtime import RetryWorkerRuntimeOutcome, run_retry_worker_once
from app.application.bounded_retry_worker_batch import (
    RetryWorkerBatchStopReason,
    run_retry_worker_batch,
)
from app.domain.execution_retry import RetryCommand, RetryCommandAction, RetryCommandState


def command(command_id):
    return RetryCommand(
        command_id=command_id, request_id=command_id, idempotency_key=command_id,
        attempt_number=1, action=RetryCommandAction.RETRY,
        authorization_policy_id="policy", authorization_policy_version="v1",
        autonomy_bound="L4", created_at=datetime(2026, 9, 20, tzinfo=timezone.utc),
        state=RetryCommandState.SCHEDULED, scheduling_id=f"s-{command_id}",
    )


class Source:
    def __init__(self, commands):
        self.commands = list(commands)

    def next_scheduled(self):
        return self.commands.pop(0) if self.commands else None


class Dispatcher:
    def __init__(self, statuses):
        self.statuses = list(statuses)
        self.calls = 0

    def __call__(self, command):
        self.calls += 1
        status = self.statuses.pop(0)
        return RetryWorkerDispatchResult(command=command, status=status)


def test_batch_stops_at_idle_after_dispatched_work():
    source = Source([command("a")])
    dispatcher = Dispatcher([RetryWorkerDispatchStatus.COMPLETED])
    result = run_retry_worker_batch(source=source, dispatch=dispatcher, max_invocations=5)

    assert result.stop_reason is RetryWorkerBatchStopReason.IDLE
    assert result.invocation_count == 2
    assert result.dispatched_count == 1
    assert [item.outcome for item in result.invocations] == [
        RetryWorkerRuntimeOutcome.DISPATCHED,
        RetryWorkerRuntimeOutcome.IDLE,
    ]


def test_batch_stops_at_explicit_limit():
    source = Source([command("a"), command("b"), command("c")])
    dispatcher = Dispatcher([
        RetryWorkerDispatchStatus.COMPLETED,
        RetryWorkerDispatchStatus.COMPLETED,
    ])
    result = run_retry_worker_batch(source=source, dispatch=dispatcher, max_invocations=2)

    assert result.stop_reason is RetryWorkerBatchStopReason.MAX_INVOCATIONS
    assert result.invocation_count == 2
    assert result.dispatched_count == 2


def test_blocked_stops_batch_without_spinning():
    source = Source([command("a"), command("b")])
    dispatcher = Dispatcher([RetryWorkerDispatchStatus.CLAIM_NOT_ACQUIRED])
    result = run_retry_worker_batch(source=source, dispatch=lambda cmd: RetryWorkerDispatchResult(command=cmd, status=RetryWorkerDispatchStatus.CLAIM_NOT_ACQUIRED, failure="claim_conflict"), max_invocations=5)

    assert result.stop_reason is RetryWorkerBatchStopReason.BLOCKED
    assert result.invocation_count == 1
    assert result.dispatched_count == 0


def test_failed_stops_batch_without_retrying():
    source = Source([command("a"), command("b")])
    dispatcher = Dispatcher([RetryWorkerDispatchStatus.CLAIM_NOT_ACQUIRED])
    # A non-claim-conflict failure is converted to FAILED by the single-command boundary.
    dispatcher.statuses[0] = RetryWorkerDispatchStatus.CLAIM_NOT_ACQUIRED
    result = run_retry_worker_batch(
        source=source,
        dispatch=lambda cmd: RetryWorkerDispatchResult(
            command=cmd,
            status=RetryWorkerDispatchStatus.CLAIM_NOT_ACQUIRED,
            failure="claim_persistence_failed",
        ),
        max_invocations=5,
    )

    assert result.stop_reason is RetryWorkerBatchStopReason.FAILED
    assert result.invocation_count == 1


def test_max_invocations_must_be_positive():
    with pytest.raises(ValueError):
        run_retry_worker_batch(
            source=Source([]),
            dispatch=Dispatcher([]),
            max_invocations=0,
        )
