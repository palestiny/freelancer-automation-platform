from dataclasses import dataclass
from datetime import datetime
from typing import Iterable

from .business_learning_memory import BusinessLearningMemoryEntry
from .evidence_learning_handoff import EvidenceHandoffType


@dataclass(frozen=True)
class BusinessLearningMemoryReviewContext:
    business_id: str
    entry_ids: tuple[str, ...]
    entry_count: int
    metrics: tuple[tuple[str, str], ...]
    latest_recorded_at: datetime | None
    minimum_evidence_quality: int | None
    average_evidence_quality: int | None
    handoff_categories: tuple[EvidenceHandoffType, ...]

    def __post_init__(self) -> None:
        if not self.business_id.strip():
            raise ValueError("business_id cannot be empty")
        if self.entry_count != len(self.entry_ids):
            raise ValueError("entry_count must match entry_ids")
        if len(set(self.entry_ids)) != len(self.entry_ids):
            raise ValueError("entry_ids must be unique")
        if self.minimum_evidence_quality is not None and not 0 <= self.minimum_evidence_quality <= 100:
            raise ValueError("minimum_evidence_quality must be between 0 and 100")
        if self.average_evidence_quality is not None and not 0 <= self.average_evidence_quality <= 100:
            raise ValueError("average_evidence_quality must be between 0 and 100")
        if self.entry_count == 0 and (self.latest_recorded_at is not None or self.minimum_evidence_quality is not None or self.average_evidence_quality is not None or self.metrics or self.handoff_categories):
            raise ValueError("empty context cannot contain derived values")
        if self.entry_count > 0 and (self.latest_recorded_at is None or self.minimum_evidence_quality is None or self.average_evidence_quality is None):
            raise ValueError("non-empty context requires derived values")


def build_learning_memory_review_context(*, business_id: str, entries: Iterable[BusinessLearningMemoryEntry]) -> BusinessLearningMemoryReviewContext:
    if not business_id.strip():
        raise ValueError("business_id cannot be empty")
    materialized = tuple(entries)
    selected = tuple(entry for entry in materialized if entry.business_id == business_id)
    ids = tuple(entry.entry_id for entry in selected)
    if len(set(ids)) != len(ids):
        raise ValueError("entries must have unique entry ids")
    ordered = tuple(sorted(selected, key=lambda entry: (entry.recorded_at, entry.entry_id)))
    qualities = tuple(entry.evidence_quality for entry in ordered)
    metrics = tuple(sorted({(entry.metric_name, entry.unit) for entry in ordered}))
    categories = tuple(sorted({entry.category for entry in ordered}, key=lambda category: category.value))
    return BusinessLearningMemoryReviewContext(
        business_id=business_id,
        entry_ids=tuple(entry.entry_id for entry in ordered),
        entry_count=len(ordered),
        metrics=metrics,
        latest_recorded_at=ordered[-1].recorded_at if ordered else None,
        minimum_evidence_quality=min(qualities) if qualities else None,
        average_evidence_quality=round(sum(qualities) / len(qualities)) if qualities else None,
        handoff_categories=categories,
    )
