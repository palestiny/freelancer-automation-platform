from dataclasses import dataclass
from enum import Enum
from typing import Protocol

from .execution_coordinator import ExecutionCoordinationResult, coordinate_execution
from .execution_port import ExecutionPort, dispatch_execution
from app.domain.authorized_execution_request import AuthorizedExecutionRequest
from app.domain.execution_outcome import ExecutionOutcome
from app.domain.execution_outcome_policy import ExecutionOutcomePolicy


class ExecutionOutcomeRecorder(Protocol):
    def save(self, outcome: ExecutionOutcome) -> None:
        ...


class PersistedExecutionCoordinationStatus(str, Enum):
    COMPLETED = "completed"
    PROVIDER_FAILURE = "provider_failure"
    OUTCOME_PERSISTENCE_FAILURE = "outcome_persistence_failure"


@dataclass(frozen=True)
class PersistedExecutionCoordinationResult:
    status: PersistedExecutionCoordinationStatus
    outcome: ExecutionOutcome | None
    coordination: ExecutionCoordinationResult | None
    failure: str | None = None


def coordinate_persisted_execution(
    *,
    port: ExecutionPort,
    request: AuthorizedExecutionRequest,
    policy: ExecutionOutcomePolicy,
    attempt_count: int,
    outcome_repository: ExecutionOutcomeRecorder,
) -> PersistedExecutionCoordinationResult:
    try:
        outcome = dispatch_execution(port=port, request=request)
    except Exception:
        return PersistedExecutionCoordinationResult(
            status=PersistedExecutionCoordinationStatus.PROVIDER_FAILURE,
            outcome=None,
            coordination=None,
            failure="provider_execution_failed",
        )

    try:
        outcome_repository.save(outcome)
    except Exception:
        return PersistedExecutionCoordinationResult(
            status=PersistedExecutionCoordinationStatus.OUTCOME_PERSISTENCE_FAILURE,
            outcome=outcome,
            coordination=None,
            failure="outcome_persistence_failed",
        )

    coordination = coordinate_execution(
        port=_AlreadyExecutedPort(outcome),
        request=request,
        policy=policy,
        attempt_count=attempt_count,
    )
    return PersistedExecutionCoordinationResult(
        status=PersistedExecutionCoordinationStatus.COMPLETED,
        outcome=outcome,
        coordination=coordination,
    )


class _AlreadyExecutedPort(ExecutionPort):
    def __init__(self, outcome: ExecutionOutcome) -> None:
        self._outcome = outcome

    def execute(self, request):
        return self._outcome
