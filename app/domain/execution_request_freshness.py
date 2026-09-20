from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum

from .authorized_execution_request import AuthorizedExecutionRequest, ExecutionRequestStatus


class ExecutionRequestFreshnessStatus(str, Enum):
    FRESH = "fresh"
    STALE = "stale"
    INELIGIBLE = "ineligible"


class ExecutionRequestFreshnessReason(str, Enum):
    FRESH = "fresh"
    STALE = "stale"
    MISSING_PREPARED_AT = "missing_prepared_at"
    FUTURE_PREPARED_AT = "future_prepared_at"
    NOT_PREPARED = "not_prepared"


@dataclass(frozen=True)
class ExecutionRequestFreshnessPolicy:
    maximum_age: timedelta = timedelta(minutes=30)

    def __post_init__(self) -> None:
        if self.maximum_age <= timedelta(0):
            raise ValueError("maximum_age must be greater than zero")


@dataclass(frozen=True)
class ExecutionRequestFreshnessAssessment:
    status: ExecutionRequestFreshnessStatus
    reason: ExecutionRequestFreshnessReason

    def __post_init__(self) -> None:
        if self.status is ExecutionRequestFreshnessStatus.FRESH:
            if self.reason is not ExecutionRequestFreshnessReason.FRESH:
                raise ValueError("fresh status requires fresh reason")
        elif self.status is ExecutionRequestFreshnessStatus.STALE:
            if self.reason is not ExecutionRequestFreshnessReason.STALE:
                raise ValueError("stale status requires stale reason")
        elif self.reason in {
            ExecutionRequestFreshnessReason.FRESH,
            ExecutionRequestFreshnessReason.STALE,
        }:
            raise ValueError("ineligible status requires an ineligibility reason")


def assess_execution_request_freshness(
    *,
    request: AuthorizedExecutionRequest,
    policy: ExecutionRequestFreshnessPolicy,
    as_of: datetime,
) -> ExecutionRequestFreshnessAssessment:
    if request.status is not ExecutionRequestStatus.PREPARED:
        return ExecutionRequestFreshnessAssessment(
            status=ExecutionRequestFreshnessStatus.INELIGIBLE,
            reason=ExecutionRequestFreshnessReason.NOT_PREPARED,
        )
    if request.prepared_at is None:
        return ExecutionRequestFreshnessAssessment(
            status=ExecutionRequestFreshnessStatus.INELIGIBLE,
            reason=ExecutionRequestFreshnessReason.MISSING_PREPARED_AT,
        )
    if request.prepared_at > as_of:
        return ExecutionRequestFreshnessAssessment(
            status=ExecutionRequestFreshnessStatus.INELIGIBLE,
            reason=ExecutionRequestFreshnessReason.FUTURE_PREPARED_AT,
        )
    if as_of - request.prepared_at > policy.maximum_age:
        return ExecutionRequestFreshnessAssessment(
            status=ExecutionRequestFreshnessStatus.STALE,
            reason=ExecutionRequestFreshnessReason.STALE,
        )
    return ExecutionRequestFreshnessAssessment(
        status=ExecutionRequestFreshnessStatus.FRESH,
        reason=ExecutionRequestFreshnessReason.FRESH,
    )
