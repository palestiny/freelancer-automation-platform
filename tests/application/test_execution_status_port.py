from datetime import datetime, timezone

import pytest

from app.application.execution_status_port import (
    ProviderExecutionStatusPort,
    ProviderExecutionStatusQuery,
    ProviderExecutionStatusResult,
    observe_provider_execution_status,
)
from app.domain.execution_outcome import ExecutionOutcomeStatus


OBSERVED_AT = datetime(2026, 9, 20, 8, 0, tzinfo=timezone.utc)


class StubStatusPort(ProviderExecutionStatusPort):
    def __init__(self, result):
        self.result = result
        self.query = None

    def get_status(self, query):
        self.query = query
        return self.result


def _result(status=ExecutionOutcomeStatus.UNKNOWN):
    return ProviderExecutionStatusResult(
        request_id="request-1",
        idempotency_key="idem-1",
        status=status,
        outcome_code="provider_status",
        observed_at=OBSERVED_AT,
        external_reference="external-1",
    )


def test_status_observation_preserves_identity_and_is_non_executing():
    port = StubStatusPort(_result(ExecutionOutcomeStatus.SUCCEEDED))

    result = observe_provider_execution_status(
        port=port,
        query=ProviderExecutionStatusQuery(
            request_id="request-1",
            idempotency_key="idem-1",
        ),
    )

    assert result.status is ExecutionOutcomeStatus.SUCCEEDED
    assert result.request_id == "request-1"
    assert result.idempotency_key == "idem-1"
    assert port.query.request_id == "request-1"


def test_unknown_status_remains_unknown():
    port = StubStatusPort(_result())

    result = observe_provider_execution_status(
        port=port,
        query=ProviderExecutionStatusQuery(
            request_id="request-1",
            idempotency_key="idem-1",
        ),
    )

    assert result.status is ExecutionOutcomeStatus.UNKNOWN


def test_provider_result_identity_mismatch_is_rejected():
    port = StubStatusPort(
        ProviderExecutionStatusResult(
            request_id="other",
            idempotency_key="idem-1",
            status=ExecutionOutcomeStatus.SUCCEEDED,
            outcome_code="done",
            observed_at=OBSERVED_AT,
        )
    )

    with pytest.raises(ValueError, match="request_id"):
        observe_provider_execution_status(
            port=port,
            query=ProviderExecutionStatusQuery(
                request_id="request-1",
                idempotency_key="idem-1",
            ),
        )


def test_provider_result_requires_timezone_aware_timestamp():
    with pytest.raises(ValueError, match="timezone-aware"):
        ProviderExecutionStatusResult(
            request_id="request-1",
            idempotency_key="idem-1",
            status=ExecutionOutcomeStatus.UNKNOWN,
            outcome_code="unknown",
            observed_at=datetime(2026, 9, 20, 8, 0),
        )
