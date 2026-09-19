import pytest

from app.domain.action_authorization import ActionAuthorization, ActionAuthorizationStatus, ActionClass, AutonomyLevel
from app.domain.authorized_execution_request import ExecutionRequestStatus, prepare_execution_request


def _authorization(status=ActionAuthorizationStatus.AUTHORIZED):
    return ActionAuthorization(policy_id="p1", policy_version="1", action_class=ActionClass.REVERSIBLE_EXTERNAL,
                               requested_autonomy=AutonomyLevel.L3_EXECUTE_WITH_APPROVAL,
                               maximum_autonomy=AutonomyLevel.L3_EXECUTE_WITH_APPROVAL,
                               status=status, requires_human_approval=(status is ActionAuthorizationStatus.HUMAN_APPROVAL_REQUIRED))


def test_authorized_action_produces_prepared_request():
    result = prepare_execution_request(request_id="r1", idempotency_key="idem-1", authorization=_authorization())
    assert result.status is ExecutionRequestStatus.PREPARED
    assert result.policy_id == "p1"
    assert result.idempotency_key == "idem-1"


@pytest.mark.parametrize("status", [ActionAuthorizationStatus.HUMAN_APPROVAL_REQUIRED, ActionAuthorizationStatus.NOT_AUTHORIZED, ActionAuthorizationStatus.SAFETY_BLOCKED])
def test_unauthorized_action_cannot_be_prepared(status):
    result = prepare_execution_request(request_id="r1", idempotency_key="idem-1", authorization=_authorization(status))
    assert result.status is ExecutionRequestStatus.REJECTED


def test_request_identity_and_idempotency_key_are_required():
    with pytest.raises(ValueError):
        prepare_execution_request(request_id="", idempotency_key="idem-1", authorization=_authorization())
    with pytest.raises(ValueError):
        prepare_execution_request(request_id="r1", idempotency_key="", authorization=_authorization())


def test_prepared_request_preserves_authorization_context():
    result = prepare_execution_request(request_id="r1", idempotency_key="idem-1", authorization=_authorization())
    assert result.action_class is ActionClass.REVERSIBLE_EXTERNAL
    assert result.autonomy_level is AutonomyLevel.L3_EXECUTE_WITH_APPROVAL
    assert result.policy_version == "1"
