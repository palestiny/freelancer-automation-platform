from dataclasses import dataclass

from .execution_coordinator import ExecutionCoordinationResult
from .execution_port import ExecutionPort, dispatch_execution
from app.domain.authorized_execution_request import AuthorizedExecutionRequest
from app.domain.execution_attempt_history import ExecutionAttempt, ExecutionAttemptHistory
from app.domain.execution_outcome_policy import ExecutionOutcomePolicy
from app.domain.execution_policy_history import assess_execution_outcome_with_history


@dataclass(frozen=True)
class HistoryAwareExecutionCoordinationResult:
    outcome: object
    history: ExecutionAttemptHistory
    policy_assessment: object
    recovery_handoff: object


def coordinate_execution_with_history(
    *,
    port: ExecutionPort,
    request: AuthorizedExecutionRequest,
    history: ExecutionAttemptHistory,
    policy: ExecutionOutcomePolicy,
) -> HistoryAwareExecutionCoordinationResult:
    if request.request_id != history.request_id or request.idempotency_key != history.idempotency_key:
        raise ValueError("execution request identity does not match attempt history")

    outcome = dispatch_execution(port=port, request=request)
    next_attempt_number = (history.latest_attempt.attempt_number + 1) if history.latest_attempt else 1
    attempt = ExecutionAttempt(
        request_id=outcome.request_id,
        idempotency_key=outcome.idempotency_key,
        attempt_number=next_attempt_number,
        status=outcome.status,
        outcome_code=outcome.outcome_code,
        observed_at=outcome.observed_at,
        external_reference=outcome.external_reference,
    )
    updated_history = history.append(attempt)
    policy_history = assess_execution_outcome_with_history(
        outcome=outcome,
        history=updated_history,
        policy=policy,
    )
    if policy_history.assessment is None:
        raise ValueError("execution outcome history is inconsistent")
    from app.domain.execution_recovery import create_execution_recovery_handoff
    return HistoryAwareExecutionCoordinationResult(
        outcome=outcome,
        history=updated_history,
        policy_assessment=policy_history.assessment,
        recovery_handoff=create_execution_recovery_handoff(assessment=policy_history.assessment),
    )
