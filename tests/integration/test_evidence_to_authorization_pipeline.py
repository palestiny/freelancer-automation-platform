from app.domain.action_authorization import (
    ActionAuthorizationStatus,
    ActionClass,
    AutonomyLevel,
    authorize_action,
)
from app.domain.evidence_decision_handoff import handoff_evidence_for_review
from app.domain.evidence_policy_review import (
    EvidencePolicyReviewStatus,
    PolicyReviewPolicy,
    review_evidence_policy,
)
from app.domain.performance_evidence_decision_support import (
    CombinedEvidencePosture,
    DescriptiveDirection,
    InferentialStatus,
    PerformanceEvidenceDecisionSupport,
)


def _evidence() -> PerformanceEvidenceDecisionSupport:
    return PerformanceEvidenceDecisionSupport(
        business_id="business-1",
        metric_name="profit",
        unit="EGP",
        descriptive_direction=DescriptiveDirection.INCREASED,
        inferential_status=InferentialStatus.STATISTICAL_DIFFERENCE_DETECTED,
        posture=CombinedEvidencePosture.DESCRIPTIVE_CHANGE_WITH_STATISTICAL_DETECTION,
        statistical_observation_ids=("stat-1", "stat-2"),
        statistical_difference_direction=DescriptiveDirection.INCREASED,
        current_observation_ids=("current-1", "current-2"),
        baseline_observation_ids=("baseline-1", "baseline-2"),
    )


def test_evidence_to_authorization_preserves_gates_and_lineage():
    handoff = handoff_evidence_for_review(_evidence())

    assert handoff.requires_policy_review is True

    review = review_evidence_policy(
        handoff=handoff,
        policy=PolicyReviewPolicy(
            policy_id="policy-profit-growth",
            version="1",
            allowed_directions=frozenset({DescriptiveDirection.INCREASED}),
            require_statistical_detection=True,
            require_complete_evidence=True,
        ),
    )

    assert review.status is EvidencePolicyReviewStatus.POLICY_SATISFIED
    assert review.current_observation_ids == ("current-1", "current-2")
    assert review.baseline_observation_ids == ("baseline-1", "baseline-2")
    assert review.statistical_observation_ids == ("stat-1", "stat-2")

    authorization = authorize_action(
        review=review,
        action_class=ActionClass.REVERSIBLE_EXTERNAL,
        requested_autonomy=AutonomyLevel.L3_EXECUTE_WITH_APPROVAL,
        maximum_autonomy=AutonomyLevel.L3_EXECUTE_WITH_APPROVAL,
        policy_id="policy-profit-growth",
        policy_version="1",
        human_approval_granted=False,
    )

    assert authorization.status is ActionAuthorizationStatus.HUMAN_APPROVAL_REQUIRED
    assert authorization.current_observation_ids == review.current_observation_ids
    assert authorization.baseline_observation_ids == review.baseline_observation_ids
    assert authorization.statistical_observation_ids == review.statistical_observation_ids


def test_unsatisfied_policy_stops_before_authorization():
    handoff = handoff_evidence_for_review(_evidence())
    review = review_evidence_policy(
        handoff=handoff,
        policy=PolicyReviewPolicy(
            policy_id="policy-profit-decline-only",
            version="1",
            allowed_directions=frozenset({DescriptiveDirection.DECREASED}),
            require_statistical_detection=False,
            require_complete_evidence=True,
        ),
    )

    assert review.status is EvidencePolicyReviewStatus.POLICY_NOT_SATISFIED

    authorization = authorize_action(
        review=review,
        action_class=ActionClass.REVERSIBLE_EXTERNAL,
        requested_autonomy=AutonomyLevel.L3_EXECUTE_WITH_APPROVAL,
        maximum_autonomy=AutonomyLevel.L3_EXECUTE_WITH_APPROVAL,
        policy_id="policy-profit-decline-only",
        policy_version="1",
        human_approval_granted=True,
    )

    assert authorization.status is ActionAuthorizationStatus.NOT_AUTHORIZED
