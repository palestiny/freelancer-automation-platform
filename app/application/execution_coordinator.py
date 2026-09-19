from dataclasses import dataclass

from .execution_port import ExecutionPort, dispatch_execution
from app.domain.authorized_execution_request import AuthorizedExecutionRequest
from app.domain.execution_outcome import ExecutionOutcome
from app.domain.execution_outcome_policy import ExecutionOutcomePolicy, assess_execution_outcome
from app.domain.execution_recovery import ExecutionRecoveryHandoff, derive_execution_recovery


@dataclass(frozen=True)
class ExecutionCoordinationResult:
    outcome: ExecutionOutcome
    policy_assessment: object
    recovery_handoff: ExecutionRecoveryHandoff


def coordinate_execution(
    *,
    port: ExecutionPort,
    request: AuthorizedExecutionRequest,
    policy: ExecutionOutcomePolicy,
    attempt_number: int,
) -> ExecutionCoordinationResult:
    outcome = dispatch_execution(port=port, request=request)
    assessment = assess_execution_outcome(
        outcome=outcome,
        policy=policy,
        attempt_number=attempt_number,
    )
    recovery = derive_execution_recovery(
        outcome=outcome,
        policy_assessment=assessment,
    )
    return ExecutionCoordinationResult(
        outcome=outcome,
        policy_assessment=assessment,
        recovery_handoff=recovery,
    )
