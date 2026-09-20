import pytest

from app.domain.evidence_to_decision_policy import (
    DecisionSupportOutcome,
    EvidenceToDecisionPolicy,
    evaluate_evidence_to_decision,
)


def test_policy_requires_explicit_minimum_evidence_quality():
    policy = EvidenceToDecisionPolicy(policy_id="growth-v1", version="1.0", minimum_evidence_quality=70)
    result = evaluate_evidence_to_decision(
        evidence_id="evidence-1",
        observation_ids=("obs-1", "obs-2"),
        evidence_eligible=True,
        evidence_quality=80,
        statistical_difference_detected=True,
        policy=policy,
    )
    assert result.outcome is DecisionSupportOutcome.SUPPORTS
    assert result.policy_id == "growth-v1"
    assert result.policy_version == "1.0"


def test_insufficient_evidence_cannot_become_a_positive_decision():
    policy = EvidenceToDecisionPolicy(policy_id="growth-v1", version="1.0", minimum_evidence_quality=70)
    result = evaluate_evidence_to_decision(
        evidence_id="evidence-1",
        observation_ids=("obs-1", "obs-2"),
        evidence_eligible=False,
        evidence_quality=90,
        statistical_difference_detected=True,
        policy=policy,
    )
    assert result.outcome is DecisionSupportOutcome.INSUFFICIENT_EVIDENCE


def test_policy_can_require_statistical_difference():
    policy = EvidenceToDecisionPolicy(
        policy_id="growth-v1",
        version="1.0",
        minimum_evidence_quality=70,
        require_statistical_difference=True,
    )
    result = evaluate_evidence_to_decision(
        evidence_id="evidence-1",
        observation_ids=("obs-1", "obs-2"),
        evidence_eligible=True,
        evidence_quality=80,
        statistical_difference_detected=False,
        policy=policy,
    )
    assert result.outcome is DecisionSupportOutcome.DOES_NOT_SUPPORT


def test_invalid_policy_threshold_is_rejected():
    with pytest.raises(ValueError):
        EvidenceToDecisionPolicy(policy_id="growth-v1", version="1.0", minimum_evidence_quality=101)


def test_policy_identity_is_required():
    with pytest.raises(ValueError):
        EvidenceToDecisionPolicy(policy_id="", version="1.0")
    with pytest.raises(ValueError):
        EvidenceToDecisionPolicy(policy_id="growth-v1", version="")


def test_decision_support_preserves_evidence_lineage():
    policy = EvidenceToDecisionPolicy(policy_id="growth-v1", version="1.0")
    result = evaluate_evidence_to_decision(
        evidence_id="evidence-1",
        observation_ids=("obs-1", "obs-2"),
        evidence_eligible=True,
        evidence_quality=80,
        statistical_difference_detected=True,
        policy=policy,
    )
    assert result.evidence_id == "evidence-1"
    assert result.observation_ids == ("obs-1", "obs-2")


def test_duplicate_observation_lineage_is_rejected():
    policy = EvidenceToDecisionPolicy(policy_id="growth-v1", version="1.0")
    with pytest.raises(ValueError):
        evaluate_evidence_to_decision(
            evidence_id="evidence-1",
            observation_ids=("obs-1", "obs-1"),
            evidence_eligible=True,
            evidence_quality=80,
            statistical_difference_detected=True,
            policy=policy,
        )


def test_empty_evidence_identity_is_rejected():
    policy = EvidenceToDecisionPolicy(policy_id="growth-v1", version="1.0")
    with pytest.raises(ValueError):
        evaluate_evidence_to_decision(
            evidence_id="",
            observation_ids=("obs-1",),
            evidence_eligible=True,
            evidence_quality=80,
            statistical_difference_detected=True,
            policy=policy,
        )
