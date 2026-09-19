from datetime import datetime, timezone

from app.application.retry_execution_outcome import record_retry_execution_outcome
from app.domain.execution_outcome import ExecutionOutcome, ExecutionOutcomeStatus
from app.domain.execution_retry import RetryCommand, RetryCommandAction, RetryCommandState


class Store:
    def __init__(self, command):
        self.command = command

    def save(self, command):
        self.command = command
        return command


def command(state=RetryCommandState.EXECUTION_IN_PROGRESS):
    return RetryCommand(
        command_id="cmd-1", request_id="req-1", idempotency_key="idem-1",
        attempt_number=2, action=RetryCommandAction.RETRY,
        authorization_policy_id="policy-1", authorization_policy_version="v1",
        autonomy_bound="L3", created_at=datetime(2026, 9, 20, tzinfo=timezone.utc),
        state=state, scheduling_id="sched-1",
    )


def outcome(status=ExecutionOutcomeStatus.SUCCEEDED):
    return ExecutionOutcome(
        request_id="req-1", idempotency_key="idem-1", status=status,
        outcome_code=status.value, observed_at=datetime(2026, 9, 20, 1, tzinfo=timezone.utc),
    )


def test_success_completes_retry_command():
    cmd = command()
    result = record_retry_execution_outcome(command=cmd, outcome=outcome(), store=Store(cmd))
    assert result.command.state is RetryCommandState.COMPLETED
    assert result.recorded is True
    assert result.failure is None


def test_failed_outcome_goes_to_manual_review_without_retry():
    cmd = command()
    result = record_retry_execution_outcome(command=cmd, outcome=outcome(ExecutionOutcomeStatus.FAILED), store=Store(cmd))
    assert result.command.state is RetryCommandState.REQUIRES_MANUAL_REVIEW
    assert result.recorded is True


def test_identity_mismatch_is_rejected():
    cmd = command()
    bad = ExecutionOutcome("other", "idem-1", ExecutionOutcomeStatus.SUCCEEDED, "ok", datetime(2026, 9, 20, tzinfo=timezone.utc))
    result = record_retry_execution_outcome(command=cmd, outcome=bad, store=Store(cmd))
    assert result.recorded is False
    assert result.failure == "outcome_identity_mismatch"


def test_non_in_progress_command_is_rejected():
    cmd = command(RetryCommandState.COMPLETED)
    result = record_retry_execution_outcome(command=cmd, outcome=outcome(), store=Store(cmd))
    assert result.recorded is False
    assert result.failure == "command_not_in_execution"


def test_persistence_failure_does_not_report_recorded():
    cmd = command()
    class FailingStore(Store):
        def save(self, command):
            raise RuntimeError("db down")
    result = record_retry_execution_outcome(command=cmd, outcome=outcome(), store=FailingStore(cmd))
    assert result.recorded is False
    assert result.failure == "outcome_persistence_failed"
