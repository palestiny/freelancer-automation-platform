from datetime import datetime, timezone

from app.domain.execution_attempt_history import ExecutionAttempt, ExecutionAttemptHistory
from app.domain.execution_history_consistency import ExecutionHistoryConsistencyStatus
from app.domain.execution_outcome import ExecutionOutcome, ExecutionOutcomeStatus
from app.domain.execution_outcome_policy import ExecutionOutcomeAssessmentStatus, ExecutionOutcomePolicy
from app.domain.execution_policy_history import assess_execution_outcome_with_history


def _outcome(status=ExecutionOutcomeStatus.FAILED, code="timeout"):
    return ExecutionOutcome(
        request_id="r1",
        idempotency_key="k1",
        status=status,
        outcome_code=code,
        observed_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
        external_reference=None,
    )


def _history(attempt_number=1, outcome=None):
    outcome = outcome or _outcome()
    return ExecutionAttemptHistory(
        request_id="r1",
        idempotency_key="k1",
        attempts=(
            ExecutionAttempt(
                request_id="r1",
                idempotency_key="k1",
                attempt_number=attempt_number,
                status=outcome.status,
                outcome_code=outcome.outcome_code,
                observed_at=outcome.observed_at,
                external_reference=outcome.external_reference,
            ),
        ),
    )


def test_consistent_history_drives_attempt_count_and_retry_policy():
    result = assess_execution_outcome_with_history(
        outcome=_outcome(),
        history=_history(),
        policy=ExecutionOutcomePolicy(retryable_outcome_codes=("timeout",), maximum_attempts=2),
    )
    assert result.consistency_status is ExecutionHistoryConsistencyStatus.CONSISTENT
    assert result.assessment is not None
    assert result.assessment.attempt_count == 1
    assert result.assessment.status is ExecutionOutcomeAssessmentStatus.RETRY_ELIGIBLE


def test_latest_attempt_mismatch_blocks_policy_assessment():
    history = _history()
    outcome = _outcome(code="provider_timeout")
    result = assess_execution_outcome_with_history(
        outcome=outcome,
        history=history,
        policy=ExecutionOutcomePolicy(retryable_outcome_codes=("provider_timeout",), maximum_attempts=2),
    )
    assert result.assessment is None
    assert result.consistency_status is ExecutionHistoryConsistencyStatus.LATEST_ATTEMPT_MISMATCH


def test_empty_history_blocks_policy_assessment():
    history = ExecutionAttemptHistory(request_id="r1", idempotency_key="k1")
    result = assess_execution_outcome_with_history(
        outcome=_outcome(),
        history=history,
        policy=ExecutionOutcomePolicy(retryable_outcome_codes=("timeout",), maximum_attempts=2),
    )
    assert result.assessment is None
    assert result.consistency_status is ExecutionHistoryConsistencyStatus.EMPTY_HISTORY


def test_history_identity_mismatch_blocks_policy_assessment():
    history = ExecutionAttemptHistory(request_id="other", idempotency_key="k1")
    result = assess_execution_outcome_with_history(
        outcome=_outcome(),
        history=history,
        policy=ExecutionOutcomePolicy(retryable_outcome_codes=("timeout",), maximum_attempts=2),
    )
    assert result.assessment is None
    assert result.consistency_status is ExecutionHistoryConsistencyStatus.IDENTITY_MISMATCH


def test_maximum_attempts_uses_history_not_caller_supplied_count():
    history = _history(attempt_number=2)
    result = assess_execution_outcome_with_history(
        outcome=_outcome(),
        history=history,
        policy=ExecutionOutcomePolicy(retryable_outcome_codes=("timeout",), maximum_attempts=2),
    )
    assert result.assessment is not None
    assert result.assessment.attempt_count == 1
