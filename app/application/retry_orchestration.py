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
    try:
        existing = store.create_or_get(command)
    except Exception:
        return RetryOrchestrationResult(
            command=command,
            scheduled=False,
            failure="command_persistence_failed",
        )

    if existing.identity != command.identity:
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

    try:
        claimed = store.claim(existing.command_id)
    except Exception:
        return RetryOrchestrationResult(
            command=existing,
            scheduled=False,
            failure="claim_persistence_failed",
        )

    if claimed is None:
        return RetryOrchestrationResult(command=existing, scheduled=False, failure="claim_conflict")
    if claimed.state is not RetryCommandState.CLAIMED:
        return RetryOrchestrationResult(command=claimed, scheduled=False, failure="claim_state_invalid")
    existing = claimed

    try:
        authorization = authorization_revalidator.revalidate(existing)
    except Exception:
        updated = _state(existing, RetryCommandState.REQUIRES_MANUAL_REVIEW)
        persisted, failure = _try_persist_state(store, updated)
        return RetryOrchestrationResult(command=persisted, scheduled=False, failure=failure or "authorization_revalidation_failed")
    if authorization.status is not ActionAuthorizationStatus.AUTHORIZED:
        updated = _state(existing, RetryCommandState.REQUIRES_MANUAL_REVIEW)
        try:
            persisted = store.save(updated)
        except Exception:
            return RetryOrchestrationResult(
                command=existing,
                scheduled=False,
                failure="state_persistence_failed",
            )
        return RetryOrchestrationResult(command=persisted, scheduled=False, failure="authorization_revalidation_failed")

    if (
        authorization.policy_id != existing.authorization_policy_id
        or authorization.policy_version != existing.authorization_policy_version
        or f"L{authorization.requested_autonomy.value}" != existing.autonomy_bound
    ):
        updated = _state(existing, RetryCommandState.REQUIRES_MANUAL_REVIEW)
        try:
            persisted = store.save(updated)
        except Exception:
            return RetryOrchestrationResult(
                command=existing,
                scheduled=False,
                failure="state_persistence_failed",
            )
        return RetryOrchestrationResult(command=persisted, scheduled=False, failure=("authorization_policy_changed" if authorization.policy_id != existing.authorization_policy_id or authorization.policy_version != existing.authorization_policy_version else "authorization_autonomy_changed"))

    try:
        acknowledgement = scheduler.schedule(existing)
    except Exception:
        ambiguous = _state(existing, RetryCommandState.SCHEDULING_AMBIGUOUS)
        try:
            persisted = store.save(ambiguous)
        except Exception:
            return RetryOrchestrationResult(
                command=existing,
                scheduled=False,
                failure="state_persistence_failed",
            )
        return RetryOrchestrationResult(
            command=persisted,
            scheduled=False,
            failure="scheduler_call_ambiguous",
        )

    if acknowledgement.command_id != existing.command_id:
        ambiguous = _state(existing, RetryCommandState.SCHEDULING_AMBIGUOUS, acknowledgement.scheduling_id)
        persisted, failure = _try_persist_state(store, ambiguous)
        return RetryOrchestrationResult(
            command=persisted,
            scheduled=False,
            failure=failure or "scheduler_command_mismatch",
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
            try:
                persisted = store.save(ambiguous)
            except Exception:
                return RetryOrchestrationResult(
                    command=existing,
                    scheduled=False,
                    failure="state_persistence_failed",
                )
            return RetryOrchestrationResult(
                command=persisted,
                scheduled=False,
                failure="scheduler_acknowledgement_persistence_ambiguous",
            )
        return RetryOrchestrationResult(command=scheduled, scheduled=True)

    if acknowledgement.status is SchedulerAcknowledgementStatus.REJECTED:
        rejected = _state(existing, RetryCommandState.REQUIRES_MANUAL_REVIEW, acknowledgement.scheduling_id)
        try:
            persisted = store.save(rejected)
        except Exception:
            return RetryOrchestrationResult(
                command=existing,
                scheduled=False,
                failure="state_persistence_failed",
            )
        return RetryOrchestrationResult(command=persisted, scheduled=False, failure="scheduler_rejected")

    ambiguous = _state(existing, RetryCommandState.SCHEDULING_AMBIGUOUS, acknowledgement.scheduling_id)
    persisted, failure = _try_persist_state(store, ambiguous)
    return RetryOrchestrationResult(command=persisted, scheduled=False, failure=failure or "scheduler_acknowledgement_ambiguous")


def _try_persist_state(store: RetryCommandStore, command: RetryCommand) -> tuple[RetryCommand, str | None]:
    try:
        return store.save(command), None
    except Exception:
        return command, "state_persistence_failed"


def _state(
    command: RetryCommand,
    state: RetryCommandState,
    scheduling_id: str | None = None,
) -> RetryCommand:
    return command.transition_to(
        state,
        scheduling_id=scheduling_id,
    )
