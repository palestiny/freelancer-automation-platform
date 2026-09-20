from datetime import datetime, timezone

import pytest

from app.application.retry_worker_runtime import RetryWorkerRuntimeOutcome
from app.application.retry_runtime_observation import RetryRuntimeObservation


def test_observation_preserves_invocation_and_outcome():
    start = datetime(2026, 9, 20, 9, 0, tzinfo=timezone.utc)
    end = datetime(2026, 9, 20, 9, 0, 1, tzinfo=timezone.utc)
    observation = RetryRuntimeObservation(
        invocation_id="inv-1",
        started_at=start,
        finished_at=end,
        outcome=RetryWorkerRuntimeOutcome.DISPATCHED,
        command_id="cmd-1",
        dispatch_status="completed",
    )
    assert observation.duration_seconds == 1.0
    assert observation.command_id == "cmd-1"


def test_observation_requires_ordered_timestamps():
    start = datetime(2026, 9, 20, 9, 0, tzinfo=timezone.utc)
    with pytest.raises(ValueError):
        RetryRuntimeObservation(
            invocation_id="inv-1",
            started_at=start,
            finished_at=start,
            outcome=RetryWorkerRuntimeOutcome.IDLE,
        )


def test_observation_requires_invocation_id():
    start = datetime(2026, 9, 20, 9, 0, tzinfo=timezone.utc)
    end = datetime(2026, 9, 20, 9, 0, 1, tzinfo=timezone.utc)
    with pytest.raises(ValueError):
        RetryRuntimeObservation(
            invocation_id="",
            started_at=start,
            finished_at=end,
            outcome=RetryWorkerRuntimeOutcome.IDLE,
        )


def test_observation_keeps_failure_explicit():
    start = datetime(2026, 9, 20, 9, 0, tzinfo=timezone.utc)
    end = datetime(2026, 9, 20, 9, 0, 1, tzinfo=timezone.utc)
    observation = RetryRuntimeObservation(
        invocation_id="inv-1",
        started_at=start,
        finished_at=end,
        outcome=RetryWorkerRuntimeOutcome.FAILED,
        failure="work_source_failed",
    )
    assert observation.failure == "work_source_failed"
