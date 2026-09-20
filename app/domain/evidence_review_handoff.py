from dataclasses import dataclass
from enum import Enum

from .performance_evidence_decision_support import (
    CombinedEvidencePosture,
    DescriptiveDirection,
    InferentialStatus,
    PerformanceEvidenceDecisionSupport,
)


class ReviewTarget(str, Enum):
    POLICY_REVIEW = "policy_review"
    HUMAN_REVIEW = "human_review"


@dataclass(frozen=True)
class EvidenceReviewHandoff:
    business_id: str
    metric_name: str
    unit: str
    descriptive_direction: DescriptiveDirection
    inferential_status: InferentialStatus
    posture: CombinedEvidencePosture
    observation_ids: tuple[str, ...]
    target: ReviewTarget
    reason: str
    authorized: bool = False

    def __post_init__(self) -> None:
        if not self.business_id.strip() or not self.metric_name.strip() or not self.unit.strip():
            raise ValueError("business_id, metric_name, and unit cannot be empty")
        if not self.observation_ids:
            raise ValueError("observation_ids cannot be empty")
        if len(set(self.observation_ids)) != len(self.observation_ids):
            raise ValueError("observation_ids must be unique")
        if not self.reason.strip():
            raise ValueError("reason cannot be empty")
        if self.authorized:
            raise ValueError("evidence handoff cannot authorize policy or execution")


def create_evidence_review_handoff(
    *,
    evidence: PerformanceEvidenceDecisionSupport,
    target: ReviewTarget,
    reason: str,
) -> EvidenceReviewHandoff:
    if not isinstance(target, ReviewTarget):
        raise TypeError("target must be a ReviewTarget")

    return EvidenceReviewHandoff(
        business_id=evidence.business_id,
        metric_name=evidence.metric_name,
        unit=evidence.unit,
        descriptive_direction=evidence.descriptive_direction,
        inferential_status=evidence.inferential_status,
        posture=evidence.posture,
        observation_ids=evidence.statistical_observation_ids,
        target=target,
        reason=reason,
        authorized=False,
    )
