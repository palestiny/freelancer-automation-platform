from app.domain.evidence_decision_handoff import EvidenceHandoffStatus, EvidenceDecisionHandoff
from app.domain.performance_evidence_decision_support import (
    CombinedEvidencePosture,
    DescriptiveDirection,
    InferentialStatus,
)
from app.domain.evidence_policy_review import (
    EvidencePolicyReviewReason,
    EvidencePolicyReviewStatus,
    PolicyReviewPolicy,
    review_evidence_policy,
)


def _handoff(*, status=EvidenceHandoffStatus.READY_FOR_REVIEW, direction=DescriptiveDirection.INCREASED,
             inferential=InferentialStatus.STATISTICAL_DIFFERENCE_DETECTED, requires=True):
    return EvidenceDecisionHandoff(
        business_id="b1",
        metric_name="profit",
        unit="EGP",
        status=status,
        descriptive_direction=direction,
        inferential_status=inferential,
        posture=CombinedEvidencePosture.DESCRIPTIVE_CHANGE_WITH_STATISTICAL_DETECTION,
        statistical_observation_ids=("s1", "s2"),
        current_observation_ids=("c1",),
        baseline_observation_ids=("b1",),
        requires_policy_review=requires,
    )


def test_policy_satisfied_when_explicit_conditions_match():
    result = review_evidence_policy(
        handoff=_handoff(),
        policy=PolicyReviewPolicy(
            policy_id="policy-1",
            version="1",
            allowed_directions=frozenset({DescriptiveDirection.INCREASED}),
            require_statistical_detection=True,
            require_complete_evidence=True,
        ),
    )
    assert result.status is EvidencePolicyReviewStatus.POLICY_SATISFIED
    assert result.reason is EvidencePolicyReviewReason.SATISFIED
    assert result.current_observation_ids == ("c1",)


def test_direction_mismatch_is_explicit():
    result = review_evidence_policy(
        handoff=_handoff(direction=DescriptiveDirection.DECREASED),
        policy=PolicyReviewPolicy(
            policy_id="policy-1",
            version="1",
            allowed_directions=frozenset({DescriptiveDirection.INCREASED}),
            require_statistical_detection=False,
            require_complete_evidence=False,
        ),
    )
    assert result.status is EvidencePolicyReviewStatus.POLICY_NOT_SATISFIED
    assert result.reason is EvidencePolicyReviewReason.DIRECTION_NOT_ALLOWED


def test_statistical_detection_requirement_is_explicit():
    result = review_evidence_policy(
        handoff=_handoff(inferential=InferentialStatus.NO_STATISTICALLY_DETECTED_DIFFERENCE),
        policy=PolicyReviewPolicy(
            policy_id="policy-1",
            version="1",
            allowed_directions=frozenset({DescriptiveDirection.INCREASED}),
            require_statistical_detection=True,
            require_complete_evidence=False,
        ),
    )
    assert result.status is EvidencePolicyReviewStatus.POLICY_NOT_SATISFIED
    assert result.reason is EvidencePolicyReviewReason.STATISTICAL_DETECTION_REQUIRED


def test_incomplete_evidence_requires_review_when_policy_requires_complete_evidence():
    result = review_evidence_policy(
        handoff=_handoff(
            status=EvidenceHandoffStatus.EVIDENCE_INCOMPLETE,
            inferential=InferentialStatus.UNAVAILABLE,
        ),
        policy=PolicyReviewPolicy(
            policy_id="policy-1",
            version="1",
            allowed_directions=frozenset({DescriptiveDirection.INCREASED}),
            require_statistical_detection=False,
            require_complete_evidence=True,
        ),
    )
    assert result.status is EvidencePolicyReviewStatus.REVIEW_REQUIRED
    assert result.reason is EvidencePolicyReviewReason.EVIDENCE_INCOMPLETE


def test_context_invalid_is_not_satisfied():
    result = review_evidence_policy(
        handoff=_handoff(
            status=EvidenceHandoffStatus.CONTEXT_INVALID,
            requires=False,
        ),
        policy=PolicyReviewPolicy(
            policy_id="policy-1",
            version="1",
            allowed_directions=frozenset({DescriptiveDirection.INCREASED}),
            require_statistical_detection=False,
            require_complete_evidence=False,
        ),
    )
    assert result.status is EvidencePolicyReviewStatus.POLICY_NOT_SATISFIED
    assert result.reason is EvidencePolicyReviewReason.INVALID_CONTEXT


