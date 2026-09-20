from datetime import datetime, timezone

from app.domain.business_learning_memory import BusinessLearningMemoryEntry
from app.domain.evidence_learning_handoff import EvidenceHandoffType
from app.domain.business_learning_memory_review_context import build_learning_memory_review_context


def _entry(entry_id, metric="profit", quality=80, when=None, category=EvidenceHandoffType.POLICY_REVIEW):
    return BusinessLearningMemoryEntry(
        entry_id=entry_id,
        business_id="b1",
        metric_name=metric,
        unit="EGP",
        category=category,
        statement=entry_id,
        source_handoff_id=f"h-{entry_id}",
        observation_ids=(f"o-{entry_id}",),
        recorded_at=when or datetime(2026, 1, 2, tzinfo=timezone.utc),
        evidence_quality=quality,
    )


def test_review_context_is_deterministic_and_business_isolated():
    result = build_learning_memory_review_context(
        business_id="b1",
        entries=(
            _entry("late", quality=70, when=datetime(2026, 1, 3, tzinfo=timezone.utc)),
            _entry("early", quality=90, when=datetime(2026, 1, 1, tzinfo=timezone.utc)),
            BusinessLearningMemoryEntry(
                entry_id="other",
                business_id="b2",
                metric_name="profit",
                unit="EGP",
                category=EvidenceHandoffType.EXPERIMENT,
                statement="other",
                source_handoff_id="h-other",
                observation_ids=("o-other",),
                recorded_at=datetime(2026, 1, 2, tzinfo=timezone.utc),
                evidence_quality=10,
            ),
        ),
    )
    assert result.entry_ids == ("early", "late")
    assert result.entry_count == 2
    assert result.minimum_evidence_quality == 70
    assert result.average_evidence_quality == 80
    assert result.latest_recorded_at == datetime(2026, 1, 3, tzinfo=timezone.utc)
    assert result.metrics == (("profit", "EGP"),)


def test_empty_review_context_is_explicit():
    result = build_learning_memory_review_context(business_id="b1", entries=())
    assert result.entry_count == 0
    assert result.entry_ids == ()
    assert result.latest_recorded_at is None
    assert result.minimum_evidence_quality is None
    assert result.average_evidence_quality is None
    assert result.metrics == ()
