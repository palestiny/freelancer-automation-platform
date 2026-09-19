from __future__ import annotations

import sqlite3
from datetime import datetime
from typing import Any

from app.domain.execution_retry import (
    RetryCommand,
    RetryCommandAction,
    RetryCommandState,
    RetryCommandStore,
    SchedulerAcknowledgement,
    SchedulerAcknowledgementStatus,
)


class SQLiteRetryCommandStore(RetryCommandStore):
    def __init__(self, database: str) -> None:
        self._connection = sqlite3.connect(database, check_same_thread=False, timeout=5.0)
        self._connection.execute("PRAGMA busy_timeout = 5000")
        self._connection.execute("PRAGMA foreign_keys = ON")
        self._initialize_schema()

    def _initialize_schema(self) -> None:
        self._connection.execute(
            """
            CREATE TABLE IF NOT EXISTS retry_commands (
                command_id TEXT PRIMARY KEY,
                request_id TEXT NOT NULL,
                idempotency_key TEXT NOT NULL,
                attempt_number INTEGER NOT NULL,
                action TEXT NOT NULL,
                authorization_policy_id TEXT NOT NULL,
                authorization_policy_version TEXT NOT NULL,
                autonomy_bound TEXT NOT NULL,
                created_at TEXT NOT NULL,
                state TEXT NOT NULL,
                scheduling_id TEXT,
                UNIQUE(request_id, idempotency_key, attempt_number)
            )
            """
        )
        self._connection.commit()

    def create_or_get(self, command: RetryCommand) -> RetryCommand:
        row = self._connection.execute(
            "SELECT * FROM retry_commands WHERE request_id = ? AND idempotency_key = ? AND attempt_number = ?",
            command.deduplication_key,
        ).fetchone()
        if row is not None:
            existing = self._from_row(row)
            if existing.command_id != command.command_id:
                raise ValueError("command identity conflict for logical retry")
            return existing

        try:
            self._connection.execute(
                """
                INSERT INTO retry_commands (
                    command_id, request_id, idempotency_key, attempt_number,
                    action, authorization_policy_id, authorization_policy_version,
                    autonomy_bound, created_at, state, scheduling_id
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                self._to_params(command),
            )
            self._connection.commit()
        except sqlite3.IntegrityError:
            self._connection.rollback()
            row = self._connection.execute(
                "SELECT * FROM retry_commands WHERE request_id = ? AND idempotency_key = ? AND attempt_number = ?",
                command.deduplication_key,
            ).fetchone()
            if row is None:
                raise
            existing = self._from_row(row)
            if existing.command_id != command.command_id:
                raise ValueError("command identity conflict for logical retry")
            return existing

        return command

    def get(self, command_id: str) -> RetryCommand | None:
        row = self._connection.execute(
            "SELECT * FROM retry_commands WHERE command_id = ?",
            (command_id,),
        ).fetchone()
        return None if row is None else self._from_row(row)

    def claim(self, command_id: str) -> RetryCommand | None:
        self._connection.execute("BEGIN IMMEDIATE")
        try:
            cursor = self._connection.execute(
                """
                UPDATE retry_commands
                SET state = ?
                WHERE command_id = ? AND state = ?
                """,
                (
                    RetryCommandState.CLAIMED.value,
                    command_id,
                    RetryCommandState.CREATED.value,
                ),
            )
            if cursor.rowcount != 1:
                self._connection.rollback()
                return None

            self._connection.commit()
        except Exception:
            self._connection.rollback()
            raise

        return self.get(command_id)

    def record_scheduler_acknowledgement(
        self,
        command_id: str,
        acknowledgement: SchedulerAcknowledgement,
    ) -> RetryCommand:
        if acknowledgement.command_id != command_id:
            raise ValueError("acknowledgement command_id does not match command_id")

        current = self.get(command_id)
        if current is None:
            raise KeyError(command_id)

        target = {
            SchedulerAcknowledgementStatus.ACCEPTED: RetryCommandState.SCHEDULED,
            SchedulerAcknowledgementStatus.REJECTED: RetryCommandState.REQUIRES_MANUAL_REVIEW,
            SchedulerAcknowledgementStatus.AMBIGUOUS: RetryCommandState.SCHEDULING_AMBIGUOUS,
        }[acknowledgement.status]
        updated = current.transition_to(target, scheduling_id=acknowledgement.scheduling_id)
        return self.save(updated)

    def save(self, command: RetryCommand) -> RetryCommand:
        current = self.get(command.command_id)
        if current is None:
            raise KeyError(command.command_id)

        if current.identity != command.identity:
            raise ValueError("immutable retry command identity cannot change")
        if current.state is not command.state:
            if not current.can_transition_to(command.state):
                raise ValueError(
                    f"invalid retry command transition: {current.state.value} -> {command.state.value}"
                )

        self._connection.execute(
            """
            UPDATE retry_commands
            SET state = ?, scheduling_id = ?
            WHERE command_id = ?
            """,
            (command.state.value, command.scheduling_id, command.command_id),
        )
        self._connection.commit()
        return command

    @staticmethod
    def _to_params(command: RetryCommand) -> tuple[Any, ...]:
        return (
            command.command_id,
            command.request_id,
            command.idempotency_key,
            command.attempt_number,
            command.action.value,
            command.authorization_policy_id,
            command.authorization_policy_version,
            command.autonomy_bound,
            command.created_at.isoformat(),
            command.state.value,
            command.scheduling_id,
        )

    @staticmethod
    def _from_row(row: tuple[Any, ...]) -> RetryCommand:
        return RetryCommand(
            command_id=row[0],
            request_id=row[1],
            idempotency_key=row[2],
            attempt_number=row[3],
            action=RetryCommandAction(row[4]),
            authorization_policy_id=row[5],
            authorization_policy_version=row[6],
            autonomy_bound=row[7],
            created_at=datetime.fromisoformat(row[8]),
            state=RetryCommandState(row[9]),
            scheduling_id=row[10],
        )
