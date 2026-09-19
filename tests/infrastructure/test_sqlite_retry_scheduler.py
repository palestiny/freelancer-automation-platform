from datetime import datetime, timezone

from app.domain.execution_retry import RetryCommand, RetryCommandAction, SchedulerAcknowledgementStatus
from app.infrastructure.sqlite_retry_scheduler import SQLiteRetryScheduler


def command(command_id="cmd-1", attempt=1):
    return RetryCommand(
        command_id=command_id,
        request_id="req-1",
        idempotency_key="idem-1",
        attempt_number=attempt,
        action=RetryCommandAction.RETRY,
        authorization_policy_id="policy",
        authorization_policy_version="v1",
        autonomy_bound="L3",
        created_at=datetime(2026, 9, 20, tzinfo=timezone.utc),
    )


def test_schedule_persists_and_accepts():
    scheduler = SQLiteRetryScheduler(":memory:")
    ack = scheduler.schedule(command())

    assert ack.command_id == "cmd-1"
    assert ack.scheduling_id
    assert ack.status is SchedulerAcknowledgementStatus.ACCEPTED
    assert ack.observed_at.tzinfo is not None


def test_schedule_is_idempotent_for_same_command():
    scheduler = SQLiteRetryScheduler(":memory:")
    first = scheduler.schedule(command())
    second = scheduler.schedule(command())

    assert second.scheduling_id == first.scheduling_id


def test_different_attempts_have_distinct_schedule_identity():
    scheduler = SQLiteRetryScheduler(":memory:")
    first = scheduler.schedule(command(attempt=1))
    second = scheduler.schedule(command(attempt=2))

    assert second.scheduling_id != first.scheduling_id


def test_schedule_survives_connection_reopen(tmp_path):
    path = str(tmp_path / "scheduler.sqlite3")
    first = SQLiteRetryScheduler(path)
    ack = first.schedule(command())

    second = SQLiteRetryScheduler(path)
    restored = second.schedule(command())

    assert restored.scheduling_id == ack.scheduling_id
