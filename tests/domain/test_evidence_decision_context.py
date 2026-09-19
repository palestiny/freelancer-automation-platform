import pytest

from app.domain.evidence_decision_context import (
    EvidenceDecisionContext,
    build_evidence_decision_context,
)
from app.domain.performance_evidence_decision_support import (
    CombinedEvidencePosture,
    DescriptiveDirection,
    InferentialStatus,
    PerformanceEvidenceDecisionSupport,
)


def _support():
    return PerformanceEvidenceDecisionSupport(
        business_id="b1",
        metric_name="profit",
        unit="EGP",
        descriptive_direction=DescriptiveDirection.IMPROVING,
        inferential_status=InferentialStatus.STATISTICAL_DIFFERENCE_DETECTED,
        posture=CombinedEvidencePosture.DESCRIPTIVE_AND_STATISTICAL_ALIGNMENT,
        statistical_observation_ids=("a", "b", "c", "d"),
    )


def test_context_preserves_support_and_provenance():
    result = build_evidence_decision_context(
        support=_support(),
        source_references=("performance_trend:1", "statistical_evidence:2"),
        current_evidence_quality=80,
        baseline_evidence_quality=75,
    )
    assert isinstance(result, EvidenceDecisionContext)
    assert result.posture is CombinedEvidencePosture.DESCRIPTIVE_AND_STATISTICAL_ALIGNMENT
    assert result.source_references == ("performance_trend:1", "statistical_evidence:2")
    assert result.statistical_observation_ids == ("a", "b", "c", "d")


def test_missing_source_references_are_rejected():
    with pytest.raises(ValueError):
        build_evidence_decision_context(
            support=_support(),
            source_references=(),
            current_evidence_quality=80,
            baseline_evidence_quality=75,
        )


@pytest.mark.parametrize("value", [-1, 101])
def test_evidence_quality_is_bounded(value):
    with pytest.raises(ValueError):
        build_evidence_decision_context(
            support=_support(),
            source_references=("performance_trend:1",),
            current_evidence_quality=value,
            baseline_evidence_quality=75,
        )
