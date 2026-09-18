import pytest

from app.domain.evidence import Evidence, EvidenceKind


def test_evidence_preserves_kind_statement_and_provenance():
    evidence = Evidence(
        kind=EvidenceKind.OBSERVATION,
        statement="Customers repeatedly request automated reporting.",
        source="market_research_001",
        confidence=0.8,
    )

    assert evidence.kind is EvidenceKind.OBSERVATION
    assert evidence.statement.startswith("Customers")
    assert evidence.source == "market_research_001"
    assert evidence.confidence == 0.8


def test_evidence_rejects_empty_statement():
    with pytest.raises(ValueError):
        Evidence(kind=EvidenceKind.FACT, statement="   ")


def test_evidence_rejects_invalid_confidence():
    with pytest.raises(ValueError):
        Evidence(kind=EvidenceKind.ESTIMATE, statement="estimate", confidence=1.1)
