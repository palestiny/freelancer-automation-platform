from datetime import datetime, timezone

from app.application.retry_execution_handoff import claim_retry_for_execution
from app.domain.execution_retry import RetryCommand, RetryCommandAction, RetryCommandState


class Store:
    def __init__(self, command):
        self.command = command

    def claim(self, command_id):
        if self.command.command_id != command_id:
            return None
        if self.command.state is not RetryCommandState.SCHEDULED:
            return None
        self.command = self.command.transition_to(RetryCommandState.EXECUTION_IN_PROGRESS)
        return self.command


def command(state=RetryCommandState.SCHEDULED):
    return RetryCommand(
        command_id="cmd-1", request_id="req-1", idempotency_key="idem-1",
        attempt_number=2, action=RetryCommandAction.RETRY,
        authorization_policy_id="policy-1", authorization_policy_version="v1",
        autonomy_bound="L3", created_at=datetime(2026, 9, 20, tzinfo=timezone.utc),
        state=state, scheduling_id="sched-1",
    )


def test_claim_creates_execution_handoff():
    cmd = command()
    result = claim_retry_for_execution(command=cmd, store=Store(cmd))
    assert result.claimed is True
    assert result.handoff.command_id == "cmd-1"
    assert result.handoff.request_id == "req-1"
    assert result.handoff.attempt_number == 2
    assert result.handoff.idempotency_key == "idem-1"
    assert result.command.state is RetryCommandState.EXECUTION_IN_PROGRESS


def test_non_scheduled_command_is_not_claimed():
    cmd = command(RetryCommandState.REQUIRES_MANUAL_REVIEW)
    result = claim_retry_for_execution(command=cmd, store=Store(cmd))
    assert result.claimed is False
    assert result.handoff is None
    assert result.failure == "command_not_execution_ready"


def test_claim_race_is_explicit():
    cmd = command()
    store = Store(cmd)
    store.claim = lambda command_id: None
    result = claim_retry_for_execution(command=cmd, store=store)
    assert result.claimed is False
    assert result.handoff is None
    assert result.failure == "claim_conflict"


def test_persistence_failure_does_not_report_execution():
    cmd = command()
    store = Store(cmd)
    store.claim = lambda command_id: (_ for _ in ()).throw(RuntimeError("db down"))
    result = claim_retry_for_execution(command=cmd, store=store)
    assert result.claimed is False
    assert result.handoff is None
    assert result.failure == "claim_persistence_failed"
