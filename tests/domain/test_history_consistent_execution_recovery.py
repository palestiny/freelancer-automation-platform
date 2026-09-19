import pytest

from app.domain.execution_attempt_history import ExecutionAttemptHistory
from app.domain.execution_history_consistency import ExecutionHistoryConsistencyStatus
from app.domain.execution_outcome import ExecutionOutcome
from app.domain.execution_outcome_policy import (
    ExecutionOutcomeAssessmentStatus,
    ExecutionOutcomePolicy,
)
from app.domain.execution_recovery import (
    ExecutionRecoveryMode,
    create_execution_recovery_handoff_with_history,
)


def test_consistent_history_produces_history_derived_retry_handoff():
    outcome = ExecutionOutcome(
        request_id="req-1",
        idempotency_key="idem-1",
        status="failed",
        provider_reference="p-1",
        occurred_at=outcome_time(),
        attempt_number=2,
    )
    history = ExecutionAttemptHistory(
        request_id="req-1",
        idempotency_key="idem-1",
        attempts=(outcome,),
    )
    policy = ExecutionOutcomePolicy(max_retries=3)

    result = create_execution_recovery_handoff_with_history(
        outcome=outcome,
        history=history,
        policy=policy,
    )

    assert result.consistency_status is ExecutionHistoryConsistencyStatus.CONSISTENT
    assert result.handoff is not None
    assert result.handoff.attempt_count == 1
    assert result.handoff.mode is ExecutionRecoveryMode.RETRY


def test_inconsistent_history_blocks_recovery_handoff():
    outcome = ExecutionOutcome(
        request_id="req-1",
        idempotency_key="idem-1",
        status="failed",
        provider_reference="p-1",
        occurred_at=outcome_time(),
        attempt_number=2,
    )
    history = ExecutionAttemptHistory(
        request_id="other",
        idempotency_key="idem-1",
        attempts=(outcome,),
    )

    result = create_execution_recovery_handoff_with_history(
        outcome=outcome,
        history=history,
        policy=ExecutionOutcomePolicy(max_retries=3),
    )

    assert result.handoff is None
    assert result.consistency_status is not ExecutionHistoryConsistencyStatus.CONSISTENT


def test_manual_review_is_preserved_as_manual_review():
    outcome = ExecutionOutcome(
        request_id="req-1",
        idempotency_key="idem-1",
        status="failed",
        provider_reference="p-1",
        occurred_at=outcome_time(),
        attempt_number=1,
    )
    history = ExecutionAttemptHistory(
        request_id="req-1",
        idempotency_key="idem-1",
        attempts=(outcome,),
    )

    result = create_execution_recovery_handoff_with_history(
        outcome=outcome,
        history=history,
        policy=ExecutionOutcomePolicy(max_retries=0),
    )

    assert result.handoff is not None
    assert result.handoff.mode is ExecutionRecoveryMode.MANUAL_REVIEW
    assert result.handoff.source_status is ExecutionOutcomeAssessmentStatus.MANUAL_REVIEW_REQUIRED


def outcome_time():
    from datetime import datetime, timezone
    return datetime(2026, 9, 19, tzinfo=timezone.utc)
