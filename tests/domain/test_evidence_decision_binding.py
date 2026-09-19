from datetime import datetime, timezone

from app.domain.evidence_decision_context import EvidenceDecisionContext
from app.domain.evidence_decision_record import DecisionOutcome
from app.domain.performance_evidence_decision_support import (
    CombinedEvidencePosture,
    DescriptiveDirection,
    InferentialStatus,
)
from app.domain.evidence_decision_binding import record_evidence_decision


def _context():
    return EvidenceDecisionContext(
        business_id="b1",
        metric_name="profit",
        unit="EGP",
        descriptive_direction=DescriptiveDirection.IMPROVING,
        inferential_status=InferentialStatus.STATISTICAL_DIFFERENCE_DETECTED,
        posture=CombinedEvidencePosture.DESCRIPTIVE_CHANGE_WITH_STATISTICAL_DETECTION,
        statistical_observation_ids=("stat-1", "stat-2"),
        current_observation_ids=("current-1",),
        baseline_observation_ids=("baseline-1",),
        source_references=("trend-1", "statistical-evidence-1"),
        current_evidence_quality=80,
        baseline_evidence_quality=75,
    )


def test_records_explicit_decision_bound_to_context():
    result = record_evidence_decision(
        context=_context(),
        record_id="decision-1",
        outcome=DecisionOutcome.ACCEPT,
        statement="Continue operating.",
        rationale="The recorded evidence supports the supplied decision.",
        decision_maker_id="operator-1",
        decided_at=datetime(2026, 9, 19, tzinfo=timezone.utc),
    )

    assert result.business_id == "b1"
    assert result.outcome is DecisionOutcome.ACCEPT
    assert result.evidence_ids == (
        "trend-1",
        "statistical-evidence-1",
        "stat-1",
        "stat-2",
        "current-1",
        "baseline-1",
    )


def test_context_business_identity_cannot_be_overridden():
    context = _context()
    result = record_evidence_decision(
        context=context,
        record_id="decision-1",
        outcome=DecisionOutcome.DEFER,
        statement="Defer.",
        rationale="Need more evidence.",
        decision_maker_id="operator-1",
        decided_at=datetime(2026, 9, 19, tzinfo=timezone.utc),
    )
    assert result.business_id == context.business_id
