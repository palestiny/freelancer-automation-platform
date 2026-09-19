from datetime import datetime, timezone

import pytest

from app.domain.execution_recovery import ExecutionRecoveryHandoff, ExecutionRecoveryMode, ExecutionRecoveryReason
from app.domain.execution_outcome_policy import ExecutionOutcomeAssessmentStatus
from app.domain.execution_retry import RetryCommand, RetryCommandAction, RetryCommandState, SchedulerAcknowledgement, SchedulerAcknowledgementStatus
from app.application.execution_retry_orchestration import schedule_retry_command

class FakeStore:
    def __init__(self, existing=None):
        self.existing = existing
        self.created = []
        self.acks = []
    def create_or_get(self, command):
        self.created.append(command)
        return self.existing or command
    def get(self, command_id): return self.existing
    def claim(self, command_id): return None
    def record_scheduler_acknowledgement(self, command_id, acknowledgement):
        self.acks.append((command_id, acknowledgement))
        command = self.existing or self.created[-1]
        return command.transition_to(RetryCommandState.SCHEDULED, scheduling_id=acknowledgement.scheduling_id)
    def save(self, command): return command

class FakeScheduler:
    def __init__(self, status=SchedulerAcknowledgementStatus.ACCEPTED): self.status=status; self.calls=[]
    def schedule(self, command):
        self.calls.append(command)
        return SchedulerAcknowledgement(command_id=command.command_id, scheduling_id='sched-1', status=self.status, observed_at=datetime(2026,9,19,tzinfo=timezone.utc))

def _handoff(mode=ExecutionRecoveryMode.RETRY):
    status = ExecutionOutcomeAssessmentStatus.RETRY_ELIGIBLE if mode is ExecutionRecoveryMode.RETRY else ExecutionOutcomeAssessmentStatus.MANUAL_REVIEW_REQUIRED
    return ExecutionRecoveryHandoff(request_id='req-1', idempotency_key='idem-1', attempt_count=2, mode=mode, reason=ExecutionRecoveryReason.RETRY_ELIGIBLE if mode is ExecutionRecoveryMode.RETRY else ExecutionRecoveryReason.MANUAL_REVIEW_REQUIRED, source_status=status)

def test_retry_command_uses_history_derived_next_attempt_and_persists_before_schedule():
    store=FakeStore(); scheduler=FakeScheduler()
    result=schedule_retry_command(handoff=_handoff(),command_id='cmd-1',authorization_policy_id='policy-1',authorization_policy_version='v1',autonomy_bound='L3',created_at=datetime(2026,9,19,tzinfo=timezone.utc),store=store,scheduler=scheduler)
    assert result.state is RetryCommandState.SCHEDULED
    assert store.created[0].attempt_number == 3
    assert len(scheduler.calls) == 1

def test_ambiguous_scheduler_ack_is_not_retried():
    store=FakeStore(); scheduler=FakeScheduler(SchedulerAcknowledgementStatus.AMBIGUOUS)
    result=schedule_retry_command(handoff=_handoff(),command_id='cmd-1',authorization_policy_id='policy-1',authorization_policy_version='v1',autonomy_bound='L3',created_at=datetime(2026,9,19,tzinfo=timezone.utc),store=store,scheduler=scheduler)
    assert result.state is RetryCommandState.SCHEDULING_AMBIGUOUS
    assert len(scheduler.calls) == 1

def test_manual_review_handoff_cannot_become_retry_command():
    with pytest.raises(ValueError): schedule_retry_command(handoff=_handoff(ExecutionRecoveryMode.MANUAL_REVIEW),command_id='cmd-1',authorization_policy_id='policy-1',authorization_policy_version='v1',autonomy_bound='L3',created_at=datetime(2026,9,19,tzinfo=timezone.utc),store=FakeStore(),scheduler=FakeScheduler())

def test_existing_scheduled_command_is_not_scheduled_again():
    existing=RetryCommand(command_id='cmd-1',request_id='req-1',idempotency_key='idem-1',attempt_number=3,action=RetryCommandAction.RETRY,authorization_policy_id='policy-1',authorization_policy_version='v1',autonomy_bound='L3',created_at=datetime(2026,9,19,tzinfo=timezone.utc),state=RetryCommandState.SCHEDULED,scheduling_id='sched-existing')
    store=FakeStore(existing=existing); scheduler=FakeScheduler()
    result=schedule_retry_command(handoff=_handoff(),command_id='different',authorization_policy_id='policy-1',authorization_policy_version='v1',autonomy_bound='L3',created_at=datetime(2026,9,19,tzinfo=timezone.utc),store=store,scheduler=scheduler)
    assert result is existing
    assert scheduler.calls == []