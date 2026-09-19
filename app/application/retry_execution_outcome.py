from dataclasses import dataclass
from typing import Protocol

from app.domain.execution_outcome import ExecutionOutcome, ExecutionOutcomeStatus
from app.domain.execution_retry import RetryCommand, RetryCommandState


@dataclass(frozen=True)
class RetryExecutionOutcomeResult:
    command: RetryCommand
    outcome: ExecutionOutcome
    recorded: bool
    failure: str | None = None


class RetryExecutionOutcomeStore(Protocol):
    def save(self, command: RetryCommand) -> RetryCommand:
        ...


def record_retry_execution_outcome(*, command: RetryCommand, outcome: ExecutionOutcome, store: RetryExecutionOutcomeStore) -> RetryExecutionOutcomeResult:
    if command.state is not RetryCommandState.EXECUTION_IN_PROGRESS:
        return RetryExecutionOutcomeResult(command=command, outcome=outcome, recorded=False, failure="command_not_in_execution")
    if outcome.request_id != command.request_id or outcome.idempotency_key != command.idempotency_key:
        return RetryExecutionOutcomeResult(command=command, outcome=outcome, recorded=False, failure="outcome_identity_mismatch")
    target = RetryCommandState.COMPLETED if outcome.status is ExecutionOutcomeStatus.SUCCEEDED else RetryCommandState.REQUIRES_MANUAL_REVIEW
    try:
        updated = command.transition_to(target)
        persisted = store.save(updated)
    except Exception:
        return RetryExecutionOutcomeResult(command=command, outcome=outcome, recorded=False, failure="outcome_persistence_failed")
    return RetryExecutionOutcomeResult(command=persisted, outcome=outcome, recorded=True)
