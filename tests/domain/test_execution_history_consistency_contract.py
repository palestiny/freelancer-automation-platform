from datetime import datetime, timezone
import pytest

from app.domain.execution_history_consistency import (
    ExecutionHistoryConsistency,
    ExecutionHistoryConsistencyStatus,
)


def test_consistent_status_requires_positive_attempt_count():
    with pytest.raises(ValueError):
        ExecutionHistoryConsistency(
            request_id="req-1",
            idempotency_key="idem-1",
            attempt_count=0,
            status=ExecutionHistoryConsistencyStatus.CONSISTENT,
        )


def test_empty_history_requires_zero_attempt_count():
    with pytest.raises(ValueError):
        ExecutionHistoryConsistency(
            request_id="req-1",
            idempotency_key="idem-1",
            attempt_count=1,
            status=ExecutionHistoryConsistencyStatus.EMPTY_HISTORY,
        )


def test_empty_history_with_zero_attempts_is_valid():
    result = ExecutionHistoryConsistency(
        request_id="req-1",
        idempotency_key="idem-1",
        attempt_count=0,
        status=ExecutionHistoryConsistencyStatus.EMPTY_HISTORY,
    )
    assert result.attempt_count == 0


def test_mismatch_statuses_require_observed_history_count():
    for status in (
        ExecutionHistoryConsistencyStatus.IDENTITY_MISMATCH,
        ExecutionHistoryConsistencyStatus.LATEST_ATTEMPT_MISMATCH,
    ):
        with pytest.raises(ValueError):
            ExecutionHistoryConsistency(
                request_id="req-1",
                idempotency_key="idem-1",
                attempt_count=0,
                status=status,
            )
