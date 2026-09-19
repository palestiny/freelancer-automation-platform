from dataclasses import dataclass

from .performance_evidence_decision_support import (
    CombinedEvidencePosture,
    DescriptiveDirection,
    InferentialStatus,
    PerformanceEvidenceDecisionSupport,
)


@dataclass(frozen=True)
class DecisionSupportEvidence:
    business_id: str
    metric_name: str
    unit: str
    descriptive_direction: DescriptiveDirection
    inferential_status: InferentialStatus
    posture: CombinedEvidencePosture
    observation_ids: tuple[str, ...]
    requires_policy_review: bool

    def __post_init__(self) -> None:
        if not self.business_id.strip() or not self.metric_name.strip() or not self.unit.strip():
            raise ValueError("business_id, metric_name, and unit cannot be empty")
        if not self.observation_ids:
            raise ValueError("observation_ids cannot be empty")
        if len(set(self.observation_ids)) != len(self.observation_ids):
            raise ValueError("observation_ids must be unique")
        if self.requires_policy_review and self.posture is CombinedEvidencePosture.CONTEXT_INVALID:
            raise ValueError("context-invalid evidence cannot require policy review")


def create_decision_support_evidence(
    evidence: PerformanceEvidenceDecisionSupport,
) -> DecisionSupportEvidence:
    requires_policy_review = evidence.posture is not CombinedEvidencePosture.CONTEXT_INVALID
    return DecisionSupportEvidence(
        business_id=evidence.business_id,
        metric_name=evidence.metric_name,
        unit=evidence.unit,
        descriptive_direction=evidence.descriptive_direction,
        inferential_status=evidence.inferential_status,
        posture=evidence.posture,
        observation_ids=evidence.statistical_observation_ids,
        requires_policy_review=requires_policy_review,
    )
