from datetime import datetime, timezone
import sqlite3

import pytest

from app.domain.execution_retry import (
    RetryCommand,
    RetryCommandAction,
    RetryCommandState,
    SchedulerAcknowledgement,
    SchedulerAcknowledgementStatus,
)
from app.infrastructure.sqlite_retry_command_store import SQLiteRetryCommandStore


def command(command_id="cmd-1", request_id="req-1", created_at=None):
    return RetryCommand(
        command_id=command_id,
        request_id=request_id,
        idempotency_key=f"idem-{request_id}",
        attempt_number=1,
        action=RetryCommandAction.RETRY,
        authorization_policy_id="policy",
        authorization_policy_version="v1",
        autonomy_bound="L3",
        created_at=created_at or datetime(2026, 9, 20, tzinfo=timezone.utc),
    )


def store():
    return SQLiteRetryCommandStore(":memory:")


def test_create_and_get_round_trip_preserves_identity_and_timezone():
    s = store()
    original = command()
    created = s.create_or_get(original)
    loaded = s.get(original.command_id)

    assert created == original
    assert loaded == original
    assert loaded.created_at.tzinfo is not None


def test_duplicate_logical_command_returns_existing_record_when_identity_matches():
    s = store()
    original = command()
    assert s.create_or_get(original) == original

    assert s.create_or_get(command("cmd-1")) == original


def test_atomic_claim_allows_only_one_transition():
    s = store()
    original = s.create_or_get(command())

    first = s.claim(original.command_id)
    second = s.claim(original.command_id)

    assert first is not None
    assert first.state is RetryCommandState.CLAIMED
    assert second is None


def test_save_rejects_invalid_domain_transition():
    s = store()
    original = s.create_or_get(command())
    claimed = s.claim(original.command_id)
    assert claimed is not None

    with pytest.raises(ValueError):
        s.save(original)


def test_scheduler_acknowledgement_transitions_claimed_to_scheduled():
    s = store()
    original = s.create_or_get(command())
    claimed = s.claim(original.command_id)
    assert claimed is not None

    ack = SchedulerAcknowledgement(
        command_id=original.command_id,
        scheduling_id="schedule-1",
        status=SchedulerAcknowledgementStatus.ACCEPTED,
        observed_at=datetime(2026, 9, 20, 1, tzinfo=timezone.utc),
    )
    scheduled = s.record_scheduler_acknowledgement(original.command_id, ack)

    assert scheduled.state is RetryCommandState.SCHEDULED
    assert scheduled.scheduling_id == "schedule-1"


def test_rejected_acknowledgement_requires_manual_review():
    s = store()
    original = s.create_or_get(command())
    claimed = s.claim(original.command_id)
    assert claimed is not None

    ack = SchedulerAcknowledgement(
        command_id=original.command_id,
        scheduling_id="schedule-2",
        status=SchedulerAcknowledgementStatus.REJECTED,
        observed_at=datetime(2026, 9, 20, 1, tzinfo=timezone.utc),
    )
    rejected = s.record_scheduler_acknowledgement(original.command_id, ack)

    assert rejected.state is RetryCommandState.REQUIRES_MANUAL_REVIEW


def test_ambiguous_acknowledgement_is_persisted_as_ambiguous():
    s = store()
    original = s.create_or_get(command())
    claimed = s.claim(original.command_id)
    assert claimed is not None

    ack = SchedulerAcknowledgement(
        command_id=original.command_id,
        scheduling_id="schedule-3",
        status=SchedulerAcknowledgementStatus.AMBIGUOUS,
        observed_at=datetime(2026, 9, 20, 1, tzinfo=timezone.utc),
    )
    ambiguous = s.record_scheduler_acknowledgement(original.command_id, ack)

    assert ambiguous.state is RetryCommandState.SCHEDULING_AMBIGUOUS


def test_acknowledgement_for_unknown_command_is_rejected():
    s = store()
    ack = SchedulerAcknowledgement(
        command_id="missing",
        scheduling_id="schedule",
        status=SchedulerAcknowledgementStatus.ACCEPTED,
        observed_at=datetime(2026, 9, 20, 1, tzinfo=timezone.utc),
    )
    with pytest.raises(KeyError):
        s.record_scheduler_acknowledgement("missing", ack)


def test_mismatched_acknowledgement_command_id_is_rejected():
    s = store()
    original = s.create_or_get(command())
    s.claim(original.command_id)
    ack = SchedulerAcknowledgement(
        command_id="other",
        scheduling_id="schedule",
        status=SchedulerAcknowledgementStatus.ACCEPTED,
        observed_at=datetime(2026, 9, 20, 1, tzinfo=timezone.utc),
    )
    with pytest.raises(ValueError):
        s.record_scheduler_acknowledgement(original.command_id, ack)


def test_persistence_survives_connection_reopen(tmp_path):
    path = str(tmp_path / "retry.sqlite3")
    first = SQLiteRetryCommandStore(path)
    first.create_or_get(command())

    second = SQLiteRetryCommandStore(path)
    assert second.get("cmd-1") == command()


def test_get_rejects_invalid_persisted_state():
    s = store()
    s.create_or_get(command())
    s._connection.execute(
        "UPDATE retry_commands SET state = ? WHERE command_id = ?",
        ("invalid_state", "cmd-1"),
    )
    s._connection.commit()

    with pytest.raises(ValueError):
        s.get("cmd-1")


def test_nonexistent_claim_returns_none():
    assert store().claim("missing") is None


def test_duplicate_logical_command_with_different_command_id_is_rejected():
    s = store()
    original = command("cmd-1")
    s.create_or_get(original)

    with pytest.raises(ValueError, match="command identity conflict"):
        s.create_or_get(command("cmd-2"))


def test_concurrent_create_or_get_deduplicates_same_logical_retry(tmp_path):
    from concurrent.futures import ThreadPoolExecutor

    path = str(tmp_path / "concurrent-store.sqlite3")
    command_value = command()

    def create_once():
        return SQLiteRetryCommandStore(path).create_or_get(command_value).command_id

    with ThreadPoolExecutor(max_workers=8) as executor:
        command_ids = list(executor.map(lambda _: create_once(), range(8)))

    assert command_ids == ["cmd-1"] * 8


def test_concurrent_create_or_get_rejects_conflicting_command_identity(tmp_path):
    from concurrent.futures import ThreadPoolExecutor

    path = str(tmp_path / "conflicting-store.sqlite3")
    commands = [command(command_id=f"cmd-{index}") for index in range(8)]

    def create_once(value):
        try:
            return ("accepted", SQLiteRetryCommandStore(path).create_or_get(value).command_id)
        except ValueError as exc:
            return ("conflict", str(exc))

    with ThreadPoolExecutor(max_workers=8) as executor:
        results = list(executor.map(create_once, commands))

    accepted = [result for result in results if result[0] == "accepted"]
    conflicts = [result for result in results if result[0] == "conflict"]

    assert len(accepted) == 1
    assert len(conflicts) == 7
    assert all("command identity conflict" in result[1] for result in conflicts)

def test_atomic_execution_claim_transitions_scheduled_to_execution_in_progress():
    s = store()
    original = s.create_or_get(command())
    assert s.claim(original.command_id) is not None
    scheduled = s.record_scheduler_acknowledgement(
        original.command_id,
        SchedulerAcknowledgement(
            command_id=original.command_id,
            scheduling_id="schedule-exec",
            status=SchedulerAcknowledgementStatus.ACCEPTED,
            observed_at=datetime(2026, 9, 20, 1, tzinfo=timezone.utc),
        ),
    )
    assert scheduled.state is RetryCommandState.SCHEDULED

    execution_claim = s.claim(original.command_id)

    assert execution_claim is not None
    assert execution_claim.state is RetryCommandState.EXECUTION_IN_PROGRESS
    assert execution_claim.scheduling_id == "schedule-exec"
    assert s.claim(original.command_id) is None


def test_execution_claim_requires_scheduled_state_after_initial_claim():
    s = store()
    original = s.create_or_get(command())
    assert s.claim(original.command_id) is not None
    assert s.claim(original.command_id) is None


def test_next_scheduled_returns_oldest_scheduled_command():
    s = store()
    first = s.create_or_get(command("cmd-1", "req-1", datetime(2026, 9, 20, 1, tzinfo=timezone.utc)))
    second = s.create_or_get(command("cmd-2", "req-2", datetime(2026, 9, 20, 2, tzinfo=timezone.utc)))
    for value in (first, second):
        s.claim(value.command_id)
        s.record_scheduler_acknowledgement(value.command_id, SchedulerAcknowledgement(command_id=value.command_id, scheduling_id=f"schedule-{value.command_id}", status=SchedulerAcknowledgementStatus.ACCEPTED, observed_at=datetime(2026, 9, 20, 3, tzinfo=timezone.utc)))
    assert s.next_scheduled().command_id == "cmd-1"


def test_next_scheduled_uses_command_id_as_tiebreaker():
    s = store()
    first = s.create_or_get(command("cmd-a", "req-a"))
    second = s.create_or_get(command("cmd-b", "req-b"))
    for value in (first, second):
        s.claim(value.command_id)
        s.record_scheduler_acknowledgement(value.command_id, SchedulerAcknowledgement(command_id=value.command_id, scheduling_id=f"schedule-{value.command_id}", status=SchedulerAcknowledgementStatus.ACCEPTED, observed_at=datetime(2026, 9, 20, 3, tzinfo=timezone.utc)))
    assert s.next_scheduled().command_id == "cmd-a"


def test_next_scheduled_ignores_non_scheduled_commands():
    s = store()
    s.create_or_get(command())
    assert s.next_scheduled() is None
