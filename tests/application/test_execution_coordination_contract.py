from datetime import datetime, timezone
import pytest

from app.application.execution_coordinator import ExecutionCoordinationResult, coordinate_execution
from app.application.execution_port import ExecutionPort, ProviderExecutionResult
from app.domain.action_authorization import ActionClass, AutonomyLevel
from app.domain.authorized_execution_request import AuthorizedExecutionRequest, ExecutionRequestStatus
from app.domain.execution_outcome import ExecutionOutcomeStatus
from app.domain.execution_outcome_policy import (
    ExecutionOutcomeAssessment,
    ExecutionOutcomeAssessmentStatus,
    ExecutionOutcomePolicy,
)


class FakeExecutionPort(ExecutionPort):
    def __init__(self):
        self.received = None

    def execute(self, request):
        self.received = request
        return ProviderExecutionResult(
            request_id=request.request_id,
            idempotency_key=request.idempotency_key,
            status=ExecutionOutcomeStatus.SUCCEEDED,
            outcome_code="ok",
            observed_at=datetime(2026, 9, 19, tzinfo=timezone.utc),
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


def test_coordination_result_exposes_typed_assessment():
    port = FakeExecutionPort()
    result = coordinate_execution(
        port=port,
        request=_request(),
        policy=ExecutionOutcomePolicy(),
        attempt_count=1,
    )
    assert isinstance(result, ExecutionCoordinationResult)
    assert isinstance(result.policy_assessment, ExecutionOutcomeAssessment)
    assert result.policy_assessment.status is ExecutionOutcomeAssessmentStatus.ACCEPTED


@pytest.mark.parametrize("attempt_count", [0, -1, True, 1.5])
def test_invalid_attempt_count_is_rejected_before_provider_call(attempt_count):
    port = FakeExecutionPort()
    with pytest.raises((TypeError, ValueError)):
        coordinate_execution(
            port=port,
            request=_request(),
            policy=ExecutionOutcomePolicy(),
            attempt_count=attempt_count,
        )
    assert port.received is None
