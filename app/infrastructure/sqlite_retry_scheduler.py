from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from uuid import uuid4

from app.domain.execution_retry import (
    RetryCommand,
    RetrySchedulerPort,
    SchedulerAcknowledgement,
    SchedulerAcknowledgementStatus,
)


class SQLiteRetryScheduler(RetrySchedulerPort):
    def __init__(self, database: str) -> None:
        self._connection = sqlite3.connect(database, check_same_thread=False)
        self._connection.execute(
            """
            CREATE TABLE IF NOT EXISTS retry_schedule (
                scheduling_id TEXT PRIMARY KEY,
                command_id TEXT NOT NULL,
                request_id TEXT NOT NULL,
                idempotency_key TEXT NOT NULL,
                attempt_number INTEGER NOT NULL,
                scheduled_at TEXT NOT NULL,
                UNIQUE(command_id),
                UNIQUE(request_id, idempotency_key, attempt_number)
            )
            """
        )
        self._connection.commit()

    def schedule(self, command: RetryCommand) -> SchedulerAcknowledgement:
        if command.action.value != "retry":
            raise ValueError("only retry commands can be scheduled")

        row = self._connection.execute(
            """
            SELECT scheduling_id, scheduled_at
            FROM retry_schedule
            WHERE request_id = ? AND idempotency_key = ? AND attempt_number = ?
            """,
            command.deduplication_key,
        ).fetchone()

        if row is not None:
            existing = self._connection.execute(
                "SELECT command_id FROM retry_schedule WHERE scheduling_id = ?",
                (row[0],),
            ).fetchone()
            if existing is None:
                raise RuntimeError("retry schedule identity is inconsistent")
            if existing[0] != command.command_id:
                raise ValueError("command identity conflict for retry schedule")

        if row is None:
            scheduling_id = f"schedule-{uuid4().hex}"
            scheduled_at = datetime.now(timezone.utc)
            try:
                self._connection.execute(
                    """
                    INSERT INTO retry_schedule (
                        scheduling_id, command_id, request_id, idempotency_key,
                        attempt_number, scheduled_at
                    ) VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        scheduling_id,
                        command.command_id,
                        command.request_id,
                        command.idempotency_key,
                        command.attempt_number,
                        scheduled_at.isoformat(),
                    ),
                )
                self._connection.commit()
            except sqlite3.IntegrityError:
                self._connection.rollback()
                row = self._connection.execute(
                    """
                    SELECT scheduling_id, scheduled_at
                    FROM retry_schedule
                    WHERE request_id = ? AND idempotency_key = ? AND attempt_number = ?
                    """,
                    command.deduplication_key,
                ).fetchone()
                if row is None:
                    raise RuntimeError("retry schedule insert conflicted without a durable record")
                existing = self._connection.execute(
                    "SELECT command_id FROM retry_schedule WHERE scheduling_id = ?",
                    (row[0],),
                ).fetchone()
                if existing is None or existing[0] != command.command_id:
                    raise ValueError("command identity conflict for retry schedule")
            else:
                row = (scheduling_id, scheduled_at.isoformat())

        return SchedulerAcknowledgement(
            command_id=command.command_id,
            scheduling_id=row[0],
            status=SchedulerAcknowledgementStatus.ACCEPTED,
            observed_at=datetime.fromisoformat(row[1]),
        )
