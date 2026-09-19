from dataclasses import dataclass
from enum import Enum


class ExecutionHistoryConsistencyStatus(str, Enum):
    CONSISTENT = "consistent"
    IDENTITY_MISMATCH = "identity_mismatch"
    LATEST_ATTEMPT_MISMATCH = "latest_attempt_mismatch"
    EMPTY_HISTORY = "empty_history"


@dataclass(frozen=True)
class ExecutionHistoryConsistency:
    request_id: str
    idempotency_key: str
    attempt_count: int
    status: ExecutionHistoryConsistencyStatus

    def __post_init__(self) -> None:
        if not self.request_id.strip() or not self.idempotency_key.strip():
            raise ValueError("request_id and idempotency_key cannot be empty")
        if not isinstance(self.attempt_count, int) or isinstance(self.attempt_count, bool):
            raise TypeError("attempt_count must be an integer")
        if self.attempt_count < 0:
            raise ValueError("attempt_count cannot be negative")

        if self.status is ExecutionHistoryConsistencyStatus.CONSISTENT:
            if self.attempt_count <= 0:
                raise ValueError("consistent history requires at least one attempt")
        elif self.status is ExecutionHistoryConsistencyStatus.EMPTY_HISTORY:
            if self.attempt_count != 0:
                raise ValueError("empty history requires zero attempts")
        elif self.attempt_count <= 0:
            raise ValueError("mismatch status requires at least one observed attempt")


def assess_execution_history_consistency(*, outcome, history):
    if outcome.request_id != history.request_id or outcome.idempotency_key != history.idempotency_key:
        return ExecutionHistoryConsistency(outcome.request_id, outcome.idempotency_key, len(history.attempts), ExecutionHistoryConsistencyStatus.IDENTITY_MISMATCH)
    if not history.attempts:
        return ExecutionHistoryConsistency(outcome.request_id, outcome.idempotency_key, 0, ExecutionHistoryConsistencyStatus.EMPTY_HISTORY)
    latest = history.latest_attempt
    assert latest is not None
    if latest.status is not outcome.status or latest.outcome_code != outcome.outcome_code or latest.observed_at != outcome.observed_at or latest.external_reference != outcome.external_reference:
        return ExecutionHistoryConsistency(outcome.request_id, outcome.idempotency_key, len(history.attempts), ExecutionHistoryConsistencyStatus.LATEST_ATTEMPT_MISMATCH)
    return ExecutionHistoryConsistency(outcome.request_id, outcome.idempotency_key, len(history.attempts), ExecutionHistoryConsistencyStatus.CONSISTENT)
