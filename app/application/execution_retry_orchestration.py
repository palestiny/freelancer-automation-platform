from datetime import datetime

from app.domain.execution_recovery import ExecutionRecoveryHandoff, ExecutionRecoveryMode
from app.domain.execution_retry import RetryCommand, RetryCommandAction, RetryCommandState, RetryCommandStore, RetrySchedulerPort, SchedulerAcknowledgementStatus

def schedule_retry_command(*, handoff: ExecutionRecoveryHandoff, command_id: str, authorization_policy_id: str, authorization_policy_version: str, autonomy_bound: str, created_at: datetime, store: RetryCommandStore, scheduler: RetrySchedulerPort) -> RetryCommand:
    if handoff.mode is not ExecutionRecoveryMode.RETRY:
        raise ValueError('only retry recovery handoffs can be scheduled')
    command = RetryCommand(command_id=command_id, request_id=handoff.request_id, idempotency_key=handoff.idempotency_key, attempt_number=handoff.attempt_count + 1, action=RetryCommandAction.RETRY, authorization_policy_id=authorization_policy_id, authorization_policy_version=authorization_policy_version, autonomy_bound=autonomy_bound, created_at=created_at)
    durable = store.create_or_get(command)
    if durable.state in {RetryCommandState.SCHEDULED, RetryCommandState.COMPLETED, RetryCommandState.REQUIRES_MANUAL_REVIEW, RetryCommandState.REJECTED_STALE, RetryCommandState.SCHEDULING_AMBIGUOUS}:
        return durable
    if durable.state is not RetryCommandState.CREATED:
        raise ValueError('retry command is not schedulable from its current state')
    claimed = store.save(durable.transition_to(RetryCommandState.CLAIMED))
    acknowledgement = scheduler.schedule(claimed)
    if acknowledgement.status is SchedulerAcknowledgementStatus.ACCEPTED:
        return store.record_scheduler_acknowledgement(claimed.command_id, acknowledgement)
    if acknowledgement.status is SchedulerAcknowledgementStatus.AMBIGUOUS:
        return store.save(claimed.transition_to(RetryCommandState.SCHEDULING_AMBIGUOUS, scheduling_id=acknowledgement.scheduling_id))
    return store.save(claimed.transition_to(RetryCommandState.REQUIRES_MANUAL_REVIEW, scheduling_id=acknowledgement.scheduling_id))