from dataclasses import dataclass
from enum import Enum

from .performance_evidence_decision_support import (
    DescriptiveDirection,
    InferentialStatus,
    PerformanceEvidenceDecisionSupport,
)


class LearningHandoffTarget(str, Enum):
    POLICY_REVIEW = "policy_review"
    EXPERIMENT = "experiment"


@dataclass(frozen=True)
class StatisticalEvidenceLearningHandoff:
    business_id: str
    metric_name: str
    unit: str
    statement: str
    target: LearningHandoffTarget
    descriptive_direction: DescriptiveDirection
    inferential_status: InferentialStatus
    posture: object
    statistical_method: str
    statistical_observation_ids: tuple[str, ...]
    current_observation_ids: tuple[str, ...]
    baseline_observation_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        for name in ("business_id", "metric_name", "unit", "statement", "statistical_method"):
            if not getattr(self, name).strip():
                raise ValueError(f"{name} cannot be empty")
        for name, ids in (
            ("statistical_observation_ids", self.statistical_observation_ids),
            ("current_observation_ids", self.current_observation_ids),
            ("baseline_observation_ids", self.baseline_observation_ids),
        ):
            if not ids or len(set(ids)) != len(ids):
                raise ValueError(f"{name} must contain unique non-empty ids")


def create_statistical_evidence_learning_handoff(
    *,
    evidence: PerformanceEvidenceDecisionSupport,
    statement: str,
    target: LearningHandoffTarget,
) -> StatisticalEvidenceLearningHandoff:
    if not statement.strip():
        raise ValueError("statement cannot be empty")
    return StatisticalEvidenceLearningHandoff(
        business_id=evidence.business_id,
        metric_name=evidence.metric_name,
        unit=evidence.unit,
        statement=statement,
        target=target,
        descriptive_direction=evidence.descriptive_direction,
        inferential_status=evidence.inferential_status,
        posture=evidence.posture,
        statistical_method=evidence.statistical_method,
        statistical_observation_ids=evidence.statistical_observation_ids,
        current_observation_ids=evidence.current_observation_ids,
        baseline_observation_ids=evidence.baseline_observation_ids,
    )
