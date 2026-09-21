from datetime import datetime, timezone

from app.application.execution_port import ExecutionPort, ProviderExecutionResult
from app.application.persisted_execution_coordination import (
    PersistedExecutionCoordinationStatus,
    coordinate_persisted_execution,
)
from app.domain.action_authorization import ActionClass, AutonomyLevel
from app.domain.authorized_execution_request import AuthorizedExecutionRequest, ExecutionRequestStatus
from app.domain.execution_outcome import ExecutionOutcomeStatus
from app.domain.execution_outcome_policy import ExecutionOutcomePolicy


class Provider(ExecutionPort):
    def __init__(self, raw=None, error=None):
        self.raw = raw
        self.error = error
        self.calls = 0

    def execute(self, request):
        self.calls += 1
        if self.error:
            raise self.error
        return self.raw


class Recorder:
    def __init__(self, error=None):
        self.error = error
        self.saved = []

    def save(self, outcome):
        if self.error:
            raise self.error
        self.saved.append(outcome)


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


def outcome():
    return ProviderExecutionResult(
        request_id="req-1",
        idempotency_key="idem-1",
        status=ExecutionOutcomeStatus.SUCCEEDED,
        outcome_code="ok",
        observed_at=datetime(2026, 9, 21, tzinfo=timezone.utc),
    )


def policy():
    return ExecutionOutcomePolicy(maximum_attempts=3, retryable_outcome_codes=("timeout",))


def test_persistence_precedes_assessment_and_recovery():
    recorder = Recorder()
    result = coordinate_persisted_execution(
        port=Provider(outcome()),
        request=request(),
        policy=policy(),
        attempt_count=1,
        outcome_repository=recorder,
    )

    assert result.status is PersistedExecutionCoordinationStatus.COMPLETED
    assert len(recorder.saved) == 1
    assert result.coordination is not None
    assert result.coordination.outcome == recorder.saved[0]
    assert result.coordination.policy_assessment.outcome_status is ExecutionOutcomeStatus.SUCCEEDED


def test_persistence_failure_stops_assessment_and_recovery():
    recorder = Recorder(error=RuntimeError("database unavailable"))
    result = coordinate_persisted_execution(
        port=Provider(outcome()),
        request=request(),
        policy=policy(),
        attempt_count=1,
        outcome_repository=recorder,
    )

    assert result.status is PersistedExecutionCoordinationStatus.OUTCOME_PERSISTENCE_FAILURE
    assert result.coordination is None
    assert result.outcome.request_id == "req-1"
    assert result.outcome.status is ExecutionOutcomeStatus.SUCCEEDED


def test_provider_failure_produces_no_fabricated_outcome():
    result = coordinate_persisted_execution(
        port=Provider(error=RuntimeError("provider unavailable")),
        request=request(),
        policy=policy(),
        attempt_count=1,
        outcome_repository=Recorder(),
    )

    assert result.status is PersistedExecutionCoordinationStatus.PROVIDER_FAILURE
    assert result.outcome is None
    assert result.coordination is None


def test_existing_coordination_semantics_are_preserved_after_persistence():
    result = coordinate_persisted_execution(
        port=Provider(
            ProviderExecutionResult(
                request_id="req-1",
                idempotency_key="idem-1",
                status=ExecutionOutcomeStatus.FAILED,
                outcome_code="timeout",
                observed_at=datetime(2026, 9, 21, tzinfo=timezone.utc),
            )
        ),
        request=request(),
        policy=policy(),
        attempt_count=1,
        outcome_repository=Recorder(),
    )

    assert result.status is PersistedExecutionCoordinationStatus.COMPLETED
    assert result.coordination is not None
    assert result.coordination.recovery_handoff.mode.value == "retry"
