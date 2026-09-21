from typing import Protocol

from app.domain.execution_outcome import ExecutionOutcome


class ExecutionOutcomeRepository(Protocol):
    def save(self, outcome: ExecutionOutcome) -> None:
        ...

    def get_by_request_id(self, request_id: str) -> ExecutionOutcome | None:
        ...

    def list_by_idempotency_key(
        self,
        idempotency_key: str,
    ) -> tuple[ExecutionOutcome, ...]:
        ...
