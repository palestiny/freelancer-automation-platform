from dataclasses import dataclass
from typing import Protocol

from app.domain.action_authorization import ActionAuthorization, ActionAuthorizationStatus
from app.domain.execution_retry import (
    RetryCommand,
    RetryCommandAction,
    RetryCommandState,
    RetryCommandStore,
    RetrySchedulerPort,
    SchedulerAcknowledgementStatus,
)


class RetryAuthorizationRevalidator(Protocol):
    def revalidate(self, command: RetryCommand) -> ActionAuthorization:
        ...


class RetryOrchestrationFailure(str):
    pass


@dataclass(frozen=True)
class RetryOrchestrationResult:
    command: RetryCommand
    scheduled: bool
    failure: str | None = None


def orchestrate_retry(
    *,
    command: RetryCommand,
    store: RetryCommandStore,
    scheduler: RetrySchedulerPort,
    authorization_revalidator: RetryAuthorizationRevalidator,
) -> RetryOrchestrationResult:
    existing = store.create_or_get(command)
    if existing.command_id != command.command_id:
        return RetryOrchestrationResult(
            command=existing,
            scheduled=False,
            failure="idempotency_conflict",
        )

    if existing.action is not RetryCommandAction.RETRY:
        return RetryOrchestrationResult(command=existing, scheduled=False, failure="manual_review_not_schedulable")

    if existing.state is not RetryCommandState.CREATED:
        return RetryOrchestrationResult(
            command=existing,
            scheduled=False,
            failure="command_not_schedulable",
        )

    claimed = store.claim(existing.command_id)
    if claimed is None:
        return RetryOrchestrationResult(command=existing, scheduled=False, failure="claim_conflict")
    existing = claimed

    authorization = authorization_revalidator.revalidate(existing)
    if authorization.status is not ActionAuthorizationStatus.AUTHORIZED:
        updated = _state(existing, RetryCommandState.REQUIRES_MANUAL_REVIEW)
        store.save(updated)
        return RetryOrchestrationResult(command=updated, scheduled=False, failure="authorization_revalidation_failed")

    if (
        authorization.policy_id != existing.authorization_policy_id
        or authorization.policy_version != existing.authorization_policy_version
        or f"L{authorization.requested_autonomy.value}" != existing.autonomy_bound
    ):
        updated = _state(existing, RetryCommandState.REQUIRES_MANUAL_REVIEW)
        store.save(updated)
        return RetryOrchestrationResult(command=updated, scheduled=False, failure=("authorization_policy_changed" if authorization.policy_id != existing.authorization_policy_id or authorization.policy_version != existing.authorization_policy_version else "authorization_autonomy_changed"))

    try:
        acknowledgement = scheduler.schedule(existing)
    except Exception:
        ambiguous = _state(existing, RetryCommandState.SCHEDULING_AMBIGUOUS)
        store.save(ambiguous)
        return RetryOrchestrationResult(
            command=ambiguous,
            scheduled=False,
            failure="scheduler_call_ambiguous",
        )

    if acknowledgement.command_id != existing.command_id:
        return RetryOrchestrationResult(
            command=_state(existing, RetryCommandState.SCHEDULING_AMBIGUOUS),
            scheduled=False,
            failure="scheduler_command_mismatch",
        )

    if acknowledgement.status is SchedulerAcknowledgementStatus.ACCEPTED:
        try:
            scheduled = store.record_scheduler_acknowledgement(
                existing.command_id, acknowledgement
            )
        except Exception:
            ambiguous = _state(
                existing,
                RetryCommandState.SCHEDULING_AMBIGUOUS,
                acknowledgement.scheduling_id,
            )
            store.save(ambiguous)
            return RetryOrchestrationResult(
                command=ambiguous,
                scheduled=False,
                failure="scheduler_acknowledgement_persistence_ambiguous",
            )
        return RetryOrchestrationResult(command=scheduled, scheduled=True)

    if acknowledgement.status is SchedulerAcknowledgementStatus.REJECTED:
        rejected = _state(existing, RetryCommandState.REQUIRES_MANUAL_REVIEW, acknowledgement.scheduling_id)
        store.save(rejected)
        return RetryOrchestrationResult(command=rejected, scheduled=False, failure="scheduler_rejected")

    ambiguous = _state(existing, RetryCommandState.SCHEDULING_AMBIGUOUS, acknowledgement.scheduling_id)
    store.save(ambiguous)
    return RetryOrchestrationResult(command=ambiguous, scheduled=False, failure="scheduler_acknowledgement_ambiguous")


def _state(
    command: RetryCommand,
    state: RetryCommandState,
    scheduling_id: str | None = None,
) -> RetryCommand:
    return RetryCommand(
        command_id=command.command_id,
        request_id=command.request_id,
        idempotency_key=command.idempotency_key,
        attempt_number=command.attempt_number,
        action=command.action,
        authorization_policy_id=command.authorization_policy_id,
        authorization_policy_version=command.authorization_policy_version,
        autonomy_bound=command.autonomy_bound,
        created_at=command.created_at,
        state=state,
        scheduling_id=scheduling_id or command.scheduling_id,
    )
