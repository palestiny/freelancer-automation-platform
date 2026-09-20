from dataclasses import dataclass
from datetime import datetime

from app.application.retry_worker_runtime import RetryWorkerRuntimeOutcome


@dataclass(frozen=True)
class RetryRuntimeObservation:
    invocation_id: str
    started_at: datetime
    finished_at: datetime
    outcome: RetryWorkerRuntimeOutcome
    command_id: str | None = None
    dispatch_status: str | None = None
    failure: str | None = None

    def __post_init__(self) -> None:
        if not self.invocation_id.strip():
            raise ValueError("invocation_id cannot be empty")
        if self.finished_at <= self.started_at:
            raise ValueError("finished_at must be after started_at")
        if self.command_id is not None and not self.command_id.strip():
            raise ValueError("command_id cannot be empty")
        if self.dispatch_status is not None and not self.dispatch_status.strip():
            raise ValueError("dispatch_status cannot be empty")
        if self.failure is not None and not self.failure.strip():
            raise ValueError("failure cannot be empty")

    @property
    def duration_seconds(self) -> float:
        return (self.finished_at - self.started_at).total_seconds()
