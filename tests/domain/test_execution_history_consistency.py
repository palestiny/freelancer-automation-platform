from datetime import datetime, timezone

from app.domain.execution_attempt_history import ExecutionAttempt, ExecutionAttemptHistory
from app.domain.execution_outcome import ExecutionOutcome, ExecutionOutcomeStatus
from app.domain.execution_history_consistency import (
    ExecutionHistoryConsistencyStatus,
    assess_execution_history_consistency,
)


T1 = datetime(2026, 9, 19, 18, 0, tzinfo=timezone.utc)
T2 = datetime(2026, 9, 19, 18, 5, tzinfo=timezone.utc)


def _attempt(number, status=ExecutionOutcomeStatus.FAILED, code="timeout", when=T1):
    return ExecutionAttempt("r1", "idem-1", number, status, code, when, "ext-1")


def _history():
    return ExecutionAttemptHistory(
        "r1", "idem-1", (_attempt(1), _attempt(2, ExecutionOutcomeStatus.SUCCEEDED, "ok", T2))
    )


def _outcome():
    return ExecutionOutcome("r1", "idem-1", ExecutionOutcomeStatus.SUCCEEDED, "ok", T2, "ext-1")


def test_consistent_outcome_and_history():
    result = assess_execution_history_consistency(outcome=_outcome(), history=_history())
    assert result.status is ExecutionHistoryConsistencyStatus.CONSISTENT
    assert result.attempt_count == 2


def test_identity_mismatch_is_explicit():
    outcome = ExecutionOutcome("other", "idem-1", ExecutionOutcomeStatus.SUCCEEDED, "ok", T2, "ext-1")
    result = assess_execution_history_consistency(outcome=outcome, history=_history())
    assert result.status is ExecutionHistoryConsistencyStatus.IDENTITY_MISMATCH


def test_history_length_is_reported_without_inference():
    history = ExecutionAttemptHistory("r1", "idem-1", (_attempt(1),))
    result = assess_execution_history_consistency(outcome=_outcome(), history=history)
    assert result.status is ExecutionHistoryConsistencyStatus.LATEST_ATTEMPT_MISMATCH
    assert result.attempt_count == 1


def test_latest_attempt_mismatch_is_explicit():
    history = ExecutionAttemptHistory(
        "r1", "idem-1", (_attempt(1), _attempt(2, ExecutionOutcomeStatus.FAILED, "timeout", T2))
    )
    result = assess_execution_history_consistency(outcome=_outcome(), history=history)
    assert result.status is ExecutionHistoryConsistencyStatus.LATEST_ATTEMPT_MISMATCH


def test_empty_history_is_explicit():
    history = ExecutionAttemptHistory("r1", "idem-1")
    result = assess_execution_history_consistency(outcome=_outcome(), history=history)
    assert result.status is ExecutionHistoryConsistencyStatus.EMPTY_HISTORY
