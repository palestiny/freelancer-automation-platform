from datetime import datetime, timezone

import pytest

from app.application.execution_status_port import (
    ProviderExecutionStatusPort,
    ProviderExecutionStatusQuery,
    ProviderExecutionStatusResult,
)
from app.application.retry_status_assessment_application import RetryStatusAssessmentApplication
from app.application.retry_status_reconciliation_coordinator import RetryStatusReconciliationCoordinator
from app.domain.execution_outcome import ExecutionOutcomeStatus
from app.domain.execution_retry import RetryCommand, RetryCommandAction, RetryCommandState


def _command(state):
    return RetryCommand(
        command_id="cmd-1", request_id="req-1", idempotency_key="idem-1",
        attempt_number=2, action=RetryCommandAction.RETRY,
        authorization_policy_id="policy", authorization_policy_version="v1",
        autonomy_bound="L3", created_at=datetime(2026, 9, 20, tzinfo=timezone.utc),
        state=state,
    )


class Store:
    def __init__(self, command):
        self.command = command

    def get(self, command_id):
        return self.command if self.command.command_id == command_id else None

    def transition_if_current(self, command_id, expected_state, target_state):
        if self.command.command_id != command_id or self.command.state is not expected_state:
            return None
        self.command = self.command.transition_to(target_state)
        return self.command


class StatusPort(ProviderExecutionStatusPort):
    def __init__(self, status=None, error=None):
        self.status = status
        self.error = error
        self.calls = 0

    def get_status(self, query):
        self.calls += 1
        if self.error:
            raise self.error
        return self.status


def _status(status):
    return ProviderExecutionStatusResult(
        request_id="req-1", idempotency_key="idem-1", status=status,
        outcome_code="provider", observed_at=datetime(2026, 9, 20, 8, 1, tzinfo=timezone.utc),
    )


def test_success_coordinates_observation_assessment_and_application():
    store = Store(_command(RetryCommandState.EXECUTION_IN_PROGRESS))
    port = StatusPort(_status(ExecutionOutcomeStatus.SUCCEEDED))
    result = RetryStatusReconciliationCoordinator(
        store=store,
        status_port=port,
        assessment_application=RetryStatusAssessmentApplication(store),
    ).reconcile(command_id="cmd-1", expected_state=RetryCommandState.EXECUTION_IN_PROGRESS)
    assert result.state is RetryCommandState.COMPLETED
    assert port.calls == 1
    assert result.identity == ("req-1", "idem-1", 2, "cmd-1")


def test_failure_resolves_to_manual_review_without_retry():
    store = Store(_command(RetryCommandState.EXECUTION_IN_PROGRESS))
    port = StatusPort(_status(ExecutionOutcomeStatus.FAILED))
    result = RetryStatusReconciliationCoordinator(
        store=store, status_port=port,
        assessment_application=RetryStatusAssessmentApplication(store),
    ).reconcile(command_id="cmd-1", expected_state=RetryCommandState.EXECUTION_IN_PROGRESS)
    assert result.state is RetryCommandState.REQUIRES_MANUAL_REVIEW
    assert port.calls == 1


def test_unknown_status_leaves_command_unchanged():
    command = _command(RetryCommandState.EXECUTION_IN_PROGRESS)
    store = Store(command)
    port = StatusPort(_status(ExecutionOutcomeStatus.UNKNOWN))
    result = RetryStatusReconciliationCoordinator(
        store=store, status_port=port,
        assessment_application=RetryStatusAssessmentApplication(store),
    ).reconcile(command_id="cmd-1", expected_state=RetryCommandState.EXECUTION_IN_PROGRESS)
    assert result is command
    assert port.calls == 1


def test_terminal_command_is_not_observed_again():
    store = Store(_command(RetryCommandState.COMPLETED))
    port = StatusPort(_status(ExecutionOutcomeStatus.FAILED))
    result = RetryStatusReconciliationCoordinator(
        store=store, status_port=port,
        assessment_application=RetryStatusAssessmentApplication(store),
    ).reconcile(command_id="cmd-1", expected_state=RetryCommandState.COMPLETED)
    assert result.state is RetryCommandState.COMPLETED
    assert port.calls == 0


def test_provider_failure_does_not_mutate_command():
    command = _command(RetryCommandState.EXECUTION_IN_PROGRESS)
    store = Store(command)
    port = StatusPort(error=RuntimeError("provider unavailable"))
    coordinator = RetryStatusReconciliationCoordinator(
        store=store, status_port=port,
        assessment_application=RetryStatusAssessmentApplication(store),
    )
    with pytest.raises(RuntimeError, match="provider unavailable"):
        coordinator.reconcile(command_id="cmd-1", expected_state=RetryCommandState.EXECUTION_IN_PROGRESS)
    assert store.command is command
