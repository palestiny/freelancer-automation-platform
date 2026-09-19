from datetime import datetime, timezone
import pytest
from app.application.execution_port import ProviderExecutionResult
from app.domain.execution_outcome import ExecutionOutcomeStatus

def test_provider_result_rejects_naive_timestamp():
    with pytest.raises(ValueError, match="timezone-aware"):
        ProviderExecutionResult(
            request_id="req-1",
            idempotency_key="idem-1",
            status=ExecutionOutcomeStatus.SUCCEEDED,
            outcome_code="ok",
            observed_at=datetime(2026, 9, 19),
        )

def test_provider_result_accepts_timezone_aware_timestamp():
    result = ProviderExecutionResult(
        request_id="req-1",
        idempotency_key="idem-1",
        status=ExecutionOutcomeStatus.SUCCEEDED,
        outcome_code="ok",
        observed_at=datetime(2026, 9, 19, tzinfo=timezone.utc),
    )
    assert result.observed_at.tzinfo is timezone.utc
