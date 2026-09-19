from datetime import datetime, timezone
import pytest
from app.domain.explicit_evidence_decision import DecisionOutcome, ExplicitEvidenceDecision

def test_accept_decision_preserves_explicit_evidence_lineage():
    record=ExplicitEvidenceDecision(decision_id="d1",business_id="b1",outcome=DecisionOutcome.ACCEPT,evidence_context="performance_evidence",evidence_observation_ids=("a","b","c"),decided_at=datetime(2026,9,19,tzinfo=timezone.utc),rationale="Evidence met the stated decision criteria.")
    assert record.outcome is DecisionOutcome.ACCEPT
    assert record.evidence_observation_ids == ("a","b","c")

def test_decision_outcomes_are_explicit():
    assert {item.value for item in DecisionOutcome} == {"accept","reject","defer"}

@pytest.mark.parametrize("field",["decision_id","business_id","evidence_context","rationale"])
def test_required_text_fields_cannot_be_empty(field):
    base=dict(decision_id="d1",business_id="b1",outcome=DecisionOutcome.DEFER,evidence_context="performance_evidence",evidence_observation_ids=("a",),decided_at=datetime(2026,9,19,tzinfo=timezone.utc),rationale="Needs more evidence.")
    base[field]=""
    with pytest.raises(ValueError): ExplicitEvidenceDecision(**base)

def test_evidence_ids_must_be_unique():
    with pytest.raises(ValueError,match="unique"):
        ExplicitEvidenceDecision(decision_id="d1",business_id="b1",outcome=DecisionOutcome.DEFER,evidence_context="performance_evidence",evidence_observation_ids=("a","a"),decided_at=datetime(2026,9,19,tzinfo=timezone.utc),rationale="Needs more evidence.")

def test_evidence_lineage_cannot_be_empty():
    with pytest.raises(ValueError,match="cannot be empty"):
        ExplicitEvidenceDecision(decision_id="d1",business_id="b1",outcome=DecisionOutcome.REJECT,evidence_context="performance_evidence",evidence_observation_ids=(),decided_at=datetime(2026,9,19,tzinfo=timezone.utc),rationale="Evidence did not support the decision.")

def test_decision_is_immutable():
    record=ExplicitEvidenceDecision(decision_id="d1",business_id="b1",outcome=DecisionOutcome.DEFER,evidence_context="performance_evidence",evidence_observation_ids=("a",),decided_at=datetime(2026,9,19,tzinfo=timezone.utc),rationale="Need more evidence.")
    with pytest.raises(Exception): record.outcome=DecisionOutcome.ACCEPT
