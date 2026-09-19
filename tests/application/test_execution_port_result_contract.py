from datetime import datetime, timezone

import pytest

from app.domain.action_authorization import ActionClass, AutonomyLevel
from app.domain.authorized_execution_request import AuthorizedExecutionRequest, ExecutionRequestStatus
from app.domain.execution_outcome import ExecutionOutcomeStatus
from app.application.execution_port import (
    ExecutionPort,
    ProviderExecutionResult,
    dispatch_execution,
)


class RecordingPort(ExecutionPort):
    def __init__(self, result=None):
        self.received = []
        self.result = result

    def execute(self, request):
        self.received.append(request)
        return self.result or ProviderExecutionResult(
            request_id=request.request_id,
            idempotency_key=request.idempotency_key,
            status=ExecutionOutcomeStatus.SUCCEEDED,
            outcome_code="ok",
            observed_at=datetime(2026, 9, 19, tzinfo=timezone.utc),
        )


def _request(status=ExecutionRequestStatus.PREPARED):
    return AuthorizedExecutionRequest(
        request_id="req-1", idempotency_key="idem-1",
        action_class=ActionClass.REVERSIBLE_EXTERNAL,
        autonomy_level=AutonomyLevel.L3_EXECUTE_WITH_APPROVAL,
        policy_id="policy", policy_version="1", status=status,
    )


def test_provider_result_is_immutable_and_typed():
    result = ProviderExecutionResult(
        request_id="req-1",
        idempotency_key="idem-1",
        status=ExecutionOutcomeStatus.SUCCEEDED,
        outcome_code="ok",
        observed_at=datetime(2026, 9, 19, tzinfo=timezone.utc),
    )
    assert result.request_id == "req-1"
    with pytest.raises(AttributeError):
        result.request_id = "other"


def test_dispatch_rejects_provider_request_identity_mismatch():
    port = RecordingPort(
        ProviderExecutionResult(
            request_id="other",
            idempotency_key="idem-1",
            status=ExecutionOutcomeStatus.SUCCEEDED,
            outcome_code="ok",
            observed_at=datetime(2026, 9, 19, tzinfo=timezone.utc),
        )
    )
    with pytest.raises(ValueError, match="request_id"):
        dispatch_execution(port=port, request=_request())


def test_dispatch_rejects_provider_idempotency_mismatch():
    port = RecordingPort(
        ProviderExecutionResult(
            request_id="req-1",
            idempotency_key="other",
            status=ExecutionOutcomeStatus.SUCCEEDED,
            outcome_code="ok",
            observed_at=datetime(2026, 9, 19, tzinfo=timezone.utc),
        )
    )
    with pytest.raises(ValueError, match="idempotency"):
        dispatch_execution(port=port, request=_request())
