from dataclasses import dataclass
from enum import Enum

from .performance_evidence_decision_support import (
    CombinedEvidencePosture,
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
    posture: CombinedEvidencePosture
    statistical_method: str
    statistical_observation_ids: tuple[str, ...]
    current_observation_ids: tuple[str, ...]
    baseline_observation_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        for name in ("business_id", "metric_name", "unit", "statement", "statistical_method"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} cannot be empty")
        if not isinstance(self.target, LearningHandoffTarget):
            raise TypeError("target must be a LearningHandoffTarget")
        if not isinstance(self.descriptive_direction, DescriptiveDirection):
            raise TypeError("descriptive_direction must be a DescriptiveDirection")
        if not isinstance(self.inferential_status, InferentialStatus):
            raise TypeError("inferential_status must be an InferentialStatus")
        if not isinstance(self.posture, CombinedEvidencePosture):
            raise TypeError("posture must be a CombinedEvidencePosture")
        for name, ids in (
            ("statistical_observation_ids", self.statistical_observation_ids),
            ("current_observation_ids", self.current_observation_ids),
            ("baseline_observation_ids", self.baseline_observation_ids),
        ):
            if not ids or any(not isinstance(value, str) or not value.strip() for value in ids):
                raise ValueError(f"{name} must contain non-empty string ids")
            if len(set(ids)) != len(ids):
                raise ValueError(f"{name} must contain unique ids")


def create_statistical_evidence_learning_handoff(
    *,
    evidence: PerformanceEvidenceDecisionSupport,
    statement: str,
    target: LearningHandoffTarget,
) -> StatisticalEvidenceLearningHandoff:
    if not isinstance(evidence, PerformanceEvidenceDecisionSupport):
        raise TypeError("evidence must be PerformanceEvidenceDecisionSupport")
    if not isinstance(target, LearningHandoffTarget):
        raise TypeError("target must be a LearningHandoffTarget")
    if not isinstance(statement, str) or not statement.strip():
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
