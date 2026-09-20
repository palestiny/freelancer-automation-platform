from datetime import datetime, timezone

import pytest

from app.domain.business_learning_memory import (
    BusinessLearningMemoryEntry,
    create_learning_memory_entry,
)
from app.domain.evidence_learning_handoff import EvidenceHandoffType, EvidenceLearningHandoff


def _handoff():
    return EvidenceLearningHandoff(
        handoff_id="handoff-1",
        business_id="b1",
        metric_name="profit",
        unit="EGP",
        handoff_type=EvidenceHandoffType.POLICY_REVIEW,
        target="profit expectation",
        statement="Review the operating assumption against observed evidence.",
        observation_ids=("obs-1", "obs-2"),
    )


def test_memory_entry_preserves_handoff_lineage_and_context():
    recorded_at = datetime(2026, 9, 20, tzinfo=timezone.utc)
    result = create_learning_memory_entry(
        handoff=_handoff(),
        entry_id="mem-1",
        recorded_at=recorded_at,
        evidence_quality=80,
    )

    assert result == BusinessLearningMemoryEntry(
        entry_id="mem-1",
        business_id="b1",
        metric_name="profit",
        unit="EGP",
        category=EvidenceHandoffType.POLICY_REVIEW,
        statement="Review the operating assumption against observed evidence.",
        source_handoff_id="handoff-1",
        observation_ids=("obs-1", "obs-2"),
        recorded_at=recorded_at,
        evidence_quality=80,
    )


def test_memory_entry_rejects_empty_lineage():
    with pytest.raises(ValueError, match="observation_ids"):
        BusinessLearningMemoryEntry(
            entry_id="mem-1",
            business_id="b1",
            metric_name="profit",
            unit="EGP",
            category=EvidenceHandoffType.POLICY_REVIEW,
            statement="statement",
            source_handoff_id="handoff-1",
            observation_ids=(),
            recorded_at=datetime(2026, 9, 20, tzinfo=timezone.utc),
            evidence_quality=80,
        )


def test_memory_entry_rejects_invalid_evidence_quality():
    with pytest.raises(ValueError, match="evidence_quality"):
        BusinessLearningMemoryEntry(
            entry_id="mem-1",
            business_id="b1",
            metric_name="profit",
            unit="EGP",
            category=EvidenceHandoffType.EXPERIMENT,
            statement="statement",
            source_handoff_id="handoff-1",
            observation_ids=("obs-1",),
            recorded_at=datetime(2026, 9, 20, tzinfo=timezone.utc),
            evidence_quality=101,
        )


def test_memory_entry_is_immutable():
    entry = create_learning_memory_entry(
        handoff=_handoff(),
        entry_id="mem-1",
        recorded_at=datetime(2026, 9, 20, tzinfo=timezone.utc),
        evidence_quality=80,
    )
    with pytest.raises(Exception):
        entry.evidence_quality = 90
