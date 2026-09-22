from datetime import datetime

import pytest

from app.domain.performance_evidence_decision_support import (
    CombinedEvidencePosture,
    DescriptiveDirection,
    InferentialStatus,
    PerformanceEvidenceDecisionSupport,
)
from app.domain.statistical_evidence_learning_handoff import (
    LearningHandoffTarget,
    create_statistical_evidence_learning_handoff,
)


def evidence():
    return PerformanceEvidenceDecisionSupport(
        business_id="b1",
        metric_name="profit",
        unit="EGP",
        descriptive_direction=DescriptiveDirection.IMPROVING,
        inferential_status=InferentialStatus.STATISTICAL_DIFFERENCE_DETECTED,
        posture=CombinedEvidencePosture.DESCRIPTIVE_AND_STATISTICAL_ALIGNMENT,
        statistical_method="welch_two_sample_t_test",
        statistical_observation_ids=("s1", "s2"),
        current_observation_ids=("c1",),
        baseline_observation_ids=("b1obs",),
    )


def test_handoff_preserves_typed_posture_and_target():
    result = create_statistical_evidence_learning_handoff(
        evidence=evidence(),
        statement="Review the observed performance change.",
        target=LearningHandoffTarget.POLICY_REVIEW,
    )
    assert result.posture is CombinedEvidencePosture.DESCRIPTIVE_AND_STATISTICAL_ALIGNMENT
    assert result.target is LearningHandoffTarget.POLICY_REVIEW


def test_handoff_rejects_empty_lineage_ids():
    from app.domain.statistical_evidence_learning_handoff import StatisticalEvidenceLearningHandoff

    with pytest.raises(ValueError):
        StatisticalEvidenceLearningHandoff(
            business_id="b1",
            metric_name="profit",
            unit="EGP",
            statement="Review the observed performance change.",
            target=LearningHandoffTarget.POLICY_REVIEW,
            descriptive_direction=DescriptiveDirection.IMPROVING,
            inferential_status=InferentialStatus.STATISTICAL_DIFFERENCE_DETECTED,
            posture=CombinedEvidencePosture.DESCRIPTIVE_AND_STATISTICAL_ALIGNMENT,
            statistical_method="welch_two_sample_t_test",
            statistical_observation_ids=("", "s2"),
            current_observation_ids=("c1",),
            baseline_observation_ids=("b1obs",),
        )

def test_handoff_rejects_invalid_target():
    with pytest.raises((TypeError, ValueError)):
        create_statistical_evidence_learning_handoff(
            evidence=evidence(),
            statement="Review the observed performance change.",
            target="policy_review",
        )
