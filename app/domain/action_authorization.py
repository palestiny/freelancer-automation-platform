from dataclasses import dataclass
from enum import Enum

from .evidence_policy_review import EvidencePolicyReview, EvidencePolicyReviewStatus


class AutonomyLevel(int, Enum):
    L0_OBSERVE = 0
    L1_RECOMMEND = 1
    L2_PREPARE = 2
    L3_EXECUTE_WITH_APPROVAL = 3
    L4_EXECUTE_AUTOMATICALLY_WITHIN_POLICY = 4
    L5_OPTIMIZE_WITHIN_POLICY = 5


class ActionClass(str, Enum):
    INFORMATIONAL = "informational"
    REVERSIBLE_EXTERNAL = "reversible_external"
    IRREVERSIBLE_EXTERNAL = "irreversible_external"
    FINANCIAL = "financial"


class ActionAuthorizationStatus(str, Enum):
    AUTHORIZED = "authorized"
    HUMAN_APPROVAL_REQUIRED = "human_approval_required"
    NOT_AUTHORIZED = "not_authorized"
    SAFETY_BLOCKED = "safety_blocked"


@dataclass(frozen=True)
class ActionAuthorization:
    policy_id: str
    policy_version: str
    action_class: ActionClass
    requested_autonomy: AutonomyLevel
    maximum_autonomy: AutonomyLevel
    status: ActionAuthorizationStatus
    requires_human_approval: bool
    current_observation_ids: tuple[str, ...] = ()
    baseline_observation_ids: tuple[str, ...] = ()
    statistical_observation_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.policy_id.strip() or not self.policy_version.strip():
            raise ValueError("policy_id and policy_version cannot be empty")
        if self.requested_autonomy.value > self.maximum_autonomy.value and self.status is ActionAuthorizationStatus.AUTHORIZED:
            raise ValueError("authorized autonomy cannot exceed policy maximum")
        if self.status is ActionAuthorizationStatus.HUMAN_APPROVAL_REQUIRED and not self.requires_human_approval:
            raise ValueError("human approval required status must require approval")
        if self.status is ActionAuthorizationStatus.AUTHORIZED and self.requires_human_approval:
            raise ValueError("authorized status cannot still require human approval")
        for ids in (self.current_observation_ids, self.baseline_observation_ids, self.statistical_observation_ids):
            if len(set(ids)) != len(ids):
                raise ValueError("authorization observation IDs must be unique")


def authorize_action(*, review: EvidencePolicyReview, action_class: ActionClass,
                     requested_autonomy: AutonomyLevel, maximum_autonomy: AutonomyLevel,
                     policy_id: str, policy_version: str,
                     human_approval_granted: bool) -> ActionAuthorization:
    if not policy_id.strip() or not policy_version.strip():
        raise ValueError("policy_id and policy_version cannot be empty")
    if not isinstance(human_approval_granted, bool):
        raise TypeError("human_approval_granted must be bool")
    if review.policy_id != policy_id or review.policy_version != policy_version:
        return _result(review, policy_id, policy_version, action_class, requested_autonomy, maximum_autonomy, ActionAuthorizationStatus.NOT_AUTHORIZED, False)
    if review.status is not EvidencePolicyReviewStatus.POLICY_SATISFIED:
        return _result(review, policy_id, policy_version, action_class, requested_autonomy, maximum_autonomy, ActionAuthorizationStatus.NOT_AUTHORIZED, False)
    if action_class in {ActionClass.IRREVERSIBLE_EXTERNAL, ActionClass.FINANCIAL}:
        return _result(policy_id, policy_version, action_class, requested_autonomy, maximum_autonomy, ActionAuthorizationStatus.SAFETY_BLOCKED, False)
    if requested_autonomy.value > maximum_autonomy.value:
        return _result(policy_id, policy_version, action_class, requested_autonomy, maximum_autonomy, ActionAuthorizationStatus.NOT_AUTHORIZED, False)
    if requested_autonomy is AutonomyLevel.L3_EXECUTE_WITH_APPROVAL and not human_approval_granted:
        return _result(policy_id, policy_version, action_class, requested_autonomy, maximum_autonomy, ActionAuthorizationStatus.HUMAN_APPROVAL_REQUIRED, True)
    return _result(policy_id, policy_version, action_class, requested_autonomy, maximum_autonomy, ActionAuthorizationStatus.AUTHORIZED, False)


def _result(review, policy_id, policy_version, action_class, requested_autonomy, maximum_autonomy, status, requires):
    return ActionAuthorization(policy_id=policy_id, policy_version=policy_version,
                               action_class=action_class, requested_autonomy=requested_autonomy,
                               maximum_autonomy=maximum_autonomy, status=status,
                               requires_human_approval=requires,
                               current_observation_ids=review.current_observation_ids,
                               baseline_observation_ids=review.baseline_observation_ids,
                               statistical_observation_ids=review.statistical_observation_ids)
