from datetime import datetime, timezone

from app.application.retry_orchestration import orchestrate_retry
from app.domain.action_authorization import (
    ActionAuthorization,
    ActionAuthorizationStatus,
    ActionClass,
    AutonomyLevel,
)
from app.domain.execution_retry import (
    RetryCommand,
    RetryCommandAction,
    RetryCommandState,
    SchedulerAcknowledgement,
    SchedulerAcknowledgementStatus,
)


class Store:
    def __init__(self):
        self.command = None

    def create_or_get(self, command):
        if self.command is None:
            self.command = command
        return self.command

    def get(self, command_id):
        return self.command

    def claim(self, command_id):
        return self.command

    def save(self, command):
        self.command = command
        return command

    def record_scheduler_acknowledgement(self, command_id, acknowledgement):
        self.command = RetryCommand(
            **{**self.command.__dict__, "state": RetryCommandState.SCHEDULED, "scheduling_id": acknowledgement.scheduling_id}
        )
        return self.command


class Scheduler:
    def __init__(self, status):
        self.status = status
        self.calls = 0

    def schedule(self, command):
        self.calls += 1
        return SchedulerAcknowledgement(
            command_id=command.command_id,
            scheduling_id="schedule-1",
            status=self.status,
            observed_at=datetime(2026, 9, 19, tzinfo=timezone.utc),
        )


class Revalidator:
    def __init__(self, authorization):
        self.authorization = authorization
        self.calls = 0

    def revalidate(self, command):
        self.calls += 1
        return self.authorization


def command():
    return RetryCommand(
        command_id="cmd-1",
        request_id="req-1",
        idempotency_key="idem-1",
        attempt_number=2,
        action=RetryCommandAction.RETRY,
        authorization_policy_id="policy",
        authorization_policy_version="v1",
        autonomy_bound="L4",
        created_at=datetime(2026, 9, 19, tzinfo=timezone.utc),
    )


def authorization(status=ActionAuthorizationStatus.AUTHORIZED, version="v1"):
    return ActionAuthorization(
        policy_id="policy",
        policy_version=version,
        action_class=ActionClass.REVERSIBLE_EXTERNAL,
        requested_autonomy=AutonomyLevel.L4_EXECUTE_AUTOMATICALLY_WITHIN_POLICY,
        maximum_autonomy=AutonomyLevel.L4_EXECUTE_AUTOMATICALLY_WITHIN_POLICY,
        status=status,
        requires_human_approval=False,
    )


def test_accepted_schedule_requires_revalidation_and_is_scheduled():
    scheduler = Scheduler(SchedulerAcknowledgementStatus.ACCEPTED)
    revalidator = Revalidator(authorization())
    result = orchestrate_retry(
        command=command(),
        store=Store(),
        scheduler=scheduler,
        authorization_revalidator=revalidator,
    )
    assert result.scheduled is True
    assert result.command.state is RetryCommandState.SCHEDULED
    assert revalidator.calls == 1
    assert scheduler.calls == 1


def test_policy_change_blocks_scheduler():
    scheduler = Scheduler(SchedulerAcknowledgementStatus.ACCEPTED)
    result = orchestrate_retry(
        command=command(),
        store=Store(),
        scheduler=scheduler,
        authorization_revalidator=Revalidator(authorization(version="v2")),
    )
    assert result.scheduled is False
    assert result.failure == "authorization_policy_changed"
    assert result.command.state is RetryCommandState.REQUIRES_MANUAL_REVIEW
    assert scheduler.calls == 0


def test_ambiguous_scheduler_result_never_counts_as_scheduled():
    scheduler = Scheduler(SchedulerAcknowledgementStatus.AMBIGUOUS)
    result = orchestrate_retry(
        command=command(),
        store=Store(),
        scheduler=scheduler,
        authorization_revalidator=Revalidator(authorization()),
    )
    assert result.scheduled is False
    assert result.command.state is RetryCommandState.SCHEDULING_AMBIGUOUS


def test_duplicate_command_is_not_rescheduled():
    store = Store()
    first = orchestrate_retry(
        command=command(),
        store=store,
        scheduler=Scheduler(SchedulerAcknowledgementStatus.ACCEPTED),
        authorization_revalidator=Revalidator(authorization()),
    )
    second_scheduler = Scheduler(SchedulerAcknowledgementStatus.ACCEPTED)
    second = orchestrate_retry(
        command=command(),
        store=store,
        scheduler=second_scheduler,
        authorization_revalidator=Revalidator(authorization()),
    )
    assert first.scheduled is True
    assert second.scheduled is False
    assert second.failure == "command_not_schedulable"
    assert second_scheduler.calls == 0


class RaisingScheduler:
    def schedule(self, command):
        raise RuntimeError("scheduler outcome unknown")


def test_scheduler_exception_is_treated_as_ambiguous_and_persisted():
    store = Store()
    result = orchestrate_retry(
        command=command(),
        store=store,
        scheduler=RaisingScheduler(),
        authorization_revalidator=Revalidator(authorization()),
    )
    assert result.scheduled is False
    assert result.failure == "scheduler_call_ambiguous"
    assert result.command.state is RetryCommandState.SCHEDULING_AMBIGUOUS
    assert store.command.state is RetryCommandState.SCHEDULING_AMBIGUOUS


class AcknowledgementPersistenceFailureStore(Store):
    def record_scheduler_acknowledgement(self, command_id, acknowledgement):
        raise RuntimeError("persistence failed")


def test_scheduler_acceptance_with_ack_persistence_failure_is_ambiguous():
    store = AcknowledgementPersistenceFailureStore()
    result = orchestrate_retry(
        command=command(),
        store=store,
        scheduler=Scheduler(SchedulerAcknowledgementStatus.ACCEPTED),
        authorization_revalidator=Revalidator(authorization()),
    )
    assert result.scheduled is False
    assert result.failure == "scheduler_acknowledgement_persistence_ambiguous"
    assert result.command.state is RetryCommandState.SCHEDULING_AMBIGUOUS
    assert store.command.state is RetryCommandState.SCHEDULING_AMBIGUOUS
