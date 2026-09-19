from dataclasses import dataclass
from enum import Enum

from .evidence_decision_handoff import EvidenceDecisionHandoff, EvidenceHandoffStatus
from .performance_evidence_decision_support import DescriptiveDirection, InferentialStatus


class EvidencePolicyReviewStatus(str, Enum):
    POLICY_SATISFIED = "policy_satisfied"
    POLICY_NOT_SATISFIED = "policy_not_satisfied"
    REVIEW_REQUIRED = "review_required"


class EvidencePolicyReviewReason(str, Enum):
    SATISFIED = "satisfied"
    DIRECTION_NOT_ALLOWED = "direction_not_allowed"
    STATISTICAL_DETECTION_REQUIRED = "statistical_detection_required"
    EVIDENCE_INCOMPLETE = "evidence_incomplete"
    INVALID_CONTEXT = "invalid_context"


@dataclass(frozen=True)
class PolicyReviewPolicy:
    allowed_directions: frozenset[DescriptiveDirection]
    require_statistical_detection: bool
    require_complete_evidence: bool

    def __post_init__(self) -> None:
        if not self.allowed_directions:
            raise ValueError("allowed_directions cannot be empty")
        if not isinstance(self.require_statistical_detection, bool):
            raise TypeError("require_statistical_detection must be bool")
        if not isinstance(self.require_complete_evidence, bool):
            raise TypeError("require_complete_evidence must be bool")


@dataclass(frozen=True)
class EvidencePolicyReview:
    business_id: str
    metric_name: str
    unit: str
    status: EvidencePolicyReviewStatus
    reason: EvidencePolicyReviewReason
    descriptive_direction: DescriptiveDirection
    inferential_status: InferentialStatus
    current_observation_ids: tuple[str, ...]
    baseline_observation_ids: tuple[str, ...]
    statistical_observation_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        for name in ("business_id", "metric_name", "unit"):
            if not getattr(self, name).strip():
                raise ValueError(f"{name} cannot be empty")
        for name, ids in (
            ("current_observation_ids", self.current_observation_ids),
            ("baseline_observation_ids", self.baseline_observation_ids),
            ("statistical_observation_ids", self.statistical_observation_ids),
        ):
            if len(set(ids)) != len(ids):
                raise ValueError(f"{name} must be unique")


def review_evidence_policy(
    *,
    handoff: EvidenceDecisionHandoff,
    policy: PolicyReviewPolicy,
) -> EvidencePolicyReview:
    if handoff.status is EvidenceHandoffStatus.CONTEXT_INVALID:
        return _result(handoff, EvidencePolicyReviewStatus.POLICY_NOT_SATISFIED,
                       EvidencePolicyReviewReason.INVALID_CONTEXT)

    if policy.require_complete_evidence and handoff.status is EvidenceHandoffStatus.EVIDENCE_INCOMPLETE:
        return _result(handoff, EvidencePolicyReviewStatus.REVIEW_REQUIRED,
                       EvidencePolicyReviewReason.EVIDENCE_INCOMPLETE)

    if handoff.descriptive_direction not in policy.allowed_directions:
        return _result(handoff, EvidencePolicyReviewStatus.POLICY_NOT_SATISFIED,
                       EvidencePolicyReviewReason.DIRECTION_NOT_ALLOWED)

    if (
        policy.require_statistical_detection
        and handoff.inferential_status is not InferentialStatus.STATISTICAL_DIFFERENCE_DETECTED
    ):
        return _result(handoff, EvidencePolicyReviewStatus.POLICY_NOT_SATISFIED,
                       EvidencePolicyReviewReason.STATISTICAL_DETECTION_REQUIRED)

    return _result(handoff, EvidencePolicyReviewStatus.POLICY_SATISFIED,
                   EvidencePolicyReviewReason.SATISFIED)


def _result(handoff, status, reason):
    return EvidencePolicyReview(
        business_id=handoff.business_id,
        metric_name=handoff.metric_name,
        unit=handoff.unit,
        status=status,
        reason=reason,
        descriptive_direction=handoff.descriptive_direction,
        inferential_status=handoff.inferential_status,
        current_observation_ids=handoff.current_observation_ids,
        baseline_observation_ids=handoff.baseline_observation_ids,
        statistical_observation_ids=handoff.statistical_observation_ids,
    )
