from datetime import datetime, timezone

import pytest

from app.domain.evidence_decision_record import (
    DecisionOutcome,
    EvidenceDecisionRecord,
)


def _record(**overrides):
    values = dict(
        id="d1",
        business_id="b1",
        outcome=DecisionOutcome.ACCEPT,
        statement="Continue operating the business.",
        rationale="Evidence supports continued operation.",
        evidence_ids=("e1", "e2"),
        decided_at=datetime(2026, 9, 19, tzinfo=timezone.utc),
        decision_maker_id="operator-1",
    )
    values.update(overrides)
    return EvidenceDecisionRecord(**values)


def test_records_explicit_decision_and_evidence_lineage():
    result = _record()
    assert result.outcome is DecisionOutcome.ACCEPT
    assert result.evidence_ids == ("e1", "e2")
    assert result.decision_maker_id == "operator-1"


@pytest.mark.parametrize(
    "field,value",
    [
        ("id", ""),
        ("business_id", ""),
        ("statement", ""),
        ("rationale", ""),
        ("decision_maker_id", ""),
    ],
)
def test_required_text_fields_are_validated(field, value):
    with pytest.raises(ValueError):
        _record(**{field: value})


def test_evidence_ids_must_be_non_empty_and_unique():
    with pytest.raises(ValueError):
        _record(evidence_ids=())
    with pytest.raises(ValueError):
        _record(evidence_ids=("e1", "e1"))


def test_decision_outcome_is_required_enum():
    with pytest.raises(TypeError):
        _record(outcome="accept")


def test_decided_at_must_be_datetime():
    with pytest.raises(TypeError):
        _record(decided_at="2026-09-19")


def test_evidence_ids_must_be_tuple():
    with pytest.raises(TypeError):
        _record(evidence_ids=["e1", "e2"])
