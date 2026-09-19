from app.domain.execution_outcome import ExecutionOutcomeStatus
from app.domain.execution_outcome_policy import (
    ExecutionOutcomeAssessment,
    ExecutionOutcomeAssessmentStatus,
)
from app.domain.execution_recovery import (
    ExecutionRecoveryMode,
    create_execution_recovery_handoff,
)


def _assessment(status):
    return ExecutionOutcomeAssessment(
        request_id="req-1",
        idempotency_key="idem-1",
        outcome_status=ExecutionOutcomeStatus.FAILED,
        outcome_code="timeout",
        attempt_count=2,
        status=status,
    )


def test_retry_eligible_creates_retry_handoff_without_execution():
    result = create_execution_recovery_handoff(
        assessment=_assessment(ExecutionOutcomeAssessmentStatus.RETRY_ELIGIBLE)
    )
    assert result.mode is ExecutionRecoveryMode.RETRY
    assert result.request_id == "req-1"
    assert result.idempotency_key == "idem-1"
    assert result.attempt_count == 2


def test_unknown_outcome_requires_manual_review():
    result = create_execution_recovery_handoff(
        assessment=_assessment(ExecutionOutcomeAssessmentStatus.MANUAL_REVIEW_REQUIRED)
    )
    assert result.mode is ExecutionRecoveryMode.MANUAL_REVIEW


def test_terminal_failure_does_not_create_retry():
    result = create_execution_recovery_handoff(
        assessment=_assessment(ExecutionOutcomeAssessmentStatus.TERMINAL_FAILURE)
    )
    assert result.mode is ExecutionRecoveryMode.NONE


def test_accepted_outcome_requires_no_recovery():
    result = create_execution_recovery_handoff(
        assessment=_assessment(ExecutionOutcomeAssessmentStatus.ACCEPTED)
    )
    assert result.mode is ExecutionRecoveryMode.NONE
