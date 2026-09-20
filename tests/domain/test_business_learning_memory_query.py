from datetime import datetime, timezone

import pytest

from app.domain.business_learning_memory import BusinessLearningMemoryEntry
from app.domain.evidence_learning_handoff import EvidenceHandoffType
from app.domain.business_learning_memory_query import query_learning_memory


def _entry(entry_id, business_id="b1", metric="profit", when=None, category=EvidenceHandoffType.POLICY_REVIEW):
    return BusinessLearningMemoryEntry(
        entry_id=entry_id,
        business_id=business_id,
        metric_name=metric,
        unit="EGP",
        category=category,
        statement=entry_id,
        source_handoff_id=f"h-{entry_id}",
        observation_ids=(f"o-{entry_id}",),
        recorded_at=when or datetime(2026, 1, 2, tzinfo=timezone.utc),
        evidence_quality=80,
    )


def test_query_is_business_isolated_and_chronological():
    result = query_learning_memory(
        entries=(
            _entry("late", when=datetime(2026, 1, 3, tzinfo=timezone.utc)),
            _entry("other", business_id="b2"),
            _entry("early", when=datetime(2026, 1, 1, tzinfo=timezone.utc)),
        ),
        business_id="b1",
    )
    assert tuple(e.entry_id for e in result) == ("early", "late")


def test_query_filters_metric_and_category_and_uses_end_exclusive_window():
    result = query_learning_memory(
        entries=(
            _entry("inside", when=datetime(2026, 1, 2, tzinfo=timezone.utc)),
            _entry("at_end", when=datetime(2026, 1, 3, tzinfo=timezone.utc)),
            _entry("other_metric", metric="revenue"),
            _entry("experiment", category=EvidenceHandoffType.EXPERIMENT),
        ),
        business_id="b1",
        metric_name="profit",
        unit="EGP",
        handoff_type=EvidenceHandoffType.POLICY_REVIEW,
        start=datetime(2026, 1, 1, tzinfo=timezone.utc),
        end=datetime(2026, 1, 3, tzinfo=timezone.utc),
    )
    assert tuple(e.entry_id for e in result) == ("inside",)


def test_duplicate_entry_ids_are_rejected():
    with pytest.raises(ValueError, match="unique"):
        query_learning_memory(
            entries=(_entry("same"), _entry("same")),
            business_id="b1",
        )


def test_invalid_window_is_rejected():
    with pytest.raises(ValueError, match="end must be after start"):
        query_learning_memory(
            entries=(_entry("one"),),
            business_id="b1",
            start=datetime(2026, 1, 3, tzinfo=timezone.utc),
            end=datetime(2026, 1, 2, tzinfo=timezone.utc),
        )
