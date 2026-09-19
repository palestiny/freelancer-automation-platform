from datetime import datetime, timezone

import pytest

from app.application.execution_coordinator import coordinate_execution_with_history
from app.application.execution_port import ExecutionPort, ProviderExecutionResult
from app.domain.action_authorization import ActionClass, AutonomyLevel
from app.domain.authorized_execution_request import AuthorizedExecutionRequest, ExecutionRequestStatus
from app.domain.execution_attempt_history import ExecutionAttempt, ExecutionAttemptHistory
from app.domain.execution_outcome import ExecutionOutcomeStatus
from app.domain.execution_outcome_policy import ExecutionOutcomeAssessmentStatus, ExecutionOutcomePolicy


class FakePort(ExecutionPort):
    def __init__(self, result):
        self.result = result
        self.received = None

    def execute(self, request):
        self.received = request
        return self.result


def request():
    return AuthorizedExecutionRequest(
        request_id="req-1", idempotency_key="idem-1",
        action_class=ActionClass.REVERSIBLE_EXTERNAL,
        autonomy_level=AutonomyLevel.L3_EXECUTE_WITH_APPROVAL,
        policy_id="p1", policy_version="1", status=ExecutionRequestStatus.PREPARED,
    )


def result(status=ExecutionOutcomeStatus.SUCCEEDED, code="ok", second=False):
    return ProviderExecutionResult(
        request_id="req-1", idempotency_key="idem-1", status=status,
        outcome_code=code,
        observed_at=datetime(2026, 9, 19, 12 if second else 10, tzinfo=timezone.utc),
    )


def test_empty_history_creates_first_attempt_and_uses_history_count():
    port = FakePort(result())
    coordinated = coordinate_execution_with_history(
        port=port,
        request=request(),
        history=ExecutionAttemptHistory(request_id="req-1", idempotency_key="idem-1"),
        policy=ExecutionOutcomePolicy(maximum_attempts=3, retryable_outcome_codes=("timeout",)),
    )

    assert coordinated.history.latest_attempt is not None
    assert coordinated.history.latest_attempt.attempt_number == 1
    assert coordinated.policy_assessment.attempt_count == 1
    assert coordinated.recovery_handoff.mode.value == "none"


def test_existing_history_increments_attempt_number_without_caller_count():
    prior = ExecutionAttempt(
        request_id="req-1", idempotency_key="idem-1", attempt_number=1,
        status=ExecutionOutcomeStatus.FAILED, outcome_code="timeout",
        observed_at=datetime(2026, 9, 18, tzinfo=timezone.utc),
    )
    port = FakePort(result(ExecutionOutcomeStatus.FAILED, "timeout", second=True))
    coordinated = coordinate_execution_with_history(
        port=port,
        request=request(),
        history=ExecutionAttemptHistory(
            request_id="req-1", idempotency_key="idem-1", attempts=(prior,)
        ),
        policy=ExecutionOutcomePolicy(maximum_attempts=3, retryable_outcome_codes=("timeout",)),
    )

    assert coordinated.history.latest_attempt.attempt_number == 2
    assert coordinated.policy_assessment.status is ExecutionOutcomeAssessmentStatus.RETRY_ELIGIBLE


def test_mismatched_history_identity_is_rejected_before_provider_call():
    history = ExecutionAttemptHistory(request_id="other", idempotency_key="idem-1")
    port = FakePort(result())
    with pytest.raises(ValueError):
        coordinate_execution_with_history(
            port=port, request=request(), history=history,
            policy=ExecutionOutcomePolicy(),
        )
    assert port.received is None
