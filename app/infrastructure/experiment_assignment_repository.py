import sqlite3
from datetime import datetime

from app.domain.controlled_experiment_evidence import ExperimentAssignment


class SQLiteExperimentAssignmentRepository:
    """Reference durable adapter for authoritative experiment assignments."""

    def __init__(self, database: str) -> None:
        self._connection = sqlite3.connect(database)
        self._connection.row_factory = sqlite3.Row
        self._connection.execute(
            """
            CREATE TABLE IF NOT EXISTS experiment_assignments (
                id TEXT PRIMARY KEY,
                experiment_id TEXT NOT NULL,
                subject_id TEXT NOT NULL,
                variant TEXT NOT NULL,
                assigned_at TEXT NOT NULL,
                UNIQUE (experiment_id, subject_id)
            )
            """
        )
        self._connection.commit()

    def save(self, assignment: ExperimentAssignment) -> None:
        try:
            self._connection.execute(
                """
                INSERT INTO experiment_assignments (
                    id, experiment_id, subject_id, variant, assigned_at
                ) VALUES (?, ?, ?, ?, ?)
                """,
                (
                    assignment.id,
                    assignment.experiment_id,
                    assignment.subject_id,
                    assignment.variant,
                    assignment.assigned_at.isoformat(),
                ),
            )
            self._connection.commit()
        except sqlite3.IntegrityError as exc:
            self._connection.rollback()
            message = str(exc)
            if "experiment_assignments.id" in message:
                raise ValueError(
                    f"assignment {assignment.id!r} already exists"
                ) from exc
            if "experiment_assignments.experiment_id, experiment_assignments.subject_id" in message:
                raise ValueError(
                    f"subject {assignment.subject_id!r} already assigned to experiment "
                    f"{assignment.experiment_id!r}"
                ) from exc
            raise

    def get(self, assignment_id: str) -> ExperimentAssignment | None:
        row = self._connection.execute(
            "SELECT * FROM experiment_assignments WHERE id = ?",
            (assignment_id,),
        ).fetchone()
        if row is None:
            return None
        return self._to_domain(row)

    def list_by_experiment(
        self,
        experiment_id: str,
    ) -> tuple[ExperimentAssignment, ...]:
        rows = self._connection.execute(
            """
            SELECT * FROM experiment_assignments
            WHERE experiment_id = ?
            ORDER BY assigned_at, id
            """,
            (experiment_id,),
        ).fetchall()
        return tuple(self._to_domain(row) for row in rows)

    @staticmethod
    def _to_domain(row: sqlite3.Row) -> ExperimentAssignment:
        return ExperimentAssignment(
            id=row["id"],
            experiment_id=row["experiment_id"],
            subject_id=row["subject_id"],
            variant=row["variant"],
            assigned_at=datetime.fromisoformat(row["assigned_at"]),
        )

    def close(self) -> None:
        self._connection.close()
