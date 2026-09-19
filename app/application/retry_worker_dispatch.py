from dataclasses import dataclass
from enum import Enum
from typing import Protocol

from app.application.execution_port import ExecutionPort, dispatch_execution
from app.application.retry_execution_handoff import (
    RetryExecutionClaimStore,
    claim_retry_for_execution,
)
from app.application.retry_execution_outcome import record_retry_execution_outcome
from app.domain.authorized_execution_request import AuthorizedExecutionRequest
from app.domain.execution_outcome import ExecutionOutcome
from app.domain.execution_retry import RetryCommand, RetryCommandState


class RetryWorkerDispatchStatus(str, Enum):
    COMPLETED = "completed"
    REQUIRES_MANUAL_REVIEW = "requires_manual_review"
    REJECTED_STALE = "rejected_stale"
    CLAIM_NOT_ACQUIRED = "claim_not_acquired"
    REVALIDATION_FAILURE = "revalidation_failure"
    PROVIDER_FAILURE = "provider_failure"
    OUTCOME_PERSISTENCE_FAILURE = "outcome_persistence_failure"


@dataclass(frozen=True)
class RetryWorkerDispatchResult:
    command: RetryCommand
    status: RetryWorkerDispatchStatus
    outcome: ExecutionOutcome | None = None
    failure: str | None = None


class RetryAuthorizationRevalidator(Protocol):
    def revalidate(self, command: RetryCommand) -> AuthorizedExecutionRequest | None:
        ...


class RetryWorkerDispatchStore(RetryExecutionClaimStore, Protocol):
    def save(self, command: RetryCommand) -> RetryCommand:
        ...


def dispatch_one_retry(
    *,
    command: RetryCommand,
    store: RetryWorkerDispatchStore,
    revalidator: RetryAuthorizationRevalidator,
    provider: ExecutionPort,
) -> RetryWorkerDispatchResult:
    claim = claim_retry_for_execution(command=command, store=store)
    if not claim.claimed or claim.handoff is None:
        return RetryWorkerDispatchResult(
            command=claim.command,
            status=RetryWorkerDispatchStatus.CLAIM_NOT_ACQUIRED,
            failure=claim.failure,
        )

    claimed = claim.command

    try:
        request = revalidator.revalidate(claimed)
    except Exception:
        return _manual_review(
            command=claimed,
            store=store,
            status=RetryWorkerDispatchStatus.REVALIDATION_FAILURE,
            failure="authorization_revalidation_failed",
        )

    if request is None or not _matches_command(request, claimed):
        return _reject_stale(command=claimed, store=store)

    try:
        outcome = dispatch_execution(port=provider, request=request)
    except Exception:
        return RetryWorkerDispatchResult(
            command=claimed,
            status=RetryWorkerDispatchStatus.PROVIDER_FAILURE,
            failure="provider_execution_failed",
        )

    recorded = record_retry_execution_outcome(
        command=claimed,
        outcome=outcome,
        store=store,
    )
    if not recorded.recorded:
        return RetryWorkerDispatchResult(
            command=claimed,
            status=RetryWorkerDispatchStatus.OUTCOME_PERSISTENCE_FAILURE,
            outcome=outcome,
            failure=recorded.failure,
        )

    if recorded.command.state is RetryCommandState.COMPLETED:
        status = RetryWorkerDispatchStatus.COMPLETED
    else:
        status = RetryWorkerDispatchStatus.REQUIRES_MANUAL_REVIEW

    return RetryWorkerDispatchResult(
        command=recorded.command,
        status=status,
        outcome=outcome,
    )


def _matches_command(
    request: AuthorizedExecutionRequest,
    command: RetryCommand,
) -> bool:
    return (
        request.request_id == command.request_id
        and request.idempotency_key == command.idempotency_key
        and request.policy_id == command.authorization_policy_id
        and request.policy_version == command.authorization_policy_version
        and request.autonomy_level.name == command.autonomy_bound
    )


def _reject_stale(
    *,
    command: RetryCommand,
    store: RetryWorkerDispatchStore,
) -> RetryWorkerDispatchResult:
    try:
        updated = store.save(command.transition_to(RetryCommandState.REJECTED_STALE))
    except Exception:
        return RetryWorkerDispatchResult(
            command=command,
            status=RetryWorkerDispatchStatus.REVALIDATION_FAILURE,
            failure="stale_rejection_persistence_failed",
        )
    return RetryWorkerDispatchResult(
        command=updated,
        status=RetryWorkerDispatchStatus.REJECTED_STALE,
        failure="authorization_context_stale",
    )


def _manual_review(
    *,
    command: RetryCommand,
    store: RetryWorkerDispatchStore,
    status: RetryWorkerDispatchStatus,
    failure: str,
) -> RetryWorkerDispatchResult:
    try:
        updated = store.save(command.transition_to(RetryCommandState.REQUIRES_MANUAL_REVIEW))
    except Exception:
        return RetryWorkerDispatchResult(
            command=command,
            status=status,
            failure="manual_review_persistence_failed",
        )
    return RetryWorkerDispatchResult(
        command=updated,
        status=status,
        failure=failure,
    )
