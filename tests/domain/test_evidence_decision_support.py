from app.domain.performance_evidence_decision_support import (
    CombinedEvidencePosture,
    DescriptiveDirection,
    InferentialStatus,
    PerformanceEvidenceDecisionSupport,
)
from app.domain.evidence_decision_support import create_decision_support_evidence


def _evidence(posture):
    return PerformanceEvidenceDecisionSupport(
        business_id="b1",
        metric_name="profit",
        unit="EGP",
        descriptive_direction=DescriptiveDirection.IMPROVING,
        inferential_status=InferentialStatus.STATISTICAL_DIFFERENCE_DETECTED,
        posture=posture,
        statistical_observation_ids=("a", "b", "c"),
    )


def test_valid_evidence_is_handed_to_policy_review_without_authorizing_action():
    result = create_decision_support_evidence(_evidence(
        CombinedEvidencePosture.DESCRIPTIVE_AND_STATISTICAL_ALIGNMENT
    ))
    assert result.requires_policy_review is True
    assert result.observation_ids == ("a", "b", "c")


def test_context_invalid_evidence_cannot_be_handed_off():
    result = create_decision_support_evidence(_evidence(
        CombinedEvidencePosture.CONTEXT_INVALID
    ))
    assert result.requires_policy_review is False


def test_handoff_preserves_evidence_posture():
    posture = CombinedEvidencePosture.DESCRIPTIVE_CHANGE_WITHOUT_STATISTICAL_DETECTION
    result = create_decision_support_evidence(_evidence(posture))
    assert result.posture is posture
