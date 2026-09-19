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
