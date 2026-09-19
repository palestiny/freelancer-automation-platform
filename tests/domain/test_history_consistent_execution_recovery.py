from datetime import datetime, timezone

from app.domain.execution_attempt_history import ExecutionAttempt, ExecutionAttemptHistory
from app.domain.execution_history_consistency import ExecutionHistoryConsistencyStatus
from app.domain.execution_outcome import ExecutionOutcome, ExecutionOutcomeStatus
from app.domain.execution_outcome_policy import (
    ExecutionOutcomeAssessmentStatus,
    ExecutionOutcomePolicy,
)
from app.domain.execution_recovery import ExecutionRecoveryMode
from app.domain.history_consistent_execution_recovery import (
    create_execution_recovery_handoff_with_history,
)


def outcome_time():
    return datetime(2026, 9, 19, tzinfo=timezone.utc)


def _outcome():
    return ExecutionOutcome(
        request_id="req-1",
        idempotency_key="idem-1",
        status=ExecutionOutcomeStatus.FAILED,
        outcome_code="provider_failure",
        observed_at=outcome_time(),
        external_reference="p-1",
    )


def _attempt(number=1, *, request_id="req-1"):
    return ExecutionAttempt(
        request_id=request_id,
        idempotency_key="idem-1",
        attempt_number=number,
        status=ExecutionOutcomeStatus.FAILED,
        outcome_code="provider_failure",
        observed_at=outcome_time(),
        external_reference="p-1",
    )


def test_consistent_history_produces_history_derived_retry_handoff():
    outcome = _outcome()
    history = ExecutionAttemptHistory(
        request_id="req-1",
        idempotency_key="idem-1",
        attempts=(_attempt(1),),
    )

    result = create_execution_recovery_handoff_with_history(
        outcome=outcome,
        history=history,
        policy=ExecutionOutcomePolicy(max_retries=3),
    )

    assert result.consistency_status is ExecutionHistoryConsistencyStatus.CONSISTENT
    assert result.handoff is not None
    assert result.handoff.attempt_count == 1
    assert result.handoff.mode is ExecutionRecoveryMode.RETRY


def test_inconsistent_history_blocks_recovery_handoff():
    outcome = _outcome()
    history = ExecutionAttemptHistory(
        request_id="other",
        idempotency_key="idem-1",
        attempts=(_attempt(1, request_id="other"),),
    )

    result = create_execution_recovery_handoff_with_history(
        outcome=outcome,
        history=history,
        policy=ExecutionOutcomePolicy(max_retries=3),
    )

    assert result.handoff is None
    assert result.consistency_status is not ExecutionHistoryConsistencyStatus.CONSISTENT


def test_manual_review_is_preserved_as_manual_review():
    outcome = _outcome()
    history = ExecutionAttemptHistory(
        request_id="req-1",
        idempotency_key="idem-1",
        attempts=(_attempt(1),),
    )

    result = create_execution_recovery_handoff_with_history(
        outcome=outcome,
        history=history,
        policy=ExecutionOutcomePolicy(max_retries=0),
    )

    assert result.handoff is not None
    assert result.handoff.mode is ExecutionRecoveryMode.MANUAL_REVIEW
    assert result.handoff.source_status is ExecutionOutcomeAssessmentStatus.MANUAL_REVIEW_REQUIRED
