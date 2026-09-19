from dataclasses import dataclass
from enum import Enum

from .performance_evidence_decision_support import CombinedEvidencePosture, PerformanceEvidenceDecisionSupport

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
    observation_ids: tuple[str, ...]

def handoff_evidence_for_review(evidence: PerformanceEvidenceDecisionSupport) -> EvidenceDecisionHandoff:
    if evidence.posture is CombinedEvidencePosture.CONTEXT_INVALID:
        status = EvidenceHandoffStatus.CONTEXT_INVALID
    elif evidence.posture is CombinedEvidencePosture.INFERENTIAL_EVIDENCE_UNAVAILABLE:
        status = EvidenceHandoffStatus.EVIDENCE_INCOMPLETE
    else:
        status = EvidenceHandoffStatus.READY_FOR_REVIEW
    return EvidenceDecisionHandoff(business_id=evidence.business_id, metric_name=evidence.metric_name, unit=evidence.unit, status=status, observation_ids=evidence.statistical_observation_ids)