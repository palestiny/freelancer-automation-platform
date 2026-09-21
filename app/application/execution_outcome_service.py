from app.application.ports.execution_outcome_repository import ExecutionOutcomeRepository
from app.domain.execution_outcome import ExecutionOutcome


class ExecutionOutcomeService:
    def __init__(self, repository: ExecutionOutcomeRepository) -> None:
        self._repository = repository

    def record(self, outcome: ExecutionOutcome) -> None:
        self._repository.save(outcome)

    def get_by_request_id(self, request_id: str) -> ExecutionOutcome | None:
        if not request_id.strip():
            raise ValueError("request_id cannot be empty")
        return self._repository.get_by_request_id(request_id)

    def list_by_idempotency_key(
        self,
        idempotency_key: str,
    ) -> tuple[ExecutionOutcome, ...]:
        if not idempotency_key.strip():
            raise ValueError("idempotency_key cannot be empty")
        return self._repository.list_by_idempotency_key(idempotency_key)
