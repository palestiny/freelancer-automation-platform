from dataclasses import dataclass

from .performance_evidence_decision_support import (
    CombinedEvidencePosture,
    DescriptiveDirection,
    InferentialStatus,
    PerformanceEvidenceDecisionSupport,
)


@dataclass(frozen=True)
class EvidenceDecisionContext:
    business_id: str
    metric_name: str
    unit: str
    descriptive_direction: DescriptiveDirection
    inferential_status: InferentialStatus
    posture: CombinedEvidencePosture
    statistical_observation_ids: tuple[str, ...]
    source_references: tuple[str, ...]
    current_evidence_quality: float
    baseline_evidence_quality: float

    def __post_init__(self):
        if not self.business_id.strip() or not self.metric_name.strip() or not self.unit.strip():
            raise ValueError("business_id, metric_name, and unit cannot be empty")
        if not self.statistical_observation_ids:
            raise ValueError("statistical_observation_ids cannot be empty")
        if not self.source_references:
            raise ValueError("source_references cannot be empty")
        if len(set(self.source_references)) != len(self.source_references):
            raise ValueError("source_references must be unique")
        for value in (self.current_evidence_quality, self.baseline_evidence_quality):
            if not 0 <= value <= 100:
                raise ValueError("evidence quality must be between 0 and 100")


def build_evidence_decision_context(
    *,
    support: PerformanceEvidenceDecisionSupport,
    source_references: tuple[str, ...],
    current_evidence_quality: float,
    baseline_evidence_quality: float,
) -> EvidenceDecisionContext:
    return EvidenceDecisionContext(
        business_id=support.business_id,
        metric_name=support.metric_name,
        unit=support.unit,
        descriptive_direction=support.descriptive_direction,
        inferential_status=support.inferential_status,
        posture=support.posture,
        statistical_observation_ids=support.statistical_observation_ids,
        source_references=source_references,
        current_evidence_quality=current_evidence_quality,
        baseline_evidence_quality=baseline_evidence_quality,
    )
