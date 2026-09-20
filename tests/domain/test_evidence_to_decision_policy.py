import pytest

from app.domain.evidence_to_decision_policy import (
    DecisionSupportOutcome,
    EvidenceToDecisionPolicy,
    evaluate_evidence_to_decision,
)


def test_policy_requires_explicit_minimum_evidence_quality():
    policy = EvidenceToDecisionPolicy(minimum_evidence_quality=70)
    result = evaluate_evidence_to_decision(
        evidence_eligible=True,
        evidence_quality=80,
        statistical_difference_detected=True,
        policy=policy,
    )
    assert result.outcome is DecisionSupportOutcome.SUPPORTS


def test_insufficient_evidence_cannot_become_a_positive_decision():
    policy = EvidenceToDecisionPolicy(minimum_evidence_quality=70)
    result = evaluate_evidence_to_decision(
        evidence_eligible=False,
        evidence_quality=90,
        statistical_difference_detected=True,
        policy=policy,
    )
    assert result.outcome is DecisionSupportOutcome.INSUFFICIENT_EVIDENCE


def test_policy_can_require_statistical_difference():
    policy = EvidenceToDecisionPolicy(
        minimum_evidence_quality=70,
        require_statistical_difference=True,
    )
    result = evaluate_evidence_to_decision(
        evidence_eligible=True,
        evidence_quality=80,
        statistical_difference_detected=False,
        policy=policy,
    )
    assert result.outcome is DecisionSupportOutcome.DOES_NOT_SUPPORT


def test_invalid_policy_threshold_is_rejected():
    with pytest.raises(ValueError):
        EvidenceToDecisionPolicy(minimum_evidence_quality=101)
