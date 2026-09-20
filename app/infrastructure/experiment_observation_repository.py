import sqlite3
from datetime import datetime

from app.domain.controlled_experiment_evidence import ExperimentObservation


class SQLiteExperimentObservationRepository:
    """Reference durable adapter for authoritative experiment observations."""

    def __init__(self, database: str) -> None:
        self._connection = sqlite3.connect(database)
        self._connection.row_factory = sqlite3.Row
        self._connection.execute(
            """
            CREATE TABLE IF NOT EXISTS experiment_observations (
                id TEXT PRIMARY KEY,
                experiment_id TEXT NOT NULL,
                assignment_id TEXT NOT NULL,
                subject_id TEXT NOT NULL,
                variant TEXT NOT NULL,
                metric_name TEXT NOT NULL,
                observed_value REAL NOT NULL,
                observed_at TEXT NOT NULL,
                evidence_quality INTEGER NOT NULL
            )
            """
        )
        self._connection.commit()

    def save(self, observation: ExperimentObservation) -> None:
        existing = self._connection.execute(
            "SELECT 1 FROM experiment_observations WHERE id = ?",
            (observation.id,),
        ).fetchone()
        if existing is not None:
            raise ValueError(f"observation {observation.id!r} already exists")

        try:
            self._connection.execute(
                """
                INSERT INTO experiment_observations (
                    id, experiment_id, assignment_id, subject_id, variant,
                    metric_name, observed_value, observed_at, evidence_quality
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    observation.id,
                    observation.experiment_id,
                    observation.assignment_id,
                    observation.subject_id,
                    observation.variant,
                    observation.metric_name,
                    float(observation.observed_value),
                    observation.observed_at.isoformat(),
                    observation.evidence_quality,
                ),
            )
            self._connection.commit()
        except sqlite3.IntegrityError as exc:
            self._connection.rollback()
            if "experiment_observations.id" in str(exc):
                raise ValueError(
                    f"observation {observation.id!r} already exists"
                ) from exc
            raise

    def get(self, observation_id: str) -> ExperimentObservation | None:
        row = self._connection.execute(
            "SELECT * FROM experiment_observations WHERE id = ?",
            (observation_id,),
        ).fetchone()
        return None if row is None else self._to_domain(row)

    def list_by_experiment(
        self,
        experiment_id: str,
    ) -> tuple[ExperimentObservation, ...]:
        rows = self._connection.execute(
            """
            SELECT * FROM experiment_observations
            WHERE experiment_id = ?
            ORDER BY observed_at, id
            """,
            (experiment_id,),
        ).fetchall()
        return tuple(self._to_domain(row) for row in rows)

    @staticmethod
    def _to_domain(row: sqlite3.Row) -> ExperimentObservation:
        return ExperimentObservation(
            id=row["id"],
            experiment_id=row["experiment_id"],
            assignment_id=row["assignment_id"],
            subject_id=row["subject_id"],
            variant=row["variant"],
            metric_name=row["metric_name"],
            observed_value=row["observed_value"],
            observed_at=datetime.fromisoformat(row["observed_at"]),
            evidence_quality=row["evidence_quality"],
        )

    def close(self) -> None:
        self._connection.close()
