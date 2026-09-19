from dataclasses import dataclass
from datetime import datetime

from .execution_outcome import ExecutionOutcomeStatus


@dataclass(frozen=True)
class ExecutionAttempt:
    request_id: str
    idempotency_key: str
    attempt_number: int
    status: ExecutionOutcomeStatus
    outcome_code: str
    observed_at: datetime
    external_reference: str | None = None

    def __post_init__(self) -> None:
        for name in ("request_id", "idempotency_key", "outcome_code"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} cannot be empty")
        if not isinstance(self.attempt_number, int) or isinstance(self.attempt_number, bool):
            raise TypeError("attempt_number must be an integer")
        if self.attempt_number <= 0:
            raise ValueError("attempt_number must be greater than zero")
        if not isinstance(self.status, ExecutionOutcomeStatus):
            raise TypeError("status must be an ExecutionOutcomeStatus")
        if not isinstance(self.observed_at, datetime):
            raise TypeError("observed_at must be a datetime")
        if self.observed_at.tzinfo is None or self.observed_at.utcoffset() is None:
            raise ValueError("observed_at must be timezone-aware")
        if self.external_reference is not None and not self.external_reference.strip():
            raise ValueError("external_reference cannot be empty")


@dataclass(frozen=True)
class ExecutionAttemptHistory:
    request_id: str
    idempotency_key: str
    attempts: tuple[ExecutionAttempt, ...] = ()

    def __post_init__(self) -> None:
        if not self.request_id.strip() or not self.idempotency_key.strip():
            raise ValueError("request_id and idempotency_key cannot be empty")
        if any(
            attempt.request_id != self.request_id
            or attempt.idempotency_key != self.idempotency_key
            for attempt in self.attempts
        ):
            raise ValueError("all attempts must match history identity")
        numbers = tuple(attempt.attempt_number for attempt in self.attempts)
        if len(set(numbers)) != len(numbers):
            raise ValueError("attempt numbers must be unique")

    @property
    def ordered_attempts(self) -> tuple[ExecutionAttempt, ...]:
        return tuple(
            sorted(self.attempts, key=lambda attempt: attempt.attempt_number)
        )

    @property
    def latest_attempt(self) -> ExecutionAttempt | None:
        if not self.attempts:
            return None
        return self.ordered_attempts[-1]

    def append(self, attempt: ExecutionAttempt) -> "ExecutionAttemptHistory":
        if attempt.request_id != self.request_id or attempt.idempotency_key != self.idempotency_key:
            raise ValueError("attempt identity does not match history")
        if attempt.attempt_number in {a.attempt_number for a in self.attempts}:
            raise ValueError("attempt number already exists")
        return ExecutionAttemptHistory(
            request_id=self.request_id,
            idempotency_key=self.idempotency_key,
            attempts=self.attempts + (attempt,),
        )
