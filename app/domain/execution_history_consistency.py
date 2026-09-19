from dataclasses import dataclass
from enum import Enum

from .execution_attempt_history import ExecutionAttemptHistory
from .execution_outcome import ExecutionOutcome


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


def assess_execution_history_consistency(
    *,
    outcome: ExecutionOutcome,
    history: ExecutionAttemptHistory,
) -> ExecutionHistoryConsistency:
    if outcome.request_id != history.request_id or outcome.idempotency_key != history.idempotency_key:
        return ExecutionHistoryConsistency(
            outcome.request_id,
            outcome.idempotency_key,
            len(history.attempts),
            ExecutionHistoryConsistencyStatus.IDENTITY_MISMATCH,
        )

    if not history.attempts:
        return ExecutionHistoryConsistency(
            outcome.request_id,
            outcome.idempotency_key,
            0,
            ExecutionHistoryConsistencyStatus.EMPTY_HISTORY,
        )

    latest = history.latest_attempt
    assert latest is not None
    if (
        latest.status is not outcome.status
        or latest.outcome_code != outcome.outcome_code
        or latest.observed_at != outcome.observed_at
        or latest.external_reference != outcome.external_reference
    ):
        return ExecutionHistoryConsistency(
            outcome.request_id,
            outcome.idempotency_key,
            len(history.attempts),
            ExecutionHistoryConsistencyStatus.LATEST_ATTEMPT_MISMATCH,
        )

    return ExecutionHistoryConsistency(
        outcome.request_id,
        outcome.idempotency_key,
        len(history.attempts),
        ExecutionHistoryConsistencyStatus.CONSISTENT,
    )
