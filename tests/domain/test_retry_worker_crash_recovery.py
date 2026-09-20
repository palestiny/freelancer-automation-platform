from datetime import datetime, timezone

import pytest

from app.domain.execution_attempt_history import ExecutionAttempt, ExecutionAttemptHistory
from app.domain.execution_outcome import ExecutionOutcome, ExecutionOutcomeStatus
from app.domain.retry_worker_crash_recovery import (
    CrashRecoveryDisposition,
    CrashRecoveryReason,
    reconcile_crashed_retry_command,
)
from app.domain.execution_retry import RetryCommand, RetryCommandAction, RetryCommandState


NOW = datetime(2026, 1, 1, tzinfo=timezone.utc)


def _command(state=RetryCommandState.EXECUTION_IN_PROGRESS):
    return RetryCommand(
        command_id="cmd-1",
        request_id="req-1",
        idempotency_key="idem-1",
        attempt_number=2,
        action=RetryCommandAction.RETRY,
        authorization_policy_id="policy",
        authorization_policy_version="1",
        autonomy_bound="L2",
        created_at=NOW,
        state=state,
    )


def _history(status=ExecutionOutcomeStatus.UNKNOWN):
    attempt = ExecutionAttempt(
        request_id="req-1",
        idempotency_key="idem-1",
        attempt_number=2,
        status=status,
        outcome_code="provider_outcome_unknown",
        observed_at=NOW,
    )
    return ExecutionAttemptHistory(
        request_id="req-1",
        idempotency_key="idem-1",
        attempts=(attempt,),
    )


def test_in_flight_command_with_unknown_outcome_requires_manual_reconciliation():
    result = reconcile_crashed_retry_command(
        command=_command(),
        history=_history(),
    )
    assert result.disposition is CrashRecoveryDisposition.REQUIRES_MANUAL_RECONCILIATION
    assert result.reason is CrashRecoveryReason.AMBIGUOUS_IN_FLIGHT
    assert result.request_id == "req-1"
    assert result.idempotency_key == "idem-1"
    assert result.reexecute is False


def test_terminal_command_is_not_reopened():
    result = reconcile_crashed_retry_command(
        command=_command(RetryCommandState.COMPLETED),
        history=_history(ExecutionOutcomeStatus.SUCCEEDED),
    )
    assert result.disposition is CrashRecoveryDisposition.SAFE_TO_RELEASE_FOR_REVIEW
    assert result.reason is CrashRecoveryReason.ALREADY_TERMINAL
    assert result.reexecute is False


def test_identity_mismatch_requires_manual_reconciliation():
    history = ExecutionAttemptHistory(
        request_id="different",
        idempotency_key="idem-1",
        attempts=(),
    )
    result = reconcile_crashed_retry_command(command=_command(), history=history)
    assert result.disposition is CrashRecoveryDisposition.REQUIRES_MANUAL_RECONCILIATION
    assert result.reason is CrashRecoveryReason.IDENTITY_MISMATCH
    assert result.reexecute is False


def test_empty_history_requires_manual_reconciliation():
    history = ExecutionAttemptHistory(request_id="req-1", idempotency_key="idem-1")
    result = reconcile_crashed_retry_command(command=_command(), history=history)
    assert result.reason is CrashRecoveryReason.MISSING_ATTEMPT_HISTORY
    assert result.disposition is CrashRecoveryDisposition.REQUIRES_MANUAL_RECONCILIATION


def test_duplicate_reconciliation_is_not_reexecuted():
    result = reconcile_crashed_retry_command(
        command=_command(),
        history=_history(),
        reconciled_command_ids=frozenset({"cmd-1"}),
    )
    assert result.reason is CrashRecoveryReason.DUPLICATE_RECONCILIATION
    assert result.disposition is CrashRecoveryDisposition.SAFE_TO_RELEASE_FOR_REVIEW
    assert result.reexecute is False


def test_reconciliation_result_preserves_command_identity():
    result = reconcile_crashed_retry_command(
        command=_command(),
        history=_history(),
    )
    assert result.command_id == "cmd-1"
    assert result.request_id == "req-1"
    assert result.idempotency_key == "idem-1"
    assert result.attempt_number == 2


def test_reconciliation_does_not_accept_non_execution_state_as_ambiguous():
    result = reconcile_crashed_retry_command(
        command=_command(RetryCommandState.SCHEDULED),
        history=_history(),
    )
    assert result.reason is CrashRecoveryReason.NOT_IN_FLIGHT


def test_result_rejects_empty_identity():
    with pytest.raises(ValueError):
        from app.domain.retry_worker_crash_recovery import CrashRecoveryResult
        CrashRecoveryResult(
            command_id="",
            request_id="req",
            idempotency_key="idem",
            attempt_number=1,
            disposition=CrashRecoveryDisposition.REQUIRES_MANUAL_RECONCILIATION,
            reason=CrashRecoveryReason.AMBIGUOUS_IN_FLIGHT,
            reexecute=False,
        )
