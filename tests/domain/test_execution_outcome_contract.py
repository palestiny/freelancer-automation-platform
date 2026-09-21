from datetime import datetime, timezone

import pytest

from app.domain.execution_outcome import ExecutionOutcome, ExecutionOutcomeStatus


def _valid():
    return ExecutionOutcome(
        request_id="request-1",
        idempotency_key="idem-1",
        status=ExecutionOutcomeStatus.SUCCEEDED,
        outcome_code="completed",
        observed_at=datetime(2026, 9, 21, tzinfo=timezone.utc),
    )


def test_valid_execution_outcome_is_accepted():
    assert _valid().status is ExecutionOutcomeStatus.SUCCEEDED


def test_invalid_status_type_is_rejected():
    with pytest.raises(TypeError, match="status"):
        ExecutionOutcome(
            request_id="request-1",
            idempotency_key="idem-1",
            status="succeeded",
            outcome_code="completed",
            observed_at=datetime(2026, 9, 21, tzinfo=timezone.utc),
        )


def test_invalid_observed_at_type_is_rejected():
    with pytest.raises(TypeError, match="observed_at"):
        ExecutionOutcome(
            request_id="request-1",
            idempotency_key="idem-1",
            status=ExecutionOutcomeStatus.SUCCEEDED,
            outcome_code="completed",
            observed_at="2026-09-21T00:00:00+00:00",
        )


def test_naive_observed_at_remains_rejected():
    with pytest.raises(ValueError, match="timezone-aware"):
        ExecutionOutcome(
            request_id="request-1",
            idempotency_key="idem-1",
            status=ExecutionOutcomeStatus.SUCCEEDED,
            outcome_code="completed",
            observed_at=datetime(2026, 9, 21),
        )


def test_invalid_external_reference_remains_rejected():
    with pytest.raises(ValueError, match="external_reference"):
        ExecutionOutcome(
            request_id="request-1",
            idempotency_key="idem-1",
            status=ExecutionOutcomeStatus.SUCCEEDED,
            outcome_code="completed",
            observed_at=datetime(2026, 9, 21, tzinfo=timezone.utc),
            external_reference=" ",
        )
