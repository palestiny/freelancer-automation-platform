from dataclasses import dataclass
from enum import Enum

from .performance_evidence_decision_support import (
    CombinedEvidencePosture,
    DescriptiveDirection,
    InferentialStatus,
    PerformanceEvidenceDecisionSupport,
)


class EvidenceHandoffStatus(str, Enum):
    READY_FOR_REVIEW = "ready_for_review"
    EVIDENCE_INCOMPLETE = "evidence_incomplete"
    CONTEXT_INVALID = "context_invalid"


@dataclass(frozen=True)
class EvidenceDecisionHandoff:
    business_id: str
    metric_name: str
    unit: str
    status: EvidenceHandoffStatus
    descriptive_direction: DescriptiveDirection
    inferential_status: InferentialStatus
    posture: CombinedEvidencePosture
    statistical_observation_ids: tuple[str, ...]
    current_observation_ids: tuple[str, ...]
    baseline_observation_ids: tuple[str, ...]
    requires_policy_review: bool

    def __post_init__(self) -> None:
        for name in ("business_id", "metric_name", "unit"):
            if not getattr(self, name).strip():
                raise ValueError(f"{name} cannot be empty")

        for name, ids in (
            ("statistical_observation_ids", self.statistical_observation_ids),
            ("current_observation_ids", self.current_observation_ids),
            ("baseline_observation_ids", self.baseline_observation_ids),
        ):
            if len(set(ids)) != len(ids):
                raise ValueError(f"{name} must be unique")

        if self.status is EvidenceHandoffStatus.CONTEXT_INVALID:
            if self.requires_policy_review:
                raise ValueError("context-invalid evidence cannot require policy review")
        elif not self.requires_policy_review:
            raise ValueError("valid handoff must require explicit policy review")


def handoff_evidence_for_review(
    evidence: PerformanceEvidenceDecisionSupport,
) -> EvidenceDecisionHandoff:
    if evidence.posture is CombinedEvidencePosture.CONTEXT_INVALID:
        status = EvidenceHandoffStatus.CONTEXT_INVALID
        requires_policy_review = False
    elif evidence.posture is CombinedEvidencePosture.INFERENTIAL_EVIDENCE_UNAVAILABLE:
        status = EvidenceHandoffStatus.EVIDENCE_INCOMPLETE
        requires_policy_review = True
    else:
        status = EvidenceHandoffStatus.READY_FOR_REVIEW
        requires_policy_review = True

    return EvidenceDecisionHandoff(
        business_id=evidence.business_id,
        metric_name=evidence.metric_name,
        unit=evidence.unit,
        status=status,
        descriptive_direction=evidence.descriptive_direction,
        inferential_status=evidence.inferential_status,
        posture=evidence.posture,
        statistical_observation_ids=evidence.statistical_observation_ids,
        current_observation_ids=evidence.current_observation_ids,
        baseline_observation_ids=evidence.baseline_observation_ids,
        requires_policy_review=requires_policy_review,
    )
