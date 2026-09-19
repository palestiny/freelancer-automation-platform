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


def command(command_id="cmd-1"):
    return RetryCommand(
        command_id=command_id,
        request_id="req-1",
        idempotency_key="idem-1",
        attempt_number=1,
        action=RetryCommandAction.RETRY,
        authorization_policy_id="policy",
        authorization_policy_version="v1",
        autonomy_bound="L3",
        created_at=datetime(2026, 9, 20, tzinfo=timezone.utc),
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


def test_duplicate_logical_command_returns_existing_record():
    s = store()
    original = command()
    assert s.create_or_get(original) == original

    duplicate = command("cmd-2")
    assert s.create_or_get(duplicate) == original


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
