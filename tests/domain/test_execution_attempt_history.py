from datetime import datetime, timezone

import pytest

from app.domain.execution_attempt_history import ExecutionAttempt, ExecutionAttemptHistory
from app.domain.execution_outcome import ExecutionOutcomeStatus


def _attempt(number=1, request_id="req-1", key="idem-1", status=ExecutionOutcomeStatus.FAILED):
    return ExecutionAttempt(
        request_id=request_id,
        idempotency_key=key,
        attempt_number=number,
        status=status,
        outcome_code="timeout",
        observed_at=datetime(2026, 9, 19, 10, number, tzinfo=timezone.utc),
    )


def test_history_preserves_attempt_lineage_and_order():
    history = ExecutionAttemptHistory(
        request_id="req-1",
        idempotency_key="idem-1",
        attempts=(_attempt(2), _attempt(1)),
    )
    assert tuple(a.attempt_number for a in history.ordered_attempts) == (1, 2)
    assert history.latest_attempt is history.ordered_attempts[-1]


def test_append_rejects_duplicate_attempt_number():
    history = ExecutionAttemptHistory("req-1", "idem-1", (_attempt(1),))
    with pytest.raises(ValueError):
        history.append(_attempt(1))


def test_history_rejects_mixed_identity():
    with pytest.raises(ValueError):
        ExecutionAttemptHistory("req-1", "idem-1", (_attempt(1), _attempt(2, key="other")))


def test_attempt_requires_positive_integer_number():
    with pytest.raises(ValueError):
        _attempt(0)
    with pytest.raises(TypeError):
        ExecutionAttempt("req-1", "idem-1", True, ExecutionOutcomeStatus.FAILED, "x", datetime.now(timezone.utc))


def test_attempt_requires_timezone_aware_timestamp():
    with pytest.raises(ValueError):
        ExecutionAttempt("req-1", "idem-1", 1, ExecutionOutcomeStatus.FAILED, "x", datetime(2026, 9, 19))


def test_append_rejects_mixed_identity():
    history = ExecutionAttemptHistory("req-1", "idem-1")
    with pytest.raises(ValueError):
        history.append(_attempt(1, request_id="other"))
