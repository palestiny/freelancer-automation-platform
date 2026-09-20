from dataclasses import dataclass
from enum import Enum

from app.application.execution_status_port import ProviderExecutionStatusResult
from app.domain.execution_outcome import ExecutionOutcomeStatus
from app.domain.execution_retry import RetryCommand, RetryCommandState


class RetryRecoveryAssessmentStatus(str, Enum):
    CONFIRMED_COMPLETED = "confirmed_completed"
    CONFIRMED_FAILURE_REQUIRES_REVIEW = "confirmed_failure_requires_review"
    REMAINS_AMBIGUOUS = "remains_ambiguous"
    NO_RECONCILIATION_REQUIRED = "no_reconciliation_required"


@dataclass(frozen=True)
class RetryRecoveryAssessment:
    status: RetryRecoveryAssessmentStatus
    target_state: RetryCommandState | None


def assess_retry_status_reconciliation(
    *,
    command: RetryCommand,
    provider_status: ProviderExecutionStatusResult,
) -> RetryRecoveryAssessment:
    if provider_status.request_id != command.request_id:
        raise ValueError("provider status request_id does not match retry command")
    if provider_status.idempotency_key != command.idempotency_key:
        raise ValueError("provider status idempotency_key does not match retry command")

    if command.state in {
        RetryCommandState.COMPLETED,
        RetryCommandState.REJECTED_STALE,
        RetryCommandState.REQUIRES_MANUAL_REVIEW,
        RetryCommandState.CLAIM_CONFLICT,
    }:
        return RetryRecoveryAssessment(
            status=RetryRecoveryAssessmentStatus.NO_RECONCILIATION_REQUIRED,
            target_state=None,
        )

    if command.state is not RetryCommandState.EXECUTION_IN_PROGRESS:
        return RetryRecoveryAssessment(
            status=RetryRecoveryAssessmentStatus.NO_RECONCILIATION_REQUIRED,
            target_state=None,
        )

    if provider_status.status is ExecutionOutcomeStatus.SUCCEEDED:
        return RetryRecoveryAssessment(
            status=RetryRecoveryAssessmentStatus.CONFIRMED_COMPLETED,
            target_state=RetryCommandState.COMPLETED,
        )

    if provider_status.status in {
        ExecutionOutcomeStatus.FAILED,
        ExecutionOutcomeStatus.REJECTED,
    }:
        return RetryRecoveryAssessment(
            status=RetryRecoveryAssessmentStatus.CONFIRMED_FAILURE_REQUIRES_REVIEW,
            target_state=RetryCommandState.REQUIRES_MANUAL_REVIEW,
        )

    return RetryRecoveryAssessment(
        status=RetryRecoveryAssessmentStatus.REMAINS_AMBIGUOUS,
        target_state=None,
    )
