from datetime import datetime

from app.domain.performance_evidence_decision_support import (
    CombinedEvidencePosture,
    DescriptiveDirection,
    InferentialStatus,
    PerformanceEvidenceDecisionSupport,
)
from app.domain.performance_history import PerformanceWindow
from app.domain.evidence_decision_support import create_decision_support_evidence
from app.domain.performance_reliability import SourceReliabilityAssessment, SourceReliabilityReason
from app.domain.statistical_evidence_composition import StatisticalEvidenceEligibilityReason, StatisticalEvidenceInterpretation


def _evidence(posture):
    window1 = PerformanceWindow(datetime(2026, 1, 1), datetime(2026, 1, 8))
    window2 = PerformanceWindow(datetime(2026, 1, 8), datetime(2026, 1, 15))
    eligible = posture is not CombinedEvidencePosture.CONTEXT_INVALID
    return PerformanceEvidenceDecisionSupport(
        business_id="b1",
        metric_name="profit",
        unit="EGP",
        descriptive_direction=DescriptiveDirection.IMPROVING,
        inferential_status=InferentialStatus.STATISTICAL_DIFFERENCE_DETECTED,
        posture=posture,
        statistical_observation_ids=("a", "b", "c"),
        statistical_difference_direction=DescriptiveDirection.IMPROVING,
        current_observation_ids=("c",),
        baseline_observation_ids=("a", "b"),
    )


def test_valid_evidence_is_handed_to_policy_review_without_authorizing_action():
    result = create_decision_support_evidence(_evidence(
        CombinedEvidencePosture.DESCRIPTIVE_CHANGE_WITH_STATISTICAL_DETECTION
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
