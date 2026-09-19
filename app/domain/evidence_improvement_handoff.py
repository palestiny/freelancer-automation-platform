from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from .performance_evidence_decision_support import (
    InferentialStatus,
    PerformanceEvidenceDecisionSupport,
)


class ImprovementHandoffStatus(str, Enum):
    READY_FOR_REVIEW = "ready_for_review"
    NOT_REQUESTED = "not_requested"
    EVIDENCE_NOT_ELIGIBLE = "evidence_not_eligible"


@dataclass(frozen=True)
class ImprovementHandoffRequest:
    business_id: str
    metric_name: str
    unit: str
    statement: str
    requested_at: datetime
    status: ImprovementHandoffStatus
    observation_ids: tuple[str, ...]


def create_improvement_handoff(
    *,
    evidence: PerformanceEvidenceDecisionSupport,
    request_review: bool,
    statement: str,
    requested_at: datetime,
) -> ImprovementHandoffRequest:
    if not statement.strip():
        raise ValueError("statement cannot be empty")

    if not request_review:
        status = ImprovementHandoffStatus.NOT_REQUESTED
    elif evidence.inferential_status is InferentialStatus.UNAVAILABLE:
        status = ImprovementHandoffStatus.EVIDENCE_NOT_ELIGIBLE
    else:
        status = ImprovementHandoffStatus.READY_FOR_REVIEW

    return ImprovementHandoffRequest(
        business_id=evidence.business_id,
        metric_name=evidence.metric_name,
        unit=evidence.unit,
        statement=statement,
        requested_at=requested_at,
        status=status,
        observation_ids=evidence.statistical_observation_ids,
    )
