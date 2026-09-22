from app.domain.performance_history import PerformanceWindow
from datetime import datetime
import pytest

from app.domain.performance_evidence_decision_support import (
    CombinedEvidencePosture,
    DescriptiveDirection,
    InferentialStatus,
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
        descriptive_direction=DescriptiveDirection.IMPROVING,
        inferential_status=InferentialStatus.STATISTICAL_DIFFERENCE_DETECTED if eligible else InferentialStatus.UNAVAILABLE,
        posture=CombinedEvidencePosture.DESCRIPTIVE_CHANGE_WITH_STATISTICAL_DETECTION if eligible else CombinedEvidencePosture.INFERENTIAL_EVIDENCE_UNAVAILABLE,
        statistical_observation_ids=("a", "b"),
        statistical_method="welch_two_sample_t_test",
        statistical_first_window=PerformanceWindow(datetime(2026, 1, 25), datetime(2026, 2, 1)),
        statistical_second_window=PerformanceWindow(datetime(2026, 2, 1), datetime(2026, 2, 8)),
        statistical_difference_direction=DescriptiveDirection.IMPROVING,
        current_observation_ids=("c",),
        baseline_observation_ids=("d",),
        statistical_difference_direction=DescriptiveDirection.IMPROVING if eligible else DescriptiveDirection.UNAVAILABLE,
    )


def test_eligible_evidence_creates_explicit_policy_review_handoff():
    result = create_evidence_learning_handoff(
        handoff_id="handoff-1",
        evidence=_support(),
        handoff_type=EvidenceHandoffType.POLICY_REVIEW,
        target="profit expectation",
        statement="Historical evidence should be reviewed against the current operating policy.",
    )
    assert result.handoff_id == "handoff-1"
    assert result.business_id == "b1"
    assert result.handoff_type is EvidenceHandoffType.POLICY_REVIEW
    assert result.observation_ids == ("a", "b")


def test_ineligible_evidence_cannot_be_handed_off():
    with pytest.raises(ValueError, match="eligible"):
        create_evidence_learning_handoff(
            handoff_id="handoff-2",
            evidence=_support(eligible=False),
            handoff_type=EvidenceHandoffType.EXPERIMENT,
            target="profit expectation",
            statement="Test a revised operating assumption.",
        )


def test_handoff_requires_explicit_identity():
    with pytest.raises(ValueError, match="handoff_id"):
        create_evidence_learning_handoff(
            handoff_id=" ",
            evidence=_support(),
            handoff_type=EvidenceHandoffType.POLICY_REVIEW,
            target="profit expectation",
            statement="Review evidence.",
        )
