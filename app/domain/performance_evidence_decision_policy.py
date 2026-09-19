from enum import Enum

from .performance_evidence_decision_support import CombinedEvidencePosture, DescriptiveDirection, InferentialStatus, PerformanceEvidenceDecisionSupport


class PerformanceEvidenceState(str, Enum):
    SUPPORTS_IMPROVEMENT = "supports_improvement"
    SUPPORTS_DECLINE = "supports_decline"
    DESCRIPTIVE_CHANGE_WITHOUT_STATISTICAL_DETECTION = "descriptive_change_without_statistical_detection"
    NO_MATERIAL_DESCRIPTIVE_CHANGE = "no_material_descriptive_change"
    INSUFFICIENT_INFERENTIAL_EVIDENCE = "insufficient_inferential_evidence"
    CONTEXT_INVALID = "context_invalid"


def derive_performance_evidence_state(evidence: PerformanceEvidenceDecisionSupport) -> PerformanceEvidenceState:
    if evidence.posture is CombinedEvidencePosture.CONTEXT_INVALID:
        return PerformanceEvidenceState.CONTEXT_INVALID
    if evidence.inferential_status is InferentialStatus.UNAVAILABLE:
        return PerformanceEvidenceState.INSUFFICIENT_INFERENTIAL_EVIDENCE
    if evidence.descriptive_direction is DescriptiveDirection.NO_CHANGE:
        return PerformanceEvidenceState.NO_MATERIAL_DESCRIPTIVE_CHANGE
    if evidence.inferential_status is InferentialStatus.NO_STATISTICAL_DIFFERENCE_DETECTED:
        return PerformanceEvidenceState.DESCRIPTIVE_CHANGE_WITHOUT_STATISTICAL_DETECTION
    if evidence.descriptive_direction is DescriptiveDirection.IMPROVING:
        return PerformanceEvidenceState.SUPPORTS_IMPROVEMENT
    if evidence.descriptive_direction is DescriptiveDirection.DECLINING:
        return PerformanceEvidenceState.SUPPORTS_DECLINE
    return PerformanceEvidenceState.INSUFFICIENT_INFERENTIAL_EVIDENCE
