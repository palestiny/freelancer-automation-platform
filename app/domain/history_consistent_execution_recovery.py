from dataclasses import dataclass

from .execution_attempt_history import ExecutionAttemptHistory
from .execution_history_consistency import (
    ExecutionHistoryConsistencyStatus,
    assess_execution_history_consistency,
)
from .execution_outcome import ExecutionOutcome
from .execution_outcome_policy import ExecutionOutcomePolicy, assess_execution_outcome
from .execution_recovery import (
    ExecutionRecoveryHandoff,
    create_execution_recovery_handoff,
)


@dataclass(frozen=True)
class HistoryConsistentRecoveryHandoff:
    handoff: ExecutionRecoveryHandoff | None
    consistency_status: ExecutionHistoryConsistencyStatus


def create_execution_recovery_handoff_with_history(
    *,
    outcome: ExecutionOutcome,
    history: ExecutionAttemptHistory,
    policy: ExecutionOutcomePolicy,
) -> HistoryConsistentRecoveryHandoff:
    consistency = assess_execution_history_consistency(
        outcome=outcome,
        history=history,
    )
    if consistency.status is not ExecutionHistoryConsistencyStatus.CONSISTENT:
        return HistoryConsistentRecoveryHandoff(
            handoff=None,
            consistency_status=consistency.status,
        )

    assessment = assess_execution_outcome(
        outcome=outcome,
        attempt_count=consistency.attempt_count,
        policy=policy,
    )
    return HistoryConsistentRecoveryHandoff(
        handoff=create_execution_recovery_handoff(assessment=assessment),
        consistency_status=consistency.status,
    )
