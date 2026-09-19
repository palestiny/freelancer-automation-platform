from dataclasses import dataclass
from enum import Enum

from .performance_evidence_decision_support import (
    CombinedEvidencePosture,
    DescriptiveDirection,
    InferentialStatus,
    PerformanceEvidenceDecisionSupport,
)


class EvidenceReviewState(str, Enum):
    READY_FOR_REVIEW = "ready_for_review"
    EVIDENCE_UNAVAILABLE = "evidence_unavailable"
    CONTEXT_INVALID = "context_invalid"


@dataclass(frozen=True)
class EvidenceReviewItem:
    business_id: str
    metric_name: str
    unit: str
    descriptive_direction: DescriptiveDirection
    inferential_status: InferentialStatus
    posture: CombinedEvidencePosture
    observation_ids: tuple[str, ...]
    state: EvidenceReviewState

    def __post_init__(self) -> None:
        if not self.business_id.strip() or not self.metric_name.strip() or not self.unit.strip():
            raise ValueError("business_id, metric_name, and unit cannot be empty")
        if not self.observation_ids:
            raise ValueError("observation_ids cannot be empty")
        if len(set(self.observation_ids)) != len(self.observation_ids):
            raise ValueError("observation_ids must be unique")


def create_evidence_review_item(
    support: PerformanceEvidenceDecisionSupport,
) -> EvidenceReviewItem:
    if support.posture is CombinedEvidencePosture.CONTEXT_INVALID:
        state = EvidenceReviewState.CONTEXT_INVALID
    elif support.inferential_status is InferentialStatus.UNAVAILABLE:
        state = EvidenceReviewState.EVIDENCE_UNAVAILABLE
    else:
        state = EvidenceReviewState.READY_FOR_REVIEW

    return EvidenceReviewItem(
        business_id=support.business_id,
        metric_name=support.metric_name,
        unit=support.unit,
        descriptive_direction=support.descriptive_direction,
        inferential_status=support.inferential_status,
        posture=support.posture,
        observation_ids=support.statistical_observation_ids,
        state=state,
    )
