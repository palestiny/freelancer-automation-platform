from dataclasses import dataclass
from math import isfinite

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
    current_observation_ids: tuple[str, ...]
    baseline_observation_ids: tuple[str, ...]
    source_references: tuple[str, ...]
    current_evidence_quality: float
    baseline_evidence_quality: float

    def __post_init__(self) -> None:
        for name in ("business_id", "metric_name", "unit"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} cannot be empty")
        for name, ids in (
            ("statistical_observation_ids", self.statistical_observation_ids),
            ("current_observation_ids", self.current_observation_ids),
            ("baseline_observation_ids", self.baseline_observation_ids),
        ):
            if not isinstance(ids, tuple):
                raise TypeError(f"{name} must be a tuple")
            if not ids:
                raise ValueError(f"{name} cannot be empty")
            if any(not isinstance(value, str) or not value.strip() for value in ids):
                raise ValueError(f"{name} must contain non-empty strings")
            if len(set(ids)) != len(ids):
                raise ValueError(f"{name} must be unique")
        if not isinstance(self.source_references, tuple):
            raise TypeError("source_references must be a tuple")
        if not self.source_references:
            raise ValueError("source_references cannot be empty")
        if any(not isinstance(value, str) or not value.strip() for value in self.source_references):
            raise ValueError("source_references must contain non-empty strings")
        if len(set(self.source_references)) != len(self.source_references):
            raise ValueError("source_references must be unique")
        for value in (self.current_evidence_quality, self.baseline_evidence_quality):
            if not isinstance(value, (int, float)) or isinstance(value, bool) or not isfinite(value):
                raise ValueError("evidence quality must be finite numeric")
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
        current_observation_ids=support.current_observation_ids,
        baseline_observation_ids=support.baseline_observation_ids,
        source_references=source_references,
        current_evidence_quality=current_evidence_quality,
        baseline_evidence_quality=baseline_evidence_quality,
    )
