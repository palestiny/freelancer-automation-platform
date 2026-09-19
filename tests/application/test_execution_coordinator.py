from datetime import datetime, timezone

import pytest

from app.application.execution_port import ExecutionPort, ProviderExecutionResult
from app.application.execution_coordinator import coordinate_execution
from app.domain.authorized_execution_request import AuthorizedExecutionRequest, ExecutionRequestStatus
from app.domain.action_authorization import ActionClass, AutonomyLevel
from app.domain.execution_outcome import ExecutionOutcomeStatus
from app.domain.execution_outcome_policy import ExecutionOutcomeAssessmentStatus
from app.domain.execution_outcome_policy import ExecutionOutcomePolicy


class FakeExecutionPort(ExecutionPort):
    def __init__(self, result: ProviderExecutionResult):
        self.result = result
        self.received = None

    def execute(self, request):
        self.received = request
        return self.result


def _request(status=ExecutionRequestStatus.PREPARED):
    return AuthorizedExecutionRequest(
        request_id="req-1",
        idempotency_key="idem-1",
        action_class=ActionClass.REVERSIBLE_EXTERNAL,
        autonomy_level=AutonomyLevel.L3_EXECUTE_WITH_APPROVAL,
        policy_id="policy-1",
        policy_version="1",
        status=status,
    )


def _result(status=ExecutionOutcomeStatus.SUCCEEDED, code="ok"):
    return ProviderExecutionResult(
        request_id="req-1",
        idempotency_key="idem-1",
        status=status,
        outcome_code=code,
        observed_at=datetime(2026, 9, 19, tzinfo=timezone.utc),
    )


def test_coordinator_dispatches_and_propagates_policy_and_recovery():
    port = FakeExecutionPort(_result())
    result = coordinate_execution(
        port=port,
        request=_request(),
        policy=ExecutionOutcomePolicy(maximum_attempts=3, retryable_outcome_codes=("timeout",)),
        attempt_count=1,
    )

    assert port.received == _request()
    assert result.outcome.request_id == "req-1"
    assert result.policy_assessment.outcome_status is ExecutionOutcomeStatus.SUCCEEDED
    assert result.recovery_handoff.mode.value == "none"


def test_retryable_failure_reaches_recovery_handoff():
    port = FakeExecutionPort(
        _result(ExecutionOutcomeStatus.FAILED, "timeout")
    )
    result = coordinate_execution(
        port=port,
        request=_request(),
        policy=ExecutionOutcomePolicy(maximum_attempts=3, retryable_outcome_codes=("timeout",)),
        attempt_count=1,
    )

    assert result.policy_assessment.status is ExecutionOutcomeAssessmentStatus.RETRY_ELIGIBLE
    assert result.recovery_handoff.mode.value == "retry"


def test_non_prepared_request_is_rejected_before_provider_call():
    port = FakeExecutionPort(_result())
    with pytest.raises(ValueError):
        coordinate_execution(
            port=port,
            request=_request(ExecutionRequestStatus.REJECTED),
            policy=ExecutionOutcomePolicy(maximum_attempts=3, retryable_outcome_codes=("timeout",)),
            attempt_count=1,
        )
    assert port.received is None
