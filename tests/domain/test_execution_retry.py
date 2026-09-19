from datetime import datetime, timezone

import pytest

from app.domain.execution_retry import (
    RetryCommand,
    RetryCommandAction,
    RetryCommandState,
    SchedulerAcknowledgement,
    SchedulerAcknowledgementStatus,
)


def _command(**overrides):
    values = dict(
        command_id="cmd-1",
        request_id="req-1",
        idempotency_key="idem-1",
        attempt_number=2,
        action=RetryCommandAction.RETRY,
        authorization_policy_id="policy-1",
        authorization_policy_version="v1",
        autonomy_bound="L3",
        created_at=datetime(2026, 9, 19, tzinfo=timezone.utc),
        state=RetryCommandState.CREATED,
    )
    values.update(overrides)
    return RetryCommand(**values)


def test_retry_command_rejects_non_positive_attempt():
    with pytest.raises(ValueError):
        _command(attempt_number=0)


def test_retry_command_identity_is_immutable_and_explicit():
    command = _command()
    assert command.identity == ("req-1", "idem-1", 2, "cmd-1")


def test_retry_command_requires_timezone_aware_creation_time():
    with pytest.raises(ValueError):
        _command(created_at=datetime(2026, 9, 19))


@pytest.mark.parametrize(
    "status",
    [
        SchedulerAcknowledgementStatus.ACCEPTED,
        SchedulerAcknowledgementStatus.REJECTED,
        SchedulerAcknowledgementStatus.AMBIGUOUS,
    ],
)
def test_scheduler_acknowledgement_has_explicit_status(status):
    ack = SchedulerAcknowledgement(
        command_id="cmd-1",
        scheduling_id="schedule-1",
        status=status,
        observed_at=datetime(2026, 9, 19, tzinfo=timezone.utc),
    )
    assert ack.status is status


def test_scheduler_acknowledgement_requires_identity():
    with pytest.raises(ValueError):
        SchedulerAcknowledgement(
            command_id="",
            scheduling_id="schedule-1",
            status=SchedulerAcknowledgementStatus.ACCEPTED,
            observed_at=datetime(2026, 9, 19, tzinfo=timezone.utc),
        )


def test_retry_command_allows_declared_lifecycle_transitions():
    command = RetryCommand(command_id="cmd", request_id="req", idempotency_key="idem", attempt_number=1, action=RetryCommandAction.RETRY, authorization_policy_id="policy", authorization_policy_version="v1", autonomy_bound="L4", created_at=datetime(2026, 9, 19, tzinfo=timezone.utc))
    claimed = command.transition_to(RetryCommandState.CLAIMED)
    scheduled = claimed.transition_to(RetryCommandState.SCHEDULED, scheduling_id="s1")
    assert scheduled.state is RetryCommandState.SCHEDULED
    assert scheduled.scheduling_id == "s1"


def test_retry_command_rejects_invalid_transition():
    command = RetryCommand(command_id="cmd", request_id="req", idempotency_key="idem", attempt_number=1, action=RetryCommandAction.RETRY, authorization_policy_id="policy", authorization_policy_version="v1", autonomy_bound="L4", created_at=datetime(2026, 9, 19, tzinfo=timezone.utc))
    assert command.can_transition_to(RetryCommandState.COMPLETED) is False
    try:
        command.transition_to(RetryCommandState.COMPLETED)
    except ValueError:
        pass
    else:
        raise AssertionError("invalid transition must fail")
