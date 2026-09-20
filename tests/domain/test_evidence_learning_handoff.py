import pytest

from app.domain.performance_evidence_decision_support import (
    CombinedEvidencePosture,
    PerformanceEvidenceDecisionSupport,
)
from app.domain.evidence_learning_handoff import (
    EvidenceHandoffType,
    create_evidence_learning_handoff,
)


def _support(*, eligible=True):
    return PerformanceEvidenceDecisionSupport(
        business_id="b1",
        metric_name="profit",
        unit="EGP",
        descriptive_direction=__import__("app.domain.performance_evidence_decision_support", fromlist=["DescriptiveDirection"]).DescriptiveDirection.IMPROVING,
        inferential_status=__import__("app.domain.performance_evidence_decision_support", fromlist=["InferentialStatus"]).InferentialStatus.STATISTICAL_DIFFERENCE_DETECTED if eligible else __import__("app.domain.performance_evidence_decision_support", fromlist=["InferentialStatus"]).InferentialStatus.UNAVAILABLE,
        posture=CombinedEvidencePosture.DESCRIPTIVE_AND_STATISTICAL_ALIGNMENT if eligible else CombinedEvidencePosture.INFERENTIAL_EVIDENCE_UNAVAILABLE,
        statistical_observation_ids=("a", "b"),
    )


def test_eligible_evidence_creates_explicit_policy_review_handoff():
    result = create_evidence_learning_handoff(
        evidence=_support(),
        handoff_type=EvidenceHandoffType.POLICY_REVIEW,
        target="profit expectation",
        statement="Historical evidence should be reviewed against the current operating policy.",
    )
    assert result.business_id == "b1"
    assert result.handoff_type is EvidenceHandoffType.POLICY_REVIEW
    assert result.observation_ids == ("a", "b")


def test_ineligible_evidence_cannot_be_handed_off():
    with pytest.raises(ValueError, match="eligible"):
        create_evidence_learning_handoff(
            evidence=_support(eligible=False),
            handoff_type=EvidenceHandoffType.EXPERIMENT,
            target="profit expectation",
            statement="Test a revised operating assumption.",
        )
