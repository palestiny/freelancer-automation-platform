from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from .evidence_learning_handoff import EvidenceHandoffType, EvidenceLearningHandoff


@dataclass(frozen=True)
class BusinessLearningMemoryEntry:
    entry_id: str
    business_id: str
    metric_name: str
    unit: str
    category: EvidenceHandoffType
    statement: str
    source_handoff_id: str
    observation_ids: tuple[str, ...]
    recorded_at: datetime
    evidence_quality: int

    def __post_init__(self) -> None:
        for name in ("entry_id", "business_id", "metric_name", "unit", "statement", "source_handoff_id"):
            if not getattr(self, name).strip():
                raise ValueError(f"{name} cannot be empty")
        if not self.observation_ids:
            raise ValueError("observation_ids cannot be empty")
        if len(set(self.observation_ids)) != len(self.observation_ids):
            raise ValueError("observation_ids must be unique")
        if not 0 <= self.evidence_quality <= 100:
            raise ValueError("evidence_quality must be between 0 and 100")


def create_learning_memory_entry(
    *,
    handoff: EvidenceLearningHandoff,
    entry_id: str,
    recorded_at: datetime,
    evidence_quality: int,
) -> BusinessLearningMemoryEntry:
    return BusinessLearningMemoryEntry(
        entry_id=entry_id,
        business_id=handoff.business_id,
        metric_name=handoff.metric_name,
        unit=handoff.unit,
        category=handoff.handoff_type,
        statement=handoff.statement,
        source_handoff_id=handoff.handoff_id,
        observation_ids=handoff.observation_ids,
        recorded_at=recorded_at,
        evidence_quality=evidence_quality,
    )
