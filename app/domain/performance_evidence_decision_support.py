from dataclasses import dataclass
from enum import Enum

from .performance_trend import PerformanceTrend
from .statistical_evidence_composition import (
    StatisticalEvidenceComposition,
    StatisticalEvidenceInterpretation,
)


class DescriptiveDirection(str, Enum):
    IMPROVING = "improving"
    DECLINING = "declining"
    NO_CHANGE = "no_change"
    UNAVAILABLE = "unavailable"


class InferentialStatus(str, Enum):
    STATISTICAL_DIFFERENCE_DETECTED = "statistical_difference_detected"
    NO_STATISTICAL_DIFFERENCE_DETECTED = "no_statistical_difference_detected"
    UNAVAILABLE = "unavailable"


class CombinedEvidencePosture(str, Enum):
    DESCRIPTIVE_AND_STATISTICAL_ALIGNMENT = "descriptive_and_statistical_alignment"
    DESCRIPTIVE_CHANGE_WITHOUT_STATISTICAL_DETECTION = "descriptive_change_without_statistical_detection"
    NO_DESCRIPTIVE_CHANGE = "no_descriptive_change"
    INFERENTIAL_EVIDENCE_UNAVAILABLE = "inferential_evidence_unavailable"
    CONTEXT_INVALID = "context_invalid"


@dataclass(frozen=True)
class PerformanceEvidenceDecisionSupport:
    business_id: str
    metric_name: str
    unit: str
    descriptive_direction: DescriptiveDirection
    inferential_status: InferentialStatus
    posture: CombinedEvidencePosture
    statistical_observation_ids: tuple[str, ...]


def compose_performance_evidence(
    *,
    trend: PerformanceTrend,
    statistical_evidence: StatisticalEvidenceComposition,
    business_id: str,
) -> PerformanceEvidenceDecisionSupport:
    if not business_id.strip():
        raise ValueError("business_id cannot be empty")

    if (
        statistical_evidence.business_id != business_id
        or statistical_evidence.metric_name != trend.metric_name
        or statistical_evidence.unit != trend.unit
    ):
        return PerformanceEvidenceDecisionSupport(
            business_id=business_id,
            metric_name=trend.metric_name,
            unit=trend.unit,
            descriptive_direction=_descriptive_direction(trend),
            inferential_status=InferentialStatus.UNAVAILABLE,
            posture=CombinedEvidencePosture.CONTEXT_INVALID,
            statistical_observation_ids=statistical_evidence.observation_ids,
        )

    descriptive = _descriptive_direction(trend)
    inferential = _inferential_status(statistical_evidence)

    if inferential is InferentialStatus.UNAVAILABLE:
        posture = CombinedEvidencePosture.INFERENTIAL_EVIDENCE_UNAVAILABLE
    elif descriptive is DescriptiveDirection.NO_CHANGE:
        posture = CombinedEvidencePosture.NO_DESCRIPTIVE_CHANGE
    elif inferential is InferentialStatus.STATISTICAL_DIFFERENCE_DETECTED:
        posture = CombinedEvidencePosture.DESCRIPTIVE_AND_STATISTICAL_ALIGNMENT
    else:
        posture = CombinedEvidencePosture.DESCRIPTIVE_CHANGE_WITHOUT_STATISTICAL_DETECTION

    return PerformanceEvidenceDecisionSupport(
        business_id=business_id,
        metric_name=trend.metric_name,
        unit=trend.unit,
        descriptive_direction=descriptive,
        inferential_status=inferential,
        posture=posture,
        statistical_observation_ids=statistical_evidence.observation_ids,
    )


def _descriptive_direction(trend: PerformanceTrend) -> DescriptiveDirection:
    if trend.absolute_change > 0:
        return DescriptiveDirection.IMPROVING
    if trend.absolute_change < 0:
        return DescriptiveDirection.DECLINING
    return DescriptiveDirection.NO_CHANGE


def _inferential_status(
    evidence: StatisticalEvidenceComposition,
) -> InferentialStatus:
    if not evidence.eligible:
        return InferentialStatus.UNAVAILABLE
    if evidence.interpretation is StatisticalEvidenceInterpretation.STATISTICALLY_DETECTED_DIFFERENCE:
        return InferentialStatus.STATISTICAL_DIFFERENCE_DETECTED
    if evidence.interpretation is StatisticalEvidenceInterpretation.NO_STATISTICALLY_DETECTED_DIFFERENCE:
        return InferentialStatus.NO_STATISTICAL_DIFFERENCE_DETECTED
    return InferentialStatus.UNAVAILABLE
