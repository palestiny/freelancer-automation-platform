from datetime import datetime, timezone
import pytest

from app.application.execution_port import ProviderExecutionResult, dispatch_execution
from app.domain.action_authorization import ActionClass, AutonomyLevel
from app.domain.authorized_execution_request import AuthorizedExecutionRequest, ExecutionRequestStatus
from app.domain.execution_outcome import ExecutionOutcomeStatus

def _request():
    return AuthorizedExecutionRequest(request_id='req-1', idempotency_key='idem-1', action_class=ActionClass.REVERSIBLE_EXTERNAL, autonomy_level=AutonomyLevel.L3_EXECUTE_WITH_APPROVAL, policy_id='policy', policy_version='1', status=ExecutionRequestStatus.PREPARED)

class WrongTypePort:
    def execute(self, request):
        return {'request_id': request.request_id}

def test_dispatch_rejects_untyped_provider_result():
    with pytest.raises(TypeError, match='ProviderExecutionResult'):
        dispatch_execution(port=WrongTypePort(), request=_request())

def test_provider_result_rejects_invalid_status_type():
    with pytest.raises(TypeError, match='status'):
        ProviderExecutionResult(request_id='req-1', idempotency_key='idem-1', status='succeeded', outcome_code='ok', observed_at=datetime(2026, 9, 19, tzinfo=timezone.utc))