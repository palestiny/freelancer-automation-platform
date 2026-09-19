from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Protocol


class RetryCommandAction(str, Enum):
    RETRY = "retry"
    MANUAL_REVIEW = "manual_review"


class RetryCommandState(str, Enum):
    CREATED = "created"
    SCHEDULED = "scheduled"
    CLAIMED = "claimed"
    REVALIDATION_REQUIRED = "revalidation_required"
    EXECUTION_IN_PROGRESS = "execution_in_progress"
    COMPLETED = "completed"
    REJECTED_STALE = "rejected_stale"
    REQUIRES_MANUAL_REVIEW = "requires_manual_review"
    SCHEDULING_AMBIGUOUS = "scheduling_ambiguous"
    CLAIM_CONFLICT = "claim_conflict"


class SchedulerAcknowledgementStatus(str, Enum):
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    AMBIGUOUS = "ambiguous"


@dataclass(frozen=True)
class RetryCommand:
    command_id: str
    request_id: str
    idempotency_key: str
    attempt_number: int
    action: RetryCommandAction
    authorization_policy_id: str
    authorization_policy_version: str
    autonomy_bound: str
    created_at: datetime
    state: RetryCommandState = RetryCommandState.CREATED
    scheduling_id: str | None = None

    def __post_init__(self) -> None:
        for name in (
            "command_id",
            "request_id",
            "idempotency_key",
            "authorization_policy_id",
            "authorization_policy_version",
            "autonomy_bound",
        ):
            if not getattr(self, name).strip():
                raise ValueError(f"{name} cannot be empty")
        if self.attempt_number <= 0:
            raise ValueError("attempt_number must be greater than zero")
        if self.created_at.tzinfo is None or self.created_at.utcoffset() is None:
            raise ValueError("created_at must be timezone-aware")
        if self.scheduling_id is not None and not self.scheduling_id.strip():
            raise ValueError("scheduling_id cannot be empty")

    def can_transition_to(self, target: RetryCommandState) -> bool:
        allowed = {
            RetryCommandState.CREATED: {RetryCommandState.CLAIMED, RetryCommandState.REQUIRES_MANUAL_REVIEW, RetryCommandState.SCHEDULING_AMBIGUOUS},
            RetryCommandState.CLAIMED: {RetryCommandState.SCHEDULED, RetryCommandState.REQUIRES_MANUAL_REVIEW, RetryCommandState.SCHEDULING_AMBIGUOUS},
            RetryCommandState.SCHEDULED: {RetryCommandState.EXECUTION_IN_PROGRESS, RetryCommandState.REQUIRES_MANUAL_REVIEW, RetryCommandState.REJECTED_STALE, RetryCommandState.SCHEDULING_AMBIGUOUS},
            RetryCommandState.EXECUTION_IN_PROGRESS: {RetryCommandState.COMPLETED, RetryCommandState.REQUIRES_MANUAL_REVIEW},
            RetryCommandState.SCHEDULING_AMBIGUOUS: {RetryCommandState.SCHEDULED, RetryCommandState.REQUIRES_MANUAL_REVIEW},
            RetryCommandState.REQUIRES_MANUAL_REVIEW: set(),
            RetryCommandState.REJECTED_STALE: set(),
            RetryCommandState.COMPLETED: set(),
            RetryCommandState.CLAIM_CONFLICT: set(),
            RetryCommandState.REVALIDATION_REQUIRED: set(),
        }
        return target in allowed[self.state]

    def transition_to(self, target: RetryCommandState, scheduling_id: str | None = None) -> "RetryCommand":
        if not self.can_transition_to(target):
            raise ValueError(f"invalid retry command transition: {self.state.value} -> {target.value}")
        return RetryCommand(
            command_id=self.command_id, request_id=self.request_id, idempotency_key=self.idempotency_key,
            attempt_number=self.attempt_number, action=self.action,
            authorization_policy_id=self.authorization_policy_id,
            authorization_policy_version=self.authorization_policy_version,
            autonomy_bound=self.autonomy_bound, created_at=self.created_at, state=target,
            scheduling_id=self.scheduling_id if scheduling_id is None else scheduling_id,
        )

    @property
    def identity(self) -> tuple[str, str, int, str]:
        return (
            self.request_id,
            self.idempotency_key,
            self.attempt_number,
            self.command_id,
        )


@dataclass(frozen=True)
class SchedulerAcknowledgement:
    command_id: str
    scheduling_id: str
    status: SchedulerAcknowledgementStatus
    observed_at: datetime

    def __post_init__(self) -> None:
        if not self.command_id.strip() or not self.scheduling_id.strip():
            raise ValueError("command_id and scheduling_id cannot be empty")
        if self.observed_at.tzinfo is None or self.observed_at.utcoffset() is None:
            raise ValueError("observed_at must be timezone-aware")


class RetryCommandStore(Protocol):
    def create_or_get(self, command: RetryCommand) -> RetryCommand:
        ...

    def get(self, command_id: str) -> RetryCommand | None:
        ...

    def claim(self, command_id: str) -> RetryCommand | None:
        ...

    def record_scheduler_acknowledgement(
        self,
        command_id: str,
        acknowledgement: SchedulerAcknowledgement,
    ) -> RetryCommand:
        ...

    def save(self, command: RetryCommand) -> RetryCommand:
        ...


class RetrySchedulerPort(Protocol):
    def schedule(self, command: RetryCommand) -> SchedulerAcknowledgement:
        ...
