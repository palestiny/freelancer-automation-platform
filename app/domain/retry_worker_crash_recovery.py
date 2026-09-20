from dataclasses import dataclass
from enum import Enum

from .execution_attempt_history import ExecutionAttemptHistory
from .execution_outcome import ExecutionOutcomeStatus
from .execution_retry import RetryCommand, RetryCommandState


class CrashRecoveryDisposition(str, Enum):
    REQUIRES_MANUAL_RECONCILIATION = "requires_manual_reconciliation"
    SAFE_TO_RELEASE_FOR_REVIEW = "safe_to_release_for_review"


class CrashRecoveryReason(str, Enum):
    AMBIGUOUS_IN_FLIGHT = "ambiguous_in_flight"
    ALREADY_TERMINAL = "already_terminal"
    DUPLICATE_RECONCILIATION = "duplicate_reconciliation"
    IDENTITY_MISMATCH = "identity_mismatch"
    MISSING_ATTEMPT_HISTORY = "missing_attempt_history"
    NOT_IN_FLIGHT = "not_in_flight"


@dataclass(frozen=True)
class CrashRecoveryResult:
    command_id: str
    request_id: str
    idempotency_key: str
    attempt_number: int
    disposition: CrashRecoveryDisposition
    reason: CrashRecoveryReason
    reexecute: bool

    def __post_init__(self) -> None:
        for name in ("command_id", "request_id", "idempotency_key"):
            if not getattr(self, name).strip():
                raise ValueError(f"{name} cannot be empty")
        if self.attempt_number <= 0:
            raise ValueError("attempt_number must be greater than zero")
        if self.reexecute:
            raise ValueError("crash reconciliation cannot authorize re-execution")
        expected = {
            CrashRecoveryReason.AMBIGUOUS_IN_FLIGHT: CrashRecoveryDisposition.REQUIRES_MANUAL_RECONCILIATION,
            CrashRecoveryReason.IDENTITY_MISMATCH: CrashRecoveryDisposition.REQUIRES_MANUAL_RECONCILIATION,
            CrashRecoveryReason.MISSING_ATTEMPT_HISTORY: CrashRecoveryDisposition.REQUIRES_MANUAL_RECONCILIATION,
            CrashRecoveryReason.ALREADY_TERMINAL: CrashRecoveryDisposition.SAFE_TO_RELEASE_FOR_REVIEW,
            CrashRecoveryReason.DUPLICATE_RECONCILIATION: CrashRecoveryDisposition.SAFE_TO_RELEASE_FOR_REVIEW,
            CrashRecoveryReason.NOT_IN_FLIGHT: CrashRecoveryDisposition.SAFE_TO_RELEASE_FOR_REVIEW,
        }[self.reason]
        if self.disposition is not expected:
            raise ValueError("disposition must match reason")


def reconcile_crashed_retry_command(
    *,
    command: RetryCommand,
    history: ExecutionAttemptHistory,
    reconciled_command_ids: frozenset[str] = frozenset(),
) -> CrashRecoveryResult:
    if command.command_id in reconciled_command_ids:
        return _result(command, CrashRecoveryDisposition.SAFE_TO_RELEASE_FOR_REVIEW, CrashRecoveryReason.DUPLICATE_RECONCILIATION)

    if command.request_id != history.request_id or command.idempotency_key != history.idempotency_key:
        return _result(command, CrashRecoveryDisposition.REQUIRES_MANUAL_RECONCILIATION, CrashRecoveryReason.IDENTITY_MISMATCH)

    if command.state in {
        RetryCommandState.COMPLETED,
        RetryCommandState.REJECTED_STALE,
        RetryCommandState.REQUIRES_MANUAL_REVIEW,
    }:
        return _result(command, CrashRecoveryDisposition.SAFE_TO_RELEASE_FOR_REVIEW, CrashRecoveryReason.ALREADY_TERMINAL)

    if command.state is not RetryCommandState.EXECUTION_IN_PROGRESS:
        return _result(command, CrashRecoveryDisposition.SAFE_TO_RELEASE_FOR_REVIEW, CrashRecoveryReason.NOT_IN_FLIGHT)

    if history.latest_attempt is None:
        return _result(command, CrashRecoveryDisposition.REQUIRES_MANUAL_RECONCILIATION, CrashRecoveryReason.MISSING_ATTEMPT_HISTORY)

    latest = history.latest_attempt
    if latest.attempt_number != command.attempt_number:
        return _result(command, CrashRecoveryDisposition.REQUIRES_MANUAL_RECONCILIATION, CrashRecoveryReason.IDENTITY_MISMATCH)

    if latest.status is not ExecutionOutcomeStatus.UNKNOWN:
        return _result(command, CrashRecoveryDisposition.REQUIRES_MANUAL_RECONCILIATION, CrashRecoveryReason.AMBIGUOUS_IN_FLIGHT)

    return _result(command, CrashRecoveryDisposition.REQUIRES_MANUAL_RECONCILIATION, CrashRecoveryReason.AMBIGUOUS_IN_FLIGHT)


def _result(command, disposition, reason):
    return CrashRecoveryResult(
        command_id=command.command_id,
        request_id=command.request_id,
        idempotency_key=command.idempotency_key,
        attempt_number=command.attempt_number,
        disposition=disposition,
        reason=reason,
        reexecute=False,
    )
