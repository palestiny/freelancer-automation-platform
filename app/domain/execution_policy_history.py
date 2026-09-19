from dataclasses import dataclass

from .execution_attempt_history import ExecutionAttemptHistory
from .execution_history_consistency import (
    ExecutionHistoryConsistencyStatus,
    assess_execution_history_consistency,
)
from .execution_outcome import ExecutionOutcome
from .execution_outcome_policy import (
    ExecutionOutcomeAssessment,
    ExecutionOutcomePolicy,
    assess_execution_outcome,
)


@dataclass(frozen=True)
class ExecutionPolicyHistoryAssessment:
    assessment: ExecutionOutcomeAssessment | None
    consistency_status: ExecutionHistoryConsistencyStatus


def assess_execution_outcome_with_history(
    *,
    outcome: ExecutionOutcome,
    history: ExecutionAttemptHistory,
    policy: ExecutionOutcomePolicy,
) -> ExecutionPolicyHistoryAssessment:
    consistency = assess_execution_history_consistency(
        outcome=outcome,
        history=history,
    )
    if consistency.status is not ExecutionHistoryConsistencyStatus.CONSISTENT:
        return ExecutionPolicyHistoryAssessment(
            assessment=None,
            consistency_status=consistency.status,
        )

    return ExecutionPolicyHistoryAssessment(
        assessment=assess_execution_outcome(
            outcome=outcome,
            attempt_count=consistency.attempt_count,
            policy=policy,
        ),
        consistency_status=consistency.status,
    )
