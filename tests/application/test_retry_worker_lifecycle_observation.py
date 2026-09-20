from datetime import datetime, timezone

import pytest

from app.application.retry_worker_lifecycle import (
    RetryWorkerLifecycleState,
    RetryWorkerLifecycleStopReason,
)
from app.application.retry_worker_lifecycle_observation import (
    RetryWorkerLifecycleObservation,
)


def test_lifecycle_observation_preserves_identity_state_and_reason():
    started = datetime(2026, 9, 20, 7, 0, tzinfo=timezone.utc)
    finished = datetime(2026, 9, 20, 7, 0, 1, tzinfo=timezone.utc)

    observation = RetryWorkerLifecycleObservation(
        runtime_id="runtime-1",
        started_at=started,
        finished_at=finished,
        final_state=RetryWorkerLifecycleState.STOPPED,
        stop_reason=RetryWorkerLifecycleStopReason.STOP_REQUESTED,
        transitions=(
            RetryWorkerLifecycleState.STOPPED,
            RetryWorkerLifecycleState.STARTING,
            RetryWorkerLifecycleState.RUNNING,
            RetryWorkerLifecycleState.STOPPING,
            RetryWorkerLifecycleState.STOPPED,
        ),
    )

    assert observation.runtime_id == "runtime-1"
    assert observation.duration_seconds == 1.0
    assert observation.transitions[-1] is RetryWorkerLifecycleState.STOPPED


@pytest.mark.parametrize(
    "kwargs",
    [
        {"runtime_id": ""},
        {"finished_at": datetime(2026, 9, 20, 6, 59, tzinfo=timezone.utc)},
    ],
)
def test_invalid_lifecycle_observation_is_rejected(kwargs):
    started = datetime(2026, 9, 20, 7, 0, tzinfo=timezone.utc)
    finished = datetime(2026, 9, 20, 7, 0, 1, tzinfo=timezone.utc)
    values = {
        "runtime_id": "runtime-1",
        "started_at": started,
        "finished_at": finished,
        "final_state": RetryWorkerLifecycleState.STOPPED,
        "stop_reason": RetryWorkerLifecycleStopReason.STOP_REQUESTED,
        "transitions": (
            RetryWorkerLifecycleState.STOPPED,
            RetryWorkerLifecycleState.STARTING,
            RetryWorkerLifecycleState.RUNNING,
            RetryWorkerLifecycleState.STOPPING,
            RetryWorkerLifecycleState.STOPPED,
        ),
    }
    values.update(kwargs)

    with pytest.raises(ValueError):
        RetryWorkerLifecycleObservation(**values)


def test_transitions_must_end_in_final_state():
    started = datetime(2026, 9, 20, 7, 0, tzinfo=timezone.utc)
    finished = datetime(2026, 9, 20, 7, 0, 1, tzinfo=timezone.utc)

    with pytest.raises(ValueError):
        RetryWorkerLifecycleObservation(
            runtime_id="runtime-1",
            started_at=started,
            finished_at=finished,
            final_state=RetryWorkerLifecycleState.STOPPED,
            stop_reason=RetryWorkerLifecycleStopReason.STOP_REQUESTED,
            transitions=(RetryWorkerLifecycleState.STARTING,),
        )
