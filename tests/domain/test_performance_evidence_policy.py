from app.domain.performance_evidence_decision_support import (
    CombinedEvidencePosture,
    DescriptiveDirection,
    InferentialStatus,
    PerformanceEvidenceDecisionSupport,
)
from app.domain.performance_evidence_policy import (
    PerformanceEvidencePolicyState,
    assess_performance_evidence_policy,
)


def _support(posture, direction=DescriptiveDirection.IMPROVING):
    return PerformanceEvidenceDecisionSupport(
        business_id="b1",
        metric_name="profit",
        unit="EGP",
        descriptive_direction=direction,
        inferential_status=InferentialStatus.STATISTICAL_DIFFERENCE_DETECTED,
        posture=posture,
        statistical_observation_ids=("a", "b"),
    )


def test_aligned_improvement_supports_improvement():
    result = assess_performance_evidence_policy(
        support=_support(CombinedEvidencePosture.DESCRIPTIVE_AND_STATISTICAL_ALIGNMENT)
    )
    assert result.state is PerformanceEvidencePolicyState.SUPPORTS_IMPROVEMENT


def test_aligned_decline_supports_decline():
    result = assess_performance_evidence_policy(
        support=_support(
            CombinedEvidencePosture.DESCRIPTIVE_AND_STATISTICAL_ALIGNMENT,
            DescriptiveDirection.DECLINING,
        )
    )
    assert result.state is PerformanceEvidencePolicyState.SUPPORTS_DECLINE


def test_descriptive_only_change_is_not_presented_as_statistically_supported():
    result = assess_performance_evidence_policy(
        support=_support(CombinedEvidencePosture.DESCRIPTIVE_CHANGE_WITHOUT_STATISTICAL_DETECTION)
    )
    assert result.state is PerformanceEvidencePolicyState.DESCRIPTIVE_CHANGE_ONLY


def test_unavailable_inference_is_insufficient_evidence():
    result = assess_performance_evidence_policy(
        support=_support(CombinedEvidencePosture.INFERENTIAL_EVIDENCE_UNAVAILABLE)
    )
    assert result.state is PerformanceEvidencePolicyState.EVIDENCE_INSUFFICIENT


def test_context_invalid_remains_explicit():
    result = assess_performance_evidence_policy(
        support=_support(CombinedEvidencePosture.CONTEXT_INVALID)
    )
    assert result.state is PerformanceEvidencePolicyState.CONTEXT_INVALID
