from dataclasses import dataclass
from datetime import datetime

from app.application.retry_worker_lifecycle import (
    RetryWorkerLifecycleState,
    RetryWorkerLifecycleStopReason,
)


@dataclass(frozen=True)
class RetryWorkerLifecycleObservation:
    runtime_id: str
    started_at: datetime
    finished_at: datetime
    final_state: RetryWorkerLifecycleState
    stop_reason: RetryWorkerLifecycleStopReason
    transitions: tuple[RetryWorkerLifecycleState, ...]

    def __post_init__(self) -> None:
        if not self.runtime_id.strip():
            raise ValueError("runtime_id cannot be empty")
        if self.finished_at <= self.started_at:
            raise ValueError("finished_at must be after started_at")
        if not self.transitions:
            raise ValueError("transitions cannot be empty")
        if self.transitions[-1] is not self.final_state:
            raise ValueError("transitions must end in final_state")

    @property
    def duration_seconds(self) -> float:
        return (self.finished_at - self.started_at).total_seconds()
