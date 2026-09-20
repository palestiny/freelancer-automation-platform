from dataclasses import dataclass
from enum import Enum

from .performance_evidence_decision_support import (
    InferentialStatus,
    PerformanceEvidenceDecisionSupport,
)


class EvidenceHandoffType(str, Enum):
    POLICY_REVIEW = "policy_review"
    EXPERIMENT = "experiment"


@dataclass(frozen=True)
class EvidenceLearningHandoff:
    handoff_id: str
    business_id: str
    metric_name: str
    unit: str
    handoff_type: EvidenceHandoffType
    target: str
    statement: str
    observation_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.handoff_id.strip() or not self.business_id.strip() or not self.metric_name.strip() or not self.unit.strip():
            raise ValueError("business_id, metric_name, and unit cannot be empty")
        if not self.target.strip() or not self.statement.strip():
            raise ValueError("target and statement cannot be empty")
        if not self.observation_ids or len(set(self.observation_ids)) != len(self.observation_ids):
            raise ValueError("observation_ids must be non-empty and unique")


def create_evidence_learning_handoff(
    *,
    handoff_id: str,
    evidence: PerformanceEvidenceDecisionSupport,
    handoff_type: EvidenceHandoffType,
    target: str,
    statement: str,
) -> EvidenceLearningHandoff:
    if evidence.inferential_status.value == "unavailable":
        raise ValueError("evidence must be eligible before handoff")
    return EvidenceLearningHandoff(
        handoff_id=handoff_id,
        business_id=evidence.business_id,
        metric_name=evidence.metric_name,
        unit=evidence.unit,
        handoff_type=handoff_type,
        target=target,
        statement=statement,
        observation_ids=evidence.statistical_observation_ids,
    )
