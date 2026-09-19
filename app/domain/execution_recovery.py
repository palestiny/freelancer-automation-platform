from dataclasses import dataclass
from enum import Enum

from .execution_outcome_policy import (
    ExecutionOutcomeAssessment,
    ExecutionOutcomeAssessmentStatus,
)


class ExecutionRecoveryMode(str, Enum):
    RETRY = "retry"
    MANUAL_REVIEW = "manual_review"
    NONE = "none"


class ExecutionRecoveryReason(str, Enum):
    RETRY_ELIGIBLE = "retry_eligible"
    MANUAL_REVIEW_REQUIRED = "manual_review_required"
    NO_RECOVERY_REQUIRED = "no_recovery_required"


@dataclass(frozen=True)
class ExecutionRecoveryHandoff:
    request_id: str
    idempotency_key: str
    attempt_count: int
    mode: ExecutionRecoveryMode
    reason: ExecutionRecoveryReason
    source_status: ExecutionOutcomeAssessmentStatus

    def __post_init__(self) -> None:
        if not self.request_id.strip() or not self.idempotency_key.strip():
            raise ValueError("request_id and idempotency_key cannot be empty")
        if self.attempt_count <= 0:
            raise ValueError("attempt_count must be greater than zero")
        expected_reason = {
            ExecutionRecoveryMode.RETRY: ExecutionRecoveryReason.RETRY_ELIGIBLE,
            ExecutionRecoveryMode.MANUAL_REVIEW: ExecutionRecoveryReason.MANUAL_REVIEW_REQUIRED,
            ExecutionRecoveryMode.NONE: ExecutionRecoveryReason.NO_RECOVERY_REQUIRED,
        }[self.mode]
        if self.reason is not expected_reason:
            raise ValueError("reason must match recovery mode")
        expected_statuses = {
            ExecutionRecoveryMode.RETRY: {ExecutionOutcomeAssessmentStatus.RETRY_ELIGIBLE},
            ExecutionRecoveryMode.MANUAL_REVIEW: {ExecutionOutcomeAssessmentStatus.MANUAL_REVIEW_REQUIRED},
            ExecutionRecoveryMode.NONE: {ExecutionOutcomeAssessmentStatus.ACCEPTED, ExecutionOutcomeAssessmentStatus.TERMINAL_FAILURE},
        }[self.mode]
        if self.source_status not in expected_statuses:
            raise ValueError("source_status must match recovery mode")


def create_execution_recovery_handoff(
    *,
    assessment: ExecutionOutcomeAssessment,
) -> ExecutionRecoveryHandoff:
    if assessment.status is ExecutionOutcomeAssessmentStatus.RETRY_ELIGIBLE:
        mode = ExecutionRecoveryMode.RETRY
        reason = ExecutionRecoveryReason.RETRY_ELIGIBLE
    elif assessment.status is ExecutionOutcomeAssessmentStatus.MANUAL_REVIEW_REQUIRED:
        mode = ExecutionRecoveryMode.MANUAL_REVIEW
        reason = ExecutionRecoveryReason.MANUAL_REVIEW_REQUIRED
    else:
        mode = ExecutionRecoveryMode.NONE
        reason = ExecutionRecoveryReason.NO_RECOVERY_REQUIRED

    return ExecutionRecoveryHandoff(
        request_id=assessment.request_id,
        idempotency_key=assessment.idempotency_key,
        attempt_count=assessment.attempt_count,
        mode=mode,
        reason=reason,
        source_status=assessment.status,
    )
