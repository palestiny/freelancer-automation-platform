from datetime import datetime, timezone

import pytest

from app.application.execution_status_port import ProviderExecutionStatusResult
from app.domain.execution_outcome import ExecutionOutcomeStatus
from app.domain.execution_retry import RetryCommand, RetryCommandAction, RetryCommandState
from app.domain.retry_status_reconciliation import (
    RetryRecoveryAssessment,
    RetryRecoveryAssessmentStatus,
    assess_retry_status_reconciliation,
)


def _command(state):
    return RetryCommand(
        command_id="cmd-1",
        request_id="request-1",
        idempotency_key="idem-1",
        attempt_number=1,
        action=RetryCommandAction.RETRY,
        authorization_policy_id="policy",
        authorization_policy_version="1",
        autonomy_bound="L3",
        created_at=datetime(2026, 9, 20, 8, 0, tzinfo=timezone.utc),
        state=state,
    )


def _status(status):
    return ProviderExecutionStatusResult(
        request_id="request-1",
        idempotency_key="idem-1",
        status=status,
        outcome_code="provider",
        observed_at=datetime(2026, 9, 20, 8, 1, tzinfo=timezone.utc),
    )


def test_successful_provider_status_confirms_completion_without_mutating_command():
    command = _command(RetryCommandState.EXECUTION_IN_PROGRESS)
    assessment = assess_retry_status_reconciliation(
        command=command,
        provider_status=_status(ExecutionOutcomeStatus.SUCCEEDED),
    )
    assert isinstance(assessment, RetryRecoveryAssessment)
    assert assessment.status is RetryRecoveryAssessmentStatus.CONFIRMED_COMPLETED
    assert assessment.target_state is RetryCommandState.COMPLETED
    assert command.state is RetryCommandState.EXECUTION_IN_PROGRESS


def test_failed_provider_status_requires_manual_review():
    assessment = assess_retry_status_reconciliation(
        command=_command(RetryCommandState.EXECUTION_IN_PROGRESS),
        provider_status=_status(ExecutionOutcomeStatus.FAILED),
    )
    assert assessment.status is RetryRecoveryAssessmentStatus.CONFIRMED_FAILURE_REQUIRES_REVIEW
    assert assessment.target_state is RetryCommandState.REQUIRES_MANUAL_REVIEW


def test_unknown_provider_status_remains_ambiguous():
    assessment = assess_retry_status_reconciliation(
        command=_command(RetryCommandState.EXECUTION_IN_PROGRESS),
        provider_status=_status(ExecutionOutcomeStatus.UNKNOWN),
    )
    assert assessment.status is RetryRecoveryAssessmentStatus.REMAINS_AMBIGUOUS
    assert assessment.target_state is None


def test_terminal_command_is_not_reopened():
    assessment = assess_retry_status_reconciliation(
        command=_command(RetryCommandState.COMPLETED),
        provider_status=_status(ExecutionOutcomeStatus.FAILED),
    )
    assert assessment.status is RetryRecoveryAssessmentStatus.NO_RECONCILIATION_REQUIRED
    assert assessment.target_state is None


def test_identity_mismatch_is_explicit():
    provider_status = ProviderExecutionStatusResult(
        request_id="other",
        idempotency_key="idem-1",
        status=ExecutionOutcomeStatus.SUCCEEDED,
        outcome_code="provider",
        observed_at=datetime(2026, 9, 20, 8, 1, tzinfo=timezone.utc),
    )
    with pytest.raises(ValueError, match="request_id"):
        assess_retry_status_reconciliation(
            command=_command(RetryCommandState.EXECUTION_IN_PROGRESS),
            provider_status=provider_status,
        )
