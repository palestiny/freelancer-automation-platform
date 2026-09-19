from datetime import datetime, timezone

from app.domain.authorized_execution_request import (
    AuthorizedExecutionRequest,
    ExecutionRequestStatus,
)
from app.domain.action_authorization import ActionClass, AutonomyLevel
from app.domain.execution_outcome import ExecutionOutcome, ExecutionOutcomeStatus
from app.domain.execution_outcome_policy import (
    ExecutionOutcomeAssessmentStatus,
    ExecutionOutcomePolicy,
    assess_execution_outcome,
)


def _outcome(status, code="temporary_error"):
    return ExecutionOutcome(
        request_id="req-1",
        idempotency_key="idem-1",
        status=status,
        outcome_code=code,
        observed_at=datetime.now(timezone.utc),
    )


def test_success_is_accepted():
    result = assess_execution_outcome(
        outcome=_outcome(ExecutionOutcomeStatus.SUCCEEDED, "ok"),
        attempt_count=1,
        policy=ExecutionOutcomePolicy(retryable_outcome_codes=("temporary_error",), maximum_attempts=3),
    )
    assert result.status is ExecutionOutcomeAssessmentStatus.ACCEPTED


def test_retryable_failure_is_retry_eligible():
    result = assess_execution_outcome(
        outcome=_outcome(ExecutionOutcomeStatus.FAILED),
        attempt_count=1,
        policy=ExecutionOutcomePolicy(retryable_outcome_codes=("temporary_error",), maximum_attempts=3),
    )
    assert result.status is ExecutionOutcomeAssessmentStatus.RETRY_ELIGIBLE


def test_max_attempts_make_failure_terminal():
    result = assess_execution_outcome(
        outcome=_outcome(ExecutionOutcomeStatus.FAILED),
        attempt_count=3,
        policy=ExecutionOutcomePolicy(retryable_outcome_codes=("temporary_error",), maximum_attempts=3),
    )
    assert result.status is ExecutionOutcomeAssessmentStatus.TERMINAL_FAILURE


def test_unknown_requires_manual_review():
    result = assess_execution_outcome(
        outcome=_outcome(ExecutionOutcomeStatus.UNKNOWN, "provider_timeout"),
        attempt_count=1,
        policy=ExecutionOutcomePolicy(retryable_outcome_codes=("temporary_error",), maximum_attempts=3),
    )
    assert result.status is ExecutionOutcomeAssessmentStatus.MANUAL_REVIEW_REQUIRED


def test_non_retryable_failure_is_terminal():
    result = assess_execution_outcome(
        outcome=_outcome(ExecutionOutcomeStatus.FAILED, "permanent_error"),
        attempt_count=1,
        policy=ExecutionOutcomePolicy(retryable_outcome_codes=("temporary_error",), maximum_attempts=3),
    )
    assert result.status is ExecutionOutcomeAssessmentStatus.TERMINAL_FAILURE


def test_rejected_is_terminal():
    result = assess_execution_outcome(
        outcome=_outcome(ExecutionOutcomeStatus.REJECTED, "provider_rejected"),
        attempt_count=1,
        policy=ExecutionOutcomePolicy(retryable_outcome_codes=("provider_rejected",), maximum_attempts=3),
    )
    assert result.status is ExecutionOutcomeAssessmentStatus.TERMINAL_FAILURE


def test_assessment_preserves_identity():
    result = assess_execution_outcome(
        outcome=_outcome(ExecutionOutcomeStatus.FAILED),
        attempt_count=1,
        policy=ExecutionOutcomePolicy(retryable_outcome_codes=("temporary_error",), maximum_attempts=3),
    )
    assert result.request_id == "req-1"
    assert result.idempotency_key == "idem-1"
