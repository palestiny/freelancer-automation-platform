from datetime import datetime, timezone
import pytest

from app.domain.execution_retry import RetryCommand, RetryCommandAction
from app.infrastructure.sqlite_retry_command_store import SQLiteRetryCommandStore


def _command(command_id: str) -> RetryCommand:
    return RetryCommand(
        command_id=command_id,
        request_id="req-1",
        idempotency_key="idem-1",
        attempt_number=1,
        action=RetryCommandAction.RETRY,
        authorization_policy_id="policy",
        authorization_policy_version="v1",
        autonomy_bound="L3",
        created_at=datetime(2026, 9, 20, tzinfo=timezone.utc),
    )


def test_duplicate_logical_command_with_different_command_id_is_identity_conflict():
    store = SQLiteRetryCommandStore(":memory:")
    store.create_or_get(_command("cmd-1"))

    with pytest.raises(ValueError, match="command_id"):
        store.create_or_get(_command("cmd-2"))
