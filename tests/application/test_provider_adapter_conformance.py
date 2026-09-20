from datetime import datetime, timezone

import pytest

from app.application.execution_port import ProviderExecutionResult
from app.application.provider_adapter_conformance import validate_provider_execution_result
from app.domain.authorized_execution_request import AuthorizedExecutionRequest, ExecutionRequestStatus
from app.domain.action_authorization import ActionClass, AutonomyLevel
from app.domain.execution_outcome import ExecutionOutcomeStatus


def request():
    return AuthorizedExecutionRequest(
        request_id="req-1",
        idempotency_key="idem-1",
        action_class=ActionClass.REVERSIBLE_EXTERNAL,
        autonomy_level=AutonomyLevel.L3_EXECUTE_WITH_APPROVAL,
        policy_id="policy-1",
        policy_version="1",
        status=ExecutionRequestStatus.PREPARED,
    )


def result(**overrides):
    values = {
        "request_id": "req-1",
        "idempotency_key": "idem-1",
        "status": ExecutionOutcomeStatus.SUCCEEDED,
        "outcome_code": "ok",
        "observed_at": datetime(2026, 9, 20, tzinfo=timezone.utc),
    }
    values.update(overrides)
    return ProviderExecutionResult(**values)


def test_accepts_valid_provider_result():
    validate_provider_execution_result(request(), result())


def test_rejects_request_identity_mismatch():
    with pytest.raises(ValueError, match="request_id"):
        validate_provider_execution_result(request(), result(request_id="other"))


def test_rejects_idempotency_identity_mismatch():
    with pytest.raises(ValueError, match="idempotency_key"):
        validate_provider_execution_result(request(), result(idempotency_key="other"))


def test_rejects_non_timezone_aware_observation():
    with pytest.raises(ValueError, match="timezone-aware"):
        validate_provider_execution_result(
            request(),
            result(observed_at=datetime(2026, 9, 20)),
        )


def test_rejects_non_provider_result():
    with pytest.raises(TypeError, match="ProviderExecutionResult"):
        validate_provider_execution_result(request(), object())
