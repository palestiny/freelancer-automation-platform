from datetime import datetime, timezone

import pytest

from app.domain.execution_outcome import ExecutionOutcome, ExecutionOutcomeStatus
from app.infrastructure.execution_outcome_repository import SQLiteExecutionOutcomeRepository


def _outcome(**kwargs):
    values = dict(
        request_id="req-1",
        idempotency_key="idem-1",
        status=ExecutionOutcomeStatus.SUCCEEDED,
        outcome_code="ok",
        observed_at=datetime(2026, 9, 21, tzinfo=timezone.utc),
        external_reference="ext-1",
    )
    values.update(kwargs)
    return ExecutionOutcome(**values)


def test_save_and_get_round_trip(tmp_path):
    repository = SQLiteExecutionOutcomeRepository(str(tmp_path / "outcomes.db"))
    outcome = _outcome()
    repository.save(outcome)
    assert repository.get_by_request_id("req-1") == outcome
    repository.close()


def test_identical_retry_is_idempotent(tmp_path):
    repository = SQLiteExecutionOutcomeRepository(str(tmp_path / "outcomes.db"))
    outcome = _outcome()
    repository.save(outcome)
    repository.save(outcome)
    assert repository.list_by_idempotency_key("idem-1") == (outcome,)
    repository.close()


def test_conflicting_outcome_same_request_and_time_is_rejected(tmp_path):
    repository = SQLiteExecutionOutcomeRepository(str(tmp_path / "outcomes.db"))
    repository.save(_outcome())
    with pytest.raises(ValueError, match="conflicting"):
        repository.save(_outcome(status=ExecutionOutcomeStatus.FAILED, outcome_code="failed"))
    repository.close()


def test_multiple_outcomes_for_same_idempotency_key_are_preserved_by_time(tmp_path):
    repository = SQLiteExecutionOutcomeRepository(str(tmp_path / "outcomes.db"))
    first = _outcome(observed_at=datetime(2026, 9, 21, 1, tzinfo=timezone.utc))
    second = _outcome(observed_at=datetime(2026, 9, 21, 2, tzinfo=timezone.utc), status=ExecutionOutcomeStatus.FAILED, outcome_code="timeout")
    repository.save(first)
    repository.save(second)
    assert repository.list_by_idempotency_key("idem-1") == (first, second)
    repository.close()
