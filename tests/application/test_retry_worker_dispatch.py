from datetime import datetime, timezone

from app.application.execution_port import ExecutionPort, ProviderExecutionResult
from app.application.retry_worker_dispatch import (
    RetryWorkerDispatchStatus,
    dispatch_one_retry,
)
from app.domain.authorized_execution_request import (
    AuthorizedExecutionRequest,
    ExecutionRequestStatus,
)
from app.domain.action_authorization import ActionClass, AutonomyLevel
from app.domain.execution_outcome import ExecutionOutcomeStatus
from app.domain.execution_retry import (
    RetryCommand,
    RetryCommandAction,
    RetryCommandState,
)
from app.application.retry_execution_handoff import RetryExecutionHandoff
from app.infrastructure.sqlite_retry_command_store import SQLiteRetryCommandStore


def command(state=RetryCommandState.SCHEDULED):
    return RetryCommand(
        command_id="cmd-1", request_id="req-1", idempotency_key="idem-1",
        attempt_number=2, action=RetryCommandAction.RETRY,
        authorization_policy_id="policy", authorization_policy_version="v1",
        autonomy_bound="L4", created_at=datetime(2026,9,20,tzinfo=timezone.utc),
        state=state, scheduling_id="schedule-1",
    )


class Revalidator:
    def __init__(self, request=None, error=None):
        self.request = request
        self.error = error
    def revalidate(self, command):
        if self.error:
            raise self.error
        return self.request


class Provider(ExecutionPort):
    def __init__(self, raw=None, error=None):
        self.raw = raw
        self.error = error
        self.calls = 0
    def execute(self, request):
        self.calls += 1
        if self.error:
            raise self.error
        return self.raw


def prepared_request():
    return AuthorizedExecutionRequest(
        request_id="req-1", idempotency_key="idem-1",
        action_class=ActionClass.REVERSIBLE_EXTERNAL,
        autonomy_level=AutonomyLevel.L4_EXECUTE_AUTOMATICALLY_WITHIN_POLICY,
        policy_id="policy", policy_version="v1",
        status=ExecutionRequestStatus.PREPARED,
    )


def raw_outcome(status="succeeded"):
    return ProviderExecutionResult(
        request_id="req-1",
        idempotency_key="idem-1",
        status=ExecutionOutcomeStatus(status),
        outcome_code=status,
        observed_at=datetime(2026,9,20,1,tzinfo=timezone.utc),
    )


def scheduled_store():
    s=SQLiteRetryCommandStore(":memory:")
    created=s.create_or_get(command(RetryCommandState.CREATED))
    s.claim(created.command_id)
    from app.domain.execution_retry import SchedulerAcknowledgement, SchedulerAcknowledgementStatus
    return s.record_scheduler_acknowledgement(
        created.command_id,
        SchedulerAcknowledgement(
            command_id=created.command_id, scheduling_id="schedule-1",
            status=SchedulerAcknowledgementStatus.ACCEPTED,
            observed_at=datetime(2026,9,20,1,tzinfo=timezone.utc),
        ),
    ), s


def test_successful_worker_dispatch_records_completion():
    cmd, store = scheduled_store()
    provider=Provider(raw=raw_outcome())
    result=dispatch_one_retry(command=cmd, store=store, revalidator=Revalidator(prepared_request()), provider=provider)
    assert result.status is RetryWorkerDispatchStatus.COMPLETED
    assert provider.calls == 1
    assert store.get("cmd-1").state is RetryCommandState.COMPLETED


def test_stale_authorization_is_rejected_without_provider_call():
    cmd, store = scheduled_store()
    stale=prepared_request()
    stale=AuthorizedExecutionRequest(**{**stale.__dict__, "policy_version":"v2"})
    provider=Provider(raw=raw_outcome())
    result=dispatch_one_retry(command=cmd, store=store, revalidator=Revalidator(stale), provider=provider)
    assert result.status is RetryWorkerDispatchStatus.REJECTED_STALE
    assert provider.calls == 0
    assert store.get("cmd-1").state is RetryCommandState.REJECTED_STALE


def test_duplicate_delivery_does_not_execute_twice():
    cmd, store = scheduled_store()
    provider=Provider(raw=raw_outcome())
    first=dispatch_one_retry(command=cmd, store=store, revalidator=Revalidator(prepared_request()), provider=provider)
    second=dispatch_one_retry(command=cmd, store=store, revalidator=Revalidator(prepared_request()), provider=provider)
    assert first.status is RetryWorkerDispatchStatus.COMPLETED
    assert second.status is RetryWorkerDispatchStatus.CLAIM_NOT_ACQUIRED
    assert provider.calls == 1


def test_unknown_provider_outcome_requires_manual_review():
    cmd, store = scheduled_store()
    provider=Provider(raw=raw_outcome("unknown"))
    result=dispatch_one_retry(command=cmd, store=store, revalidator=Revalidator(prepared_request()), provider=provider)
    assert result.status is RetryWorkerDispatchStatus.REQUIRES_MANUAL_REVIEW
    assert store.get("cmd-1").state is RetryCommandState.REQUIRES_MANUAL_REVIEW


def test_provider_failure_does_not_fabricate_outcome():
    cmd, store = scheduled_store()
    provider=Provider(error=RuntimeError("provider unavailable"))
    result=dispatch_one_retry(command=cmd, store=store, revalidator=Revalidator(prepared_request()), provider=provider)
    assert result.status is RetryWorkerDispatchStatus.PROVIDER_FAILURE
    assert result.outcome is None
    assert store.get("cmd-1").state is RetryCommandState.EXECUTION_IN_PROGRESS


def test_revalidation_failure_does_not_execute():
    cmd, store = scheduled_store()
    provider=Provider(raw=raw_outcome())
    result=dispatch_one_retry(command=cmd, store=store, revalidator=Revalidator(error=RuntimeError("revalidation failed")), provider=provider)
    assert result.status is RetryWorkerDispatchStatus.REVALIDATION_FAILURE
    assert provider.calls == 0
    assert store.get("cmd-1").state is RetryCommandState.REQUIRES_MANUAL_REVIEW


def test_claim_failure_is_non_executable():
    cmd, store = scheduled_store()
    provider=Provider(raw=raw_outcome())
    store.claim(cmd.command_id)
    result=dispatch_one_retry(command=cmd, store=store, revalidator=Revalidator(prepared_request()), provider=provider)
    assert result.status is RetryWorkerDispatchStatus.CLAIM_NOT_ACQUIRED
    assert provider.calls == 0
