from dataclasses import dataclass
from enum import Enum

from .performance_evidence_decision_support import (
    CombinedEvidencePosture,
    PerformanceEvidenceDecisionSupport,
)


class PerformanceEvidencePolicyState(str, Enum):
    SUPPORTS_IMPROVEMENT = "supports_improvement"
    SUPPORTS_DECLINE = "supports_decline"
    DESCRIPTIVE_CHANGE_ONLY = "descriptive_change_only"
    NO_CHANGE_EVIDENCE = "no_change_evidence"
    EVIDENCE_INSUFFICIENT = "evidence_insufficient"
    CONTEXT_INVALID = "context_invalid"


@dataclass(frozen=True)
class PerformanceEvidencePolicyAssessment:
    business_id: str
    metric_name: str
    unit: str
    state: PerformanceEvidencePolicyState
    observation_ids: tuple[str, ...]


def assess_performance_evidence_policy(
    *,
    support: PerformanceEvidenceDecisionSupport,
) -> PerformanceEvidencePolicyAssessment:
    if support.posture is CombinedEvidencePosture.CONTEXT_INVALID:
        state = PerformanceEvidencePolicyState.CONTEXT_INVALID
    elif support.posture is CombinedEvidencePosture.INFERENTIAL_EVIDENCE_UNAVAILABLE:
        state = PerformanceEvidencePolicyState.EVIDENCE_INSUFFICIENT
    elif support.posture is CombinedEvidencePosture.NO_DESCRIPTIVE_CHANGE:
        state = PerformanceEvidencePolicyState.NO_CHANGE_EVIDENCE
    elif support.posture is CombinedEvidencePosture.DESCRIPTIVE_CHANGE_WITHOUT_STATISTICAL_DETECTION:
        state = PerformanceEvidencePolicyState.DESCRIPTIVE_CHANGE_ONLY
    elif support.descriptive_direction.value == "improving":
        state = PerformanceEvidencePolicyState.SUPPORTS_IMPROVEMENT
    elif support.descriptive_direction.value == "declining":
        state = PerformanceEvidencePolicyState.SUPPORTS_DECLINE
    else:
        state = PerformanceEvidencePolicyState.EVIDENCE_INSUFFICIENT

    return PerformanceEvidencePolicyAssessment(
        business_id=support.business_id,
        metric_name=support.metric_name,
        unit=support.unit,
        state=state,
        observation_ids=support.statistical_observation_ids,
    )
