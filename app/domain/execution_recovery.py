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


@dataclass(frozen=True)
class ExecutionRecoveryHandoff:
    request_id: str
    idempotency_key: str
    attempt_count: int
    mode: ExecutionRecoveryMode
    source_status: ExecutionOutcomeAssessmentStatus

    def __post_init__(self) -> None:
        if not self.request_id.strip() or not self.idempotency_key.strip():
            raise ValueError("request_id and idempotency_key cannot be empty")
        if self.attempt_count <= 0:
            raise ValueError("attempt_count must be greater than zero")


def create_execution_recovery_handoff(
    *,
    assessment: ExecutionOutcomeAssessment,
) -> ExecutionRecoveryHandoff:
    if assessment.status is ExecutionOutcomeAssessmentStatus.RETRY_ELIGIBLE:
        mode = ExecutionRecoveryMode.RETRY
    elif assessment.status is ExecutionOutcomeAssessmentStatus.MANUAL_REVIEW_REQUIRED:
        mode = ExecutionRecoveryMode.MANUAL_REVIEW
    else:
        mode = ExecutionRecoveryMode.NONE

    return ExecutionRecoveryHandoff(
        request_id=assessment.request_id,
        idempotency_key=assessment.idempotency_key,
        attempt_count=assessment.attempt_count,
        mode=mode,
        source_status=assessment.status,
    )
