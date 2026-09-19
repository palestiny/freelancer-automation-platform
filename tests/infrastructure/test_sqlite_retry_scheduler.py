import pytest
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
    first = scheduler.schedule(command(command_id="cmd-1", attempt=1))
    second = scheduler.schedule(command(command_id="cmd-2", attempt=2))

    assert second.scheduling_id != first.scheduling_id


def test_schedule_survives_connection_reopen(tmp_path):
    path = str(tmp_path / "scheduler.sqlite3")
    first = SQLiteRetryScheduler(path)
    ack = first.schedule(command())

    second = SQLiteRetryScheduler(path)
    restored = second.schedule(command())

    assert restored.scheduling_id == ack.scheduling_id


def test_schedule_rejects_same_logical_retry_with_different_command_identity():
    scheduler = SQLiteRetryScheduler(":memory:")
    scheduler.schedule(command(command_id="cmd-1"))
    with pytest.raises(ValueError, match="command identity conflict"):
        scheduler.schedule(command(command_id="cmd-2"))


def test_schedule_rejects_manual_review_commands():
    from app.domain.execution_retry import RetryCommandAction
    scheduler = SQLiteRetryScheduler(":memory:")
    review = RetryCommand(
        command_id="cmd-review",
        request_id="req-review",
        idempotency_key="idem-review",
        attempt_number=1,
        action=RetryCommandAction.MANUAL_REVIEW,
        authorization_policy_id="policy",
        authorization_policy_version="v1",
        autonomy_bound="L3",
        created_at=datetime(2026, 9, 20, tzinfo=timezone.utc),
    )
    with pytest.raises(ValueError, match="only retry commands"):
        scheduler.schedule(review)


def test_concurrent_schedulers_deduplicate_same_logical_retry(tmp_path):
    from concurrent.futures import ThreadPoolExecutor

    path = str(tmp_path / "concurrent.sqlite3")
    command_value = command()

    def schedule_once():
        return SQLiteRetryScheduler(path).schedule(command_value).scheduling_id

    with ThreadPoolExecutor(max_workers=8) as executor:
        scheduling_ids = list(executor.map(lambda _: schedule_once(), range(8)))

    assert len(set(scheduling_ids)) == 1


def test_concurrent_conflicting_command_identity_has_single_winner(tmp_path):
    from concurrent.futures import ThreadPoolExecutor

    path = str(tmp_path / "conflict.sqlite3")
    commands = [
        command(command_id=f"cmd-{index}")
        for index in range(8)
    ]

    def schedule_once(value):
        try:
            return ("accepted", SQLiteRetryScheduler(path).schedule(value).scheduling_id)
        except ValueError as exc:
            return ("conflict", str(exc))

    with ThreadPoolExecutor(max_workers=8) as executor:
        results = list(executor.map(schedule_once, commands))

    accepted = [result for result in results if result[0] == "accepted"]
    conflicts = [result for result in results if result[0] == "conflict"]

    assert len(accepted) == 1
    assert len(conflicts) == 7
    assert all("command identity conflict" in result[1] for result in conflicts)
