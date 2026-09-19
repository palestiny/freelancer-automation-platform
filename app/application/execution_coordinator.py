from dataclasses import dataclass

from .execution_port import ExecutionPort, dispatch_execution
from app.domain.authorized_execution_request import AuthorizedExecutionRequest
from app.domain.execution_outcome import ExecutionOutcome
from app.domain.execution_outcome_policy import (
    ExecutionOutcomeAssessment,
    ExecutionOutcomePolicy,
    assess_execution_outcome,
)
from app.domain.execution_recovery import (
    ExecutionRecoveryHandoff,
    create_execution_recovery_handoff,
)


@dataclass(frozen=True)
class ExecutionCoordinationResult:
    outcome: ExecutionOutcome
    policy_assessment: ExecutionOutcomeAssessment
    recovery_handoff: ExecutionRecoveryHandoff


def coordinate_execution(
    *,
    port: ExecutionPort,
    request: AuthorizedExecutionRequest,
    policy: ExecutionOutcomePolicy,
    attempt_count: int,
) -> ExecutionCoordinationResult:
    if not isinstance(attempt_count, int) or isinstance(attempt_count, bool):
        raise TypeError("attempt_count must be an integer")
    if attempt_count <= 0:
        raise ValueError("attempt_count must be greater than zero")

    outcome = dispatch_execution(port=port, request=request)
    assessment = assess_execution_outcome(
        outcome=outcome,
        policy=policy,
        attempt_count=attempt_count,
    )
    recovery = create_execution_recovery_handoff(
        assessment=assessment,
    )
    return ExecutionCoordinationResult(
        outcome=outcome,
        policy_assessment=assessment,
        recovery_handoff=recovery,
    )
