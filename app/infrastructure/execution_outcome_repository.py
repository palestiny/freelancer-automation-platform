import sqlite3
from datetime import datetime

from app.domain.execution_outcome import ExecutionOutcome, ExecutionOutcomeStatus


class SQLiteExecutionOutcomeRepository:
    def __init__(self, database: str) -> None:
        self._connection = sqlite3.connect(database)
        self._connection.row_factory = sqlite3.Row
        self._connection.execute(
            """
            CREATE TABLE IF NOT EXISTS execution_outcomes (
                request_id TEXT NOT NULL,
                idempotency_key TEXT NOT NULL,
                status TEXT NOT NULL,
                outcome_code TEXT NOT NULL,
                observed_at TEXT NOT NULL,
                external_reference TEXT,
                PRIMARY KEY (request_id, observed_at),
                UNIQUE (request_id, idempotency_key, outcome_code, status, observed_at)
            )
            """
        )
        self._connection.commit()

    def save(self, outcome: ExecutionOutcome) -> None:
        existing = self._connection.execute(
            "SELECT * FROM execution_outcomes WHERE request_id = ? AND observed_at = ?",
            (outcome.request_id, outcome.observed_at.isoformat()),
        ).fetchone()
        if existing is not None:
            current = self._to_domain(existing)
            if current == outcome:
                return
            raise ValueError("conflicting execution outcome for request and observation time")
        self._connection.execute(
            """
            INSERT INTO execution_outcomes
            (request_id, idempotency_key, status, outcome_code, observed_at, external_reference)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                outcome.request_id,
                outcome.idempotency_key,
                outcome.status.value,
                outcome.outcome_code,
                outcome.observed_at.isoformat(),
                outcome.external_reference,
            ),
        )
        self._connection.commit()

    def get_by_request_id(self, request_id: str) -> ExecutionOutcome | None:
        row = self._connection.execute(
            "SELECT * FROM execution_outcomes WHERE request_id = ? ORDER BY observed_at DESC LIMIT 1",
            (request_id,),
        ).fetchone()
        return None if row is None else self._to_domain(row)

    def list_by_idempotency_key(
        self, idempotency_key: str
    ) -> tuple[ExecutionOutcome, ...]:
        rows = self._connection.execute(
            "SELECT * FROM execution_outcomes WHERE idempotency_key = ? ORDER BY observed_at",
            (idempotency_key,),
        ).fetchall()
        return tuple(self._to_domain(row) for row in rows)

    @staticmethod
    def _to_domain(row: sqlite3.Row) -> ExecutionOutcome:
        return ExecutionOutcome(
            request_id=row["request_id"],
            idempotency_key=row["idempotency_key"],
            status=ExecutionOutcomeStatus(row["status"]),
            outcome_code=row["outcome_code"],
            observed_at=datetime.fromisoformat(row["observed_at"]),
            external_reference=row["external_reference"],
        )

    def close(self) -> None:
        self._connection.close()
