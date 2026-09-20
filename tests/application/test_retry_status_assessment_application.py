from datetime import datetime, timezone

import pytest

from app.domain.execution_outcome import ExecutionOutcomeStatus
from app.domain.execution_retry import RetryCommandAction, RetryCommandState
from app.domain.retry_status_reconciliation import (
    RetryRecoveryAssessment,
    RetryRecoveryAssessmentStatus,
)
from app.application.retry_status_assessment_application import (
    RetryStatusAssessmentApplication,
)


def _command():
    from app.domain.execution_retry import RetryCommand
    return RetryCommand(
        command_id="cmd-1",
        request_id="req-1",
        idempotency_key="idem-1",
        attempt_number=2,
        action=RetryCommandAction.RETRY,
        authorization_policy_id="policy-1",
        authorization_policy_version="v1",
        autonomy_bound="L3",
        created_at=datetime(2026, 9, 20, tzinfo=timezone.utc),
        state=RetryCommandState.EXECUTION_IN_PROGRESS,
    )


class FakeStore:
    def __init__(self, command):
        self.command = command

    def get(self, command_id):
        return self.command if self.command.command_id == command_id else None

    def transition_if_current(self, command_id, expected_state, target_state):
        if self.command.command_id != command_id:
            return None
        if self.command.state is not expected_state:
            return None
        self.command = self.command.transition_to(target_state)
        return self.command


def _assessment(status, target):
    return RetryRecoveryAssessment(status=status, target_state=target)


def test_confirmed_success_is_applied_atomically():
    store = FakeStore(_command())
    result = RetryStatusAssessmentApplication(store).apply(
        command_id="cmd-1",
        assessment=_assessment(
            RetryRecoveryAssessmentStatus.CONFIRMED_COMPLETED,
            RetryCommandState.COMPLETED,
        ),
        expected_state=RetryCommandState.EXECUTION_IN_PROGRESS,
    )
    assert result.state is RetryCommandState.COMPLETED
    assert result.identity == ("req-1", "idem-1", 2, "cmd-1")


def test_confirmed_failure_moves_to_manual_review_only():
    store = FakeStore(_command())
    result = RetryStatusAssessmentApplication(store).apply(
        command_id="cmd-1",
        assessment=_assessment(
            RetryRecoveryAssessmentStatus.CONFIRMED_FAILURE_REQUIRES_REVIEW,
            RetryCommandState.REQUIRES_MANUAL_REVIEW,
        ),
        expected_state=RetryCommandState.EXECUTION_IN_PROGRESS,
    )
    assert result.state is RetryCommandState.REQUIRES_MANUAL_REVIEW


@pytest.mark.parametrize(
    "status",
    [
        RetryRecoveryAssessmentStatus.REMAINS_AMBIGUOUS,
        RetryRecoveryAssessmentStatus.NO_RECONCILIATION_REQUIRED,
    ],
)
def test_non_mutating_assessments_are_no_ops(status):
    command = _command()
    store = FakeStore(command)
    result = RetryStatusAssessmentApplication(store).apply(
        command_id="cmd-1",
        assessment=_assessment(status, None),
        expected_state=RetryCommandState.EXECUTION_IN_PROGRESS,
    )
    assert result is command
    assert store.command.state is RetryCommandState.EXECUTION_IN_PROGRESS


def test_concurrent_state_change_is_explicit_conflict():
    store = FakeStore(_command().transition_to(RetryCommandState.REQUIRES_MANUAL_REVIEW))
    application = RetryStatusAssessmentApplication(store)
    with pytest.raises(RuntimeError, match="retry command state changed"):
        application.apply(
            command_id="cmd-1",
            assessment=_assessment(
                RetryRecoveryAssessmentStatus.CONFIRMED_COMPLETED,
                RetryCommandState.COMPLETED,
            ),
            expected_state=RetryCommandState.EXECUTION_IN_PROGRESS,
        )
