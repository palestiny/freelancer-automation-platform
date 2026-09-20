import sqlite3
from datetime import datetime

from app.domain.business_performance import (
    BusinessPerformanceObservation,
    PerformanceSourceType,
)


class SQLitePerformanceObservationRepository:
    """Reference durable adapter for authoritative performance observations."""

    def __init__(self, database: str) -> None:
        self._connection = sqlite3.connect(database)
        self._connection.row_factory = sqlite3.Row
        self._connection.execute(
            """
            CREATE TABLE IF NOT EXISTS performance_observations (
                id TEXT PRIMARY KEY,
                business_id TEXT NOT NULL,
                source_type TEXT NOT NULL,
                source_id TEXT NOT NULL,
                metric_name TEXT NOT NULL,
                unit TEXT NOT NULL,
                expected_value REAL,
                actual_value REAL NOT NULL,
                observed_at TEXT NOT NULL,
                evidence_quality INTEGER NOT NULL
            )
            """
        )
        self._connection.commit()

    def save(self, observation: BusinessPerformanceObservation) -> None:
        try:
            self._connection.execute(
                """
                INSERT INTO performance_observations (
                    id, business_id, source_type, source_id, metric_name, unit,
                    expected_value, actual_value, observed_at, evidence_quality
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    observation.id,
                    observation.business_id,
                    observation.source_type.value,
                    observation.source_id,
                    observation.metric_name,
                    observation.unit,
                    observation.expected_value,
                    observation.actual_value,
                    observation.observed_at.isoformat(),
                    observation.evidence_quality,
                ),
            )
            self._connection.commit()
        except sqlite3.IntegrityError as exc:
            self._connection.rollback()
            if "performance_observations.id" in str(exc):
                raise ValueError(
                    f"observation {observation.id!r} already exists"
                ) from exc
            raise

    def get(self, observation_id: str) -> BusinessPerformanceObservation | None:
        row = self._connection.execute(
            "SELECT * FROM performance_observations WHERE id = ?",
            (observation_id,),
        ).fetchone()
        if row is None:
            return None
        return self._to_domain(row)

    def list_by_business(
        self,
        business_id: str,
    ) -> tuple[BusinessPerformanceObservation, ...]:
        rows = self._connection.execute(
            """
            SELECT * FROM performance_observations
            WHERE business_id = ?
            ORDER BY observed_at, id
            """,
            (business_id,),
        ).fetchall()
        return tuple(self._to_domain(row) for row in rows)

    @staticmethod
    def _to_domain(row: sqlite3.Row) -> BusinessPerformanceObservation:
        return BusinessPerformanceObservation(
            id=row["id"],
            business_id=row["business_id"],
            source_type=PerformanceSourceType(row["source_type"]),
            source_id=row["source_id"],
            metric_name=row["metric_name"],
            unit=row["unit"],
            expected_value=row["expected_value"],
            actual_value=row["actual_value"],
            observed_at=datetime.fromisoformat(row["observed_at"]),
            evidence_quality=row["evidence_quality"],
        )

    def close(self) -> None:
        self._connection.close()
