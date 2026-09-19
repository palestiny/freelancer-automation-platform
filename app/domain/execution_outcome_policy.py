from dataclasses import dataclass
from enum import Enum

from .execution_outcome import ExecutionOutcome, ExecutionOutcomeStatus


class ExecutionOutcomeAssessmentStatus(str, Enum):
    ACCEPTED = "accepted"
    RETRY_ELIGIBLE = "retry_eligible"
    MANUAL_REVIEW_REQUIRED = "manual_review_required"
    TERMINAL_FAILURE = "terminal_failure"


@dataclass(frozen=True)
class ExecutionOutcomePolicy:
    retryable_outcome_codes: tuple[str, ...] = ()
    maximum_attempts: int = 1

    def __post_init__(self) -> None:
        if self.maximum_attempts <= 0:
            raise ValueError("maximum_attempts must be greater than zero")
        if len(set(self.retryable_outcome_codes)) != len(self.retryable_outcome_codes):
            raise ValueError("retryable_outcome_codes must be unique")
        if any(not code.strip() for code in self.retryable_outcome_codes):
            raise ValueError("retryable_outcome_codes cannot contain empty values")


@dataclass(frozen=True)
class ExecutionOutcomeAssessment:
    request_id: str
    idempotency_key: str
    outcome_status: ExecutionOutcomeStatus
    outcome_code: str
    attempt_count: int
    status: ExecutionOutcomeAssessmentStatus

    def __post_init__(self) -> None:
        if not self.request_id.strip() or not self.idempotency_key.strip():
            raise ValueError("request_id and idempotency_key cannot be empty")
        if not self.outcome_code.strip():
            raise ValueError("outcome_code cannot be empty")
        if self.attempt_count <= 0:
            raise ValueError("attempt_count must be greater than zero")


def assess_execution_outcome(
    *,
    outcome: ExecutionOutcome,
    attempt_count: int,
    policy: ExecutionOutcomePolicy,
) -> ExecutionOutcomeAssessment:
    if not isinstance(attempt_count, int) or isinstance(attempt_count, bool):
        raise TypeError("attempt_count must be an integer")
    if attempt_count <= 0:
        raise ValueError("attempt_count must be greater than zero")

    if outcome.status is ExecutionOutcomeStatus.SUCCEEDED:
        status = ExecutionOutcomeAssessmentStatus.ACCEPTED
    elif outcome.status is ExecutionOutcomeStatus.UNKNOWN:
        status = ExecutionOutcomeAssessmentStatus.MANUAL_REVIEW_REQUIRED
    elif outcome.status is ExecutionOutcomeStatus.REJECTED:
        status = ExecutionOutcomeAssessmentStatus.TERMINAL_FAILURE
    elif (
        outcome.status is ExecutionOutcomeStatus.FAILED
        and outcome.outcome_code in policy.retryable_outcome_codes
        and attempt_count < policy.maximum_attempts
    ):
        status = ExecutionOutcomeAssessmentStatus.RETRY_ELIGIBLE
    else:
        status = ExecutionOutcomeAssessmentStatus.TERMINAL_FAILURE

    return ExecutionOutcomeAssessment(
        request_id=outcome.request_id,
        idempotency_key=outcome.idempotency_key,
        outcome_status=outcome.status,
        outcome_code=outcome.outcome_code,
        attempt_count=attempt_count,
        status=status,
    )
