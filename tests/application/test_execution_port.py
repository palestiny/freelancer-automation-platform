from datetime import datetime, timezone

import pytest

from app.domain.action_authorization import ActionClass, AutonomyLevel
from app.domain.authorized_execution_request import AuthorizedExecutionRequest, ExecutionRequestStatus
from app.domain.execution_outcome import ExecutionOutcomeStatus
from app.application.execution_port import ExecutionPort, dispatch_execution


class RecordingPort(ExecutionPort):
    def __init__(self):
        self.received = []

    def execute(self, request):
        self.received.append(request)
        return {
            "request_id": request.request_id,
            "idempotency_key": request.idempotency_key,
            "status": ExecutionOutcomeStatus.SUCCEEDED,
            "outcome_code": "ok",
            "observed_at": datetime(2026, 9, 19, tzinfo=timezone.utc),
        }


def _request(status=ExecutionRequestStatus.PREPARED):
    return AuthorizedExecutionRequest(
        request_id="req-1", idempotency_key="idem-1",
        action_class=ActionClass.REVERSIBLE_EXTERNAL,
        autonomy_level=AutonomyLevel.L3_EXECUTE_WITH_APPROVAL,
        policy_id="policy", policy_version="1", status=status,
    )


def test_dispatch_requires_prepared_request():
    port = RecordingPort()
    with pytest.raises(ValueError, match="prepared"):
        dispatch_execution(port=port, request=_request(ExecutionRequestStatus.REJECTED))
    assert port.received == []


def test_dispatch_returns_provider_independent_execution_outcome():
    port = RecordingPort()
    outcome = dispatch_execution(port=port, request=_request())
    assert outcome.request_id == "req-1"
    assert outcome.idempotency_key == "idem-1"
    assert outcome.status is ExecutionOutcomeStatus.SUCCEEDED
    assert port.received == [_request()]


def test_dispatch_preserves_idempotency_identity():
    port = RecordingPort()
    first = dispatch_execution(port=port, request=_request())
    second = dispatch_execution(port=port, request=_request())
    assert first.idempotency_key == second.idempotency_key == "idem-1"
