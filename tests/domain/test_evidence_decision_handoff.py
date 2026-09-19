from app.domain.performance_evidence_decision_support import (
    CombinedEvidencePosture,
    DescriptiveDirection,
    InferentialStatus,
    PerformanceEvidenceDecisionSupport,
)
from app.domain.evidence_decision_handoff import (
    EvidenceHandoffStatus,
    handoff_evidence_for_review,
)


def _support(
    posture: CombinedEvidencePosture,
    inferential: InferentialStatus = InferentialStatus.STATISTICAL_DIFFERENCE_DETECTED,
):
    return PerformanceEvidenceDecisionSupport(
        business_id="b1",
        metric_name="profit",
        unit="EGP",
        descriptive_direction=DescriptiveDirection.IMPROVING,
        inferential_status=inferential,
        posture=posture,
        statistical_observation_ids=("a", "b"),
        statistical_difference_direction=(
            DescriptiveDirection.UNAVAILABLE
            if inferential is InferentialStatus.UNAVAILABLE
            else DescriptiveDirection.IMPROVING
        ),
        current_observation_ids=("c",),
        baseline_observation_ids=("b",),
    )


def test_reviewable_evidence_preserves_context_and_requires_policy_review():
    result = handoff_evidence_for_review(
        _support(CombinedEvidencePosture.DESCRIPTIVE_CHANGE_WITH_STATISTICAL_DETECTION)
    )
    assert result.status is EvidenceHandoffStatus.READY_FOR_REVIEW
    assert result.requires_policy_review is True
    assert result.descriptive_direction is DescriptiveDirection.IMPROVING
    assert result.statistical_observation_ids == ("a", "b")


def test_change_without_statistical_detection_is_reviewable():
    result = handoff_evidence_for_review(
        _support(
            CombinedEvidencePosture.DESCRIPTIVE_CHANGE_WITHOUT_STATISTICAL_DETECTION,
            InferentialStatus.NO_STATISTICALLY_DETECTED_DIFFERENCE,
        )
    )
    assert result.status is EvidenceHandoffStatus.READY_FOR_REVIEW
    assert result.requires_policy_review is True


def test_missing_inferential_evidence_is_incomplete_but_still_requires_policy_review():
    result = handoff_evidence_for_review(
        _support(
            CombinedEvidencePosture.INFERENTIAL_EVIDENCE_UNAVAILABLE,
            InferentialStatus.UNAVAILABLE,
        )
    )
    assert result.status is EvidenceHandoffStatus.EVIDENCE_INCOMPLETE
    assert result.requires_policy_review is True


def test_invalid_context_cannot_be_handed_to_policy_review():
    result = handoff_evidence_for_review(
        _support(CombinedEvidencePosture.CONTEXT_INVALID)
    )
    assert result.status is EvidenceHandoffStatus.CONTEXT_INVALID
    assert result.requires_policy_review is False


def test_lineage_is_preserved_for_all_evidence_dimensions():
    result = handoff_evidence_for_review(
        _support(CombinedEvidencePosture.DESCRIPTIVE_CHANGE_WITH_STATISTICAL_DETECTION)
    )
    assert result.current_observation_ids == ("c",)
    assert result.baseline_observation_ids == ("b",)


def test_handoff_rejects_duplicate_lineage():
    try:
        type(result := handoff_evidence_for_review(
            _support(CombinedEvidencePosture.DESCRIPTIVE_CHANGE_WITH_STATISTICAL_DETECTION)
        ))(
            business_id=result.business_id,
            metric_name=result.metric_name,
            unit=result.unit,
            status=result.status,
            descriptive_direction=result.descriptive_direction,
            inferential_status=result.inferential_status,
            posture=result.posture,
            statistical_observation_ids=("a", "a"),
            current_observation_ids=result.current_observation_ids,
            baseline_observation_ids=result.baseline_observation_ids,
            requires_policy_review=result.requires_policy_review,
        )
    except ValueError:
        return
    raise AssertionError("duplicate lineage must be rejected")
