from dataclasses import dataclass
from enum import Enum

from .performance_evidence_decision_support import (
    CombinedEvidencePosture,
    DescriptiveDirection,
    InferentialStatus,
    PerformanceEvidenceDecisionSupport,
)


class EvidenceHandoffStatus(str, Enum):
    READY = "ready"
    NOT_READY = "not_ready"


@dataclass(frozen=True)
class EvidenceHandoff:
    business_id: str
    metric_name: str
    unit: str
    consumer_id: str
    descriptive_direction: DescriptiveDirection
    inferential_status: InferentialStatus
    posture: CombinedEvidencePosture
    statistical_observation_ids: tuple[str, ...]
    status: EvidenceHandoffStatus


def create_evidence_handoff(
    *,
    evidence: PerformanceEvidenceDecisionSupport,
    consumer_id: str,
) -> EvidenceHandoff:
    if not consumer_id.strip():
        raise ValueError("consumer_id cannot be empty")

    ready = (
        evidence.posture is not CombinedEvidencePosture.CONTEXT_INVALID
        and evidence.inferential_status is not InferentialStatus.UNAVAILABLE
    )

    return EvidenceHandoff(
        business_id=evidence.business_id,
        metric_name=evidence.metric_name,
        unit=evidence.unit,
        consumer_id=consumer_id,
        descriptive_direction=evidence.descriptive_direction,
        inferential_status=evidence.inferential_status,
        posture=evidence.posture,
        statistical_observation_ids=evidence.statistical_observation_ids,
        status=EvidenceHandoffStatus.READY if ready else EvidenceHandoffStatus.NOT_READY,
    )
