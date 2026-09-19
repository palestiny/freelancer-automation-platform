from app.domain.evidence_policy_review import EvidencePolicyReview, EvidencePolicyReviewReason, EvidencePolicyReviewStatus
from app.domain.performance_evidence_decision_support import DescriptiveDirection, InferentialStatus
from app.domain.action_authorization import ActionAuthorizationStatus, ActionClass, AutonomyLevel, authorize_action


def _review(status=EvidencePolicyReviewStatus.POLICY_SATISFIED):
    return EvidencePolicyReview(
        business_id="b1", metric_name="profit", unit="EGP", status=status,
        reason=EvidencePolicyReviewReason.SATISFIED if status is EvidencePolicyReviewStatus.POLICY_SATISFIED else EvidencePolicyReviewReason.DIRECTION_NOT_ALLOWED,
        descriptive_direction=DescriptiveDirection.IMPROVING,
        inferential_status=InferentialStatus.STATISTICAL_DIFFERENCE_DETECTED,
        current_observation_ids=("c1",), baseline_observation_ids=("b1",), statistical_observation_ids=("s1", "s2"),
    )


def test_reversible_action_can_be_authorized_within_policy():
    result = authorize_action(review=_review(), action_class=ActionClass.REVERSIBLE_EXTERNAL,
        requested_autonomy=AutonomyLevel.L3_EXECUTE_WITH_APPROVAL, maximum_autonomy=AutonomyLevel.L3_EXECUTE_WITH_APPROVAL,
        policy_id="policy-1", policy_version="1", human_approval_granted=True)
    assert result.status is ActionAuthorizationStatus.AUTHORIZED
    assert result.requires_human_approval is False


def test_automatic_execution_requires_policy_level():
    result = authorize_action(review=_review(), action_class=ActionClass.REVERSIBLE_EXTERNAL,
        requested_autonomy=AutonomyLevel.L4_EXECUTE_AUTOMATICALLY_WITHIN_POLICY, maximum_autonomy=AutonomyLevel.L3_EXECUTE_WITH_APPROVAL,
        policy_id="policy-1", policy_version="1", human_approval_granted=False)
    assert result.status is ActionAuthorizationStatus.NOT_AUTHORIZED


def test_human_approval_is_required_for_l3():
    result = authorize_action(review=_review(), action_class=ActionClass.REVERSIBLE_EXTERNAL,
        requested_autonomy=AutonomyLevel.L3_EXECUTE_WITH_APPROVAL, maximum_autonomy=AutonomyLevel.L3_EXECUTE_WITH_APPROVAL,
        policy_id="policy-1", policy_version="1", human_approval_granted=False)
    assert result.status is ActionAuthorizationStatus.HUMAN_APPROVAL_REQUIRED
    assert result.requires_human_approval is True


def test_irreversible_action_is_safety_blocked():
    result = authorize_action(review=_review(), action_class=ActionClass.IRREVERSIBLE_EXTERNAL,
        requested_autonomy=AutonomyLevel.L4_EXECUTE_AUTOMATICALLY_WITHIN_POLICY, maximum_autonomy=AutonomyLevel.L5_OPTIMIZE_WITHIN_POLICY,
        policy_id="policy-1", policy_version="1", human_approval_granted=True)
    assert result.status is ActionAuthorizationStatus.SAFETY_BLOCKED


def test_financial_action_is_safety_blocked_even_at_high_autonomy():
    result = authorize_action(review=_review(), action_class=ActionClass.FINANCIAL,
        requested_autonomy=AutonomyLevel.L5_OPTIMIZE_WITHIN_POLICY, maximum_autonomy=AutonomyLevel.L5_OPTIMIZE_WITHIN_POLICY,
        policy_id="policy-1", policy_version="1", human_approval_granted=True)
    assert result.status is ActionAuthorizationStatus.SAFETY_BLOCKED


def test_unsatisfied_policy_cannot_authorize():
    result = authorize_action(review=_review(EvidencePolicyReviewStatus.POLICY_NOT_SATISFIED), action_class=ActionClass.REVERSIBLE_EXTERNAL,
        requested_autonomy=AutonomyLevel.L3_EXECUTE_WITH_APPROVAL, maximum_autonomy=AutonomyLevel.L5_OPTIMIZE_WITHIN_POLICY,
        policy_id="policy-1", policy_version="1", human_approval_granted=True)
    assert result.status is ActionAuthorizationStatus.NOT_AUTHORIZED
