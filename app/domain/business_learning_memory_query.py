from datetime import datetime
from typing import Iterable

from .business_learning_memory import BusinessLearningMemoryEntry
from .evidence_learning_handoff import EvidenceHandoffType


def query_learning_memory(
    *,
    entries: Iterable[BusinessLearningMemoryEntry],
    business_id: str,
    metric_name: str | None = None,
    unit: str | None = None,
    handoff_type: EvidenceHandoffType | None = None,
    start: datetime | None = None,
    end: datetime | None = None,
) -> tuple[BusinessLearningMemoryEntry, ...]:
    if not business_id.strip():
        raise ValueError("business_id cannot be empty")
    if metric_name is not None and not metric_name.strip():
        raise ValueError("metric_name cannot be empty")
    if unit is not None and not unit.strip():
        raise ValueError("unit cannot be empty")
    if (start is None) != (end is None):
        raise ValueError("start and end must be supplied together")
    if start is not None and end is not None and end <= start:
        raise ValueError("end must be after start")

    materialized = tuple(entries)
    entry_ids = tuple(entry.entry_id for entry in materialized)
    if len(set(entry_ids)) != len(entry_ids):
        raise ValueError("entries must have unique entry ids")

    result = [
        entry for entry in materialized
        if entry.business_id == business_id
        and (metric_name is None or entry.metric_name == metric_name)
        and (unit is None or entry.unit == unit)
        and (handoff_type is None or entry.category is handoff_type)
        and (start is None or start <= entry.recorded_at < end)
    ]
    return tuple(sorted(result, key=lambda entry: (entry.recorded_at, entry.entry_id)))
