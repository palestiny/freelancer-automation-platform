import sqlite3
from datetime import datetime

from app.domain.controlled_experiment_evidence import ExperimentExposure


class SQLiteExperimentExposureRepository:
    """Reference durable adapter for authoritative experiment exposure evidence."""

    def __init__(self, database: str) -> None:
        self._connection = sqlite3.connect(database)
        self._connection.row_factory = sqlite3.Row
        self._connection.execute(
            """
            CREATE TABLE IF NOT EXISTS experiment_exposures (
                id TEXT PRIMARY KEY,
                assignment_id TEXT NOT NULL UNIQUE,
                experiment_id TEXT NOT NULL,
                subject_id TEXT NOT NULL,
                variant TEXT NOT NULL,
                exposed_at TEXT NOT NULL
            )
            """
        )
        self._connection.commit()

    def save(self, exposure: ExperimentExposure) -> None:
        existing = self._connection.execute(
            "SELECT 1 FROM experiment_exposures WHERE id = ?",
            (exposure.id,),
        ).fetchone()
        if existing is not None:
            raise ValueError(f"exposure {exposure.id!r} already exists")

        try:
            self._connection.execute(
                """
                INSERT INTO experiment_exposures (
                    id, assignment_id, experiment_id, subject_id, variant, exposed_at
                ) VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    exposure.id,
                    exposure.assignment_id,
                    exposure.experiment_id,
                    exposure.subject_id,
                    exposure.variant,
                    exposure.exposed_at.isoformat(),
                ),
            )
            self._connection.commit()
        except sqlite3.IntegrityError as exc:
            self._connection.rollback()
            if "experiment_exposures.assignment_id" in str(exc):
                raise ValueError(
                    f"assignment {exposure.assignment_id!r} already has exposure"
                ) from exc
            raise

    def get(self, exposure_id: str) -> ExperimentExposure | None:
        row = self._connection.execute(
            "SELECT * FROM experiment_exposures WHERE id = ?",
            (exposure_id,),
        ).fetchone()
        return None if row is None else self._to_domain(row)

    def get_by_assignment(self, assignment_id: str) -> ExperimentExposure | None:
        row = self._connection.execute(
            "SELECT * FROM experiment_exposures WHERE assignment_id = ?",
            (assignment_id,),
        ).fetchone()
        return None if row is None else self._to_domain(row)

    @staticmethod
    def _to_domain(row: sqlite3.Row) -> ExperimentExposure:
        return ExperimentExposure(
            id=row["id"],
            assignment_id=row["assignment_id"],
            experiment_id=row["experiment_id"],
            subject_id=row["subject_id"],
            variant=row["variant"],
            exposed_at=datetime.fromisoformat(row["exposed_at"]),
        )

    def close(self) -> None:
        self._connection.close()
