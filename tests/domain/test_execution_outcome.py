from datetime import datetime, timezone

import pytest

from app.domain.action_authorization import ActionClass, AutonomyLevel
from app.domain.authorized_execution_request import (
    AuthorizedExecutionRequest,
    ExecutionRequestStatus,
)
from app.domain.execution_outcome import (
    ExecutionOutcomeStatus,
    record_execution_outcome,
)


def _request():
    return AuthorizedExecutionRequest(
        request_id="req-1",
        idempotency_key="idem-1",
        action_class=ActionClass.REVERSIBLE_EXTERNAL,
        autonomy_level=AutonomyLevel.L3_EXECUTE_WITH_APPROVAL,
        policy_id="policy-1",
        policy_version="1",
        status=ExecutionRequestStatus.PREPARED,
    )


def test_successful_outcome_preserves_request_identity():
    result = record_execution_outcome(
        request=_request(),
        status=ExecutionOutcomeStatus.SUCCEEDED,
        outcome_code="provider_success",
        observed_at=datetime(2026, 9, 19, tzinfo=timezone.utc),
        external_reference="ext-1",
    )
    assert result.request_id == "req-1"
    assert result.idempotency_key == "idem-1"
    assert result.external_reference == "ext-1"


def test_unknown_outcome_remains_unknown():
    result = record_execution_outcome(
        request=_request(),
        status=ExecutionOutcomeStatus.UNKNOWN,
        outcome_code="provider_timeout",
        observed_at=datetime(2026, 9, 19, tzinfo=timezone.utc),
    )
    assert result.status is ExecutionOutcomeStatus.UNKNOWN


def test_rejected_request_cannot_produce_execution_outcome():
    request = _request().__class__(
        request_id="req-2",
        idempotency_key="idem-2",
        action_class=ActionClass.REVERSIBLE_EXTERNAL,
        autonomy_level=AutonomyLevel.L2_PREPARE,
        policy_id="policy-1",
        policy_version="1",
        status=ExecutionRequestStatus.REJECTED,
    )
    with pytest.raises(ValueError, match="prepared"):
        record_execution_outcome(
            request=request,
            status=ExecutionOutcomeStatus.FAILED,
            outcome_code="not_executed",
            observed_at=datetime(2026, 9, 19, tzinfo=timezone.utc),
        )


def test_empty_outcome_code_is_rejected():
    with pytest.raises(ValueError, match="outcome_code"):
        record_execution_outcome(
            request=_request(),
            status=ExecutionOutcomeStatus.FAILED,
            outcome_code="",
            observed_at=datetime(2026, 9, 19, tzinfo=timezone.utc),
        )


def test_outcome_reference_must_not_be_empty():
    with pytest.raises(ValueError, match="external_reference"):
        record_execution_outcome(
            request=_request(),
            status=ExecutionOutcomeStatus.SUCCEEDED,
            outcome_code="ok",
            observed_at=datetime(2026, 9, 19, tzinfo=timezone.utc),
            external_reference="",
        )


def test_naive_outcome_timestamp_is_rejected():
    with pytest.raises(ValueError, match="timezone-aware"):
        record_execution_outcome(request=_request(), status=ExecutionOutcomeStatus.SUCCEEDED, outcome_code="ok", observed_at=datetime(2026, 9, 19))


def test_outcome_cannot_precede_prepared_at():
    request = _request().__class__(request_id="req-3", idempotency_key="idem-3", action_class=ActionClass.REVERSIBLE_EXTERNAL, autonomy_level=AutonomyLevel.L3_EXECUTE_WITH_APPROVAL, policy_id="policy-1", policy_version="1", status=ExecutionRequestStatus.PREPARED, prepared_at=datetime(2026, 9, 19, 12, tzinfo=timezone.utc))
    with pytest.raises(ValueError, match="precede prepared_at"):
        record_execution_outcome(request=request, status=ExecutionOutcomeStatus.FAILED, outcome_code="provider_failed", observed_at=datetime(2026, 9, 19, 11, 59, tzinfo=timezone.utc))


def test_outcome_at_prepared_time_is_valid():
    request = _request().__class__(request_id="req-4", idempotency_key="idem-4", action_class=ActionClass.REVERSIBLE_EXTERNAL, autonomy_level=AutonomyLevel.L3_EXECUTE_WITH_APPROVAL, policy_id="policy-1", policy_version="1", status=ExecutionRequestStatus.PREPARED, prepared_at=datetime(2026, 9, 19, 12, tzinfo=timezone.utc))
    result = record_execution_outcome(request=request, status=ExecutionOutcomeStatus.UNKNOWN, outcome_code="provider_timeout", observed_at=datetime(2026, 9, 19, 12, tzinfo=timezone.utc))
    assert result.observed_at == request.prepared_at


def test_record_execution_outcome_rejects_naive_observed_at_before_temporal_comparison():
    from datetime import datetime
    import pytest
    request = _request()
    with pytest.raises(ValueError, match="observed_at must be timezone-aware"):
        record_execution_outcome(request=request, status=ExecutionOutcomeStatus.SUCCEEDED, outcome_code="ok", observed_at=datetime(2026, 1, 1))


def test_record_execution_outcome_rejects_invalid_status_at_boundary():
    from datetime import datetime, timezone
    import pytest
    request = _request()
    with pytest.raises(TypeError, match="status must be an ExecutionOutcomeStatus"):
        record_execution_outcome(request=request, status="succeeded", outcome_code="ok", observed_at=datetime(2026, 1, 1, tzinfo=timezone.utc))


def test_execution_outcome_rejects_non_string_external_reference():
    import pytest
    request = _request()
    with pytest.raises(TypeError, match="external_reference must be a string or None"):
        record_execution_outcome(request=request, status=ExecutionOutcomeStatus.SUCCEEDED, outcome_code="ok", observed_at=datetime(2026, 1, 1, tzinfo=timezone.utc), external_reference=123)


def test_execution_outcome_rejects_empty_external_reference():
    import pytest
    request = _request()
    with pytest.raises(ValueError, match="external_reference cannot be empty"):
        record_execution_outcome(request=request, status=ExecutionOutcomeStatus.SUCCEEDED, outcome_code="ok", observed_at=datetime(2026, 1, 1, tzinfo=timezone.utc), external_reference=" ")
