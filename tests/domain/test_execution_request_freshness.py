from datetime import datetime, timedelta, timezone

from app.domain.action_authorization import ActionClass, AutonomyLevel
from app.domain.authorized_execution_request import (
    AuthorizedExecutionRequest,
    ExecutionRequestStatus,
)
from app.domain.execution_request_freshness import (
    ExecutionRequestFreshnessReason,
    ExecutionRequestFreshnessStatus,
    ExecutionRequestFreshnessPolicy,
    assess_execution_request_freshness,
)


def _request(status=ExecutionRequestStatus.PREPARED, prepared_at=None):
    return AuthorizedExecutionRequest(
        request_id="r1",
        idempotency_key="i1",
        action_class=ActionClass.REVERSIBLE_EXTERNAL,
        autonomy_level=AutonomyLevel.L3_EXECUTE_WITH_APPROVAL,
        policy_id="p1",
        policy_version="1",
        status=status,
        prepared_at=prepared_at,
    )


def test_prepared_request_is_fresh_within_explicit_age():
    prepared_at = datetime(2026, 9, 20, 12, tzinfo=timezone.utc)
    result = assess_execution_request_freshness(
        request=_request(prepared_at=prepared_at),
        policy=ExecutionRequestFreshnessPolicy(maximum_age=timedelta(minutes=30)),
        as_of=prepared_at + timedelta(minutes=10),
    )
    assert result.status is ExecutionRequestFreshnessStatus.FRESH
    assert result.reason is ExecutionRequestFreshnessReason.FRESH


def test_prepared_request_becomes_stale_after_policy_age():
    prepared_at = datetime(2026, 9, 20, 12, tzinfo=timezone.utc)
    result = assess_execution_request_freshness(
        request=_request(prepared_at=prepared_at),
        policy=ExecutionRequestFreshnessPolicy(maximum_age=timedelta(minutes=30)),
        as_of=prepared_at + timedelta(minutes=31),
    )
    assert result.status is ExecutionRequestFreshnessStatus.STALE
    assert result.reason is ExecutionRequestFreshnessReason.STALE


def test_missing_prepared_timestamp_is_explicit():
    result = assess_execution_request_freshness(
        request=_request(),
        policy=ExecutionRequestFreshnessPolicy(),
        as_of=datetime(2026, 9, 20, 12, tzinfo=timezone.utc),
    )
    assert result.reason is ExecutionRequestFreshnessReason.MISSING_PREPARED_AT


def test_future_prepared_timestamp_is_rejected():
    as_of = datetime(2026, 9, 20, 12, tzinfo=timezone.utc)
    result = assess_execution_request_freshness(
        request=_request(prepared_at=as_of + timedelta(seconds=1)),
        policy=ExecutionRequestFreshnessPolicy(),
        as_of=as_of,
    )
    assert result.reason is ExecutionRequestFreshnessReason.FUTURE_PREPARED_AT


def test_non_prepared_request_is_not_fresh():
    result = assess_execution_request_freshness(
        request=_request(status=ExecutionRequestStatus.REJECTED),
        policy=ExecutionRequestFreshnessPolicy(),
        as_of=datetime(2026, 9, 20, 12, tzinfo=timezone.utc),
    )
    assert result.reason is ExecutionRequestFreshnessReason.NOT_PREPARED
