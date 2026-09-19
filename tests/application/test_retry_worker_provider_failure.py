from datetime import datetime, timezone

from app.application.execution_port import ExecutionPort
from app.application.retry_worker_dispatch import RetryWorkerDispatchStatus, dispatch_one_retry
from app.domain.action_authorization import ActionClass, AutonomyLevel
from app.domain.authorized_execution_request import AuthorizedExecutionRequest, ExecutionRequestStatus
from app.domain.execution_retry import RetryCommand, RetryCommandAction, RetryCommandState
from app.infrastructure.sqlite_retry_command_store import SQLiteRetryCommandStore


def _command():
    return RetryCommand(
        command_id="cmd-provider", request_id="req-provider", idempotency_key="idem-provider",
        attempt_number=2, action=RetryCommandAction.RETRY,
        authorization_policy_id="policy", authorization_policy_version="v1",
        autonomy_bound="L4", created_at=datetime(2026, 9, 20, tzinfo=timezone.utc),
        state=RetryCommandState.CREATED,
    )


def _prepared_request():
    return AuthorizedExecutionRequest(
        request_id="req-provider", idempotency_key="idem-provider",
        action_class=ActionClass.REVERSIBLE_EXTERNAL,
        autonomy_level=AutonomyLevel.L4_EXECUTE_AUTOMATICALLY_WITHIN_POLICY,
        policy_id="policy", policy_version="v1",
        status=ExecutionRequestStatus.PREPARED,
    )


def _scheduled_store():
    store = SQLiteRetryCommandStore(":memory:")
    created = store.create_or_get(_command())
    store.claim(created.command_id)
    from app.domain.execution_retry import SchedulerAcknowledgement, SchedulerAcknowledgementStatus
    scheduled = store.record_scheduler_acknowledgement(
        created.command_id,
        SchedulerAcknowledgement(
            command_id=created.command_id,
            scheduling_id="schedule-provider",
            status=SchedulerAcknowledgementStatus.ACCEPTED,
            observed_at=datetime(2026, 9, 20, 1, tzinfo=timezone.utc),
        ),
    )
    return scheduled, store


class _Revalidator:
    def revalidate(self, command):
        return _prepared_request()


class _FailingProvider(ExecutionPort):
    def execute(self, request):
        raise RuntimeError("provider unavailable")


class _FailingManualReviewStore(SQLiteRetryCommandStore):
    def save(self, command):
        if command.state is RetryCommandState.REQUIRES_MANUAL_REVIEW:
            raise RuntimeError("manual review persistence unavailable")
        return super().save(command)


def test_provider_failure_transitions_claimed_command_to_manual_review():
    command, store = _scheduled_store()
    result = dispatch_one_retry(
        command=command,
        store=store,
        revalidator=_Revalidator(),
        provider=_FailingProvider(),
    )
    assert result.status is RetryWorkerDispatchStatus.PROVIDER_FAILURE
    assert result.command.state is RetryCommandState.REQUIRES_MANUAL_REVIEW
    assert store.get(command.command_id).state is RetryCommandState.REQUIRES_MANUAL_REVIEW
    assert result.failure == "provider_execution_failed"


def test_provider_failure_persistence_failure_remains_explicit():
    store = _FailingManualReviewStore(":memory:")
    created = store.create_or_get(_command())
    store.claim(created.command_id)
    from app.domain.execution_retry import SchedulerAcknowledgement, SchedulerAcknowledgementStatus
    command = store.record_scheduler_acknowledgement(
        created.command_id,
        SchedulerAcknowledgement(
            command_id=created.command_id,
            scheduling_id="schedule-provider",
            status=SchedulerAcknowledgementStatus.ACCEPTED,
            observed_at=datetime(2026, 9, 20, 1, tzinfo=timezone.utc),
        ),
    )
    result = dispatch_one_retry(
        command=command,
        store=store,
        revalidator=_Revalidator(),
        provider=_FailingProvider(),
    )
    assert result.status is RetryWorkerDispatchStatus.PROVIDER_FAILURE
    assert result.command.state is RetryCommandState.EXECUTION_IN_PROGRESS
    assert result.failure == "provider_failure_persistence_failed"
