from app.domain.execution_retry import RetryCommandState
from app.domain.retry_status_reconciliation import (
    RetryRecoveryAssessment,
    RetryRecoveryAssessmentStatus,
)


class RetryStatusAssessmentApplication:
    def __init__(self, store):
        self._store = store

    def apply(
        self,
        *,
        command_id: str,
        assessment: RetryRecoveryAssessment,
        expected_state: RetryCommandState,
    ):
        if assessment.status in {
            RetryRecoveryAssessmentStatus.REMAINS_AMBIGUOUS,
            RetryRecoveryAssessmentStatus.NO_RECONCILIATION_REQUIRED,
        }:
            command = self._store.get(command_id)
            if command is None:
                raise KeyError(command_id)
            return command

        if assessment.target_state is None:
            raise ValueError("mutating assessment requires a target state")

        updated = self._store.transition_if_current(
            command_id,
            expected_state,
            assessment.target_state,
        )
        if updated is None:
            raise RuntimeError("retry command state changed before assessment application")
        return updated
