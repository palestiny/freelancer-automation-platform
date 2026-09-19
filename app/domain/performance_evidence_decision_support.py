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
    NO_STATISTICALLY_DETECTED_DIFFERENCE = "no_statistically_detected_difference"
    UNAVAILABLE = "unavailable"


class CombinedEvidencePosture(str, Enum):
    DESCRIPTIVE_CHANGE_WITH_STATISTICAL_DETECTION = (
        "descriptive_change_with_statistical_detection"
    )
    DESCRIPTIVE_CHANGE_WITHOUT_STATISTICAL_DETECTION = (
        "descriptive_change_without_statistical_detection"
    )
    STATISTICAL_AND_DESCRIPTIVE_DIRECTION_CONFLICT = (
        "statistical_and_descriptive_direction_conflict"
    )
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
    statistical_difference_direction: DescriptiveDirection
    current_observation_ids: tuple[str, ...]
    baseline_observation_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        for name in ("business_id", "metric_name", "unit"):
            if not getattr(self, name).strip():
                raise ValueError(f"{name} cannot be empty")

        for name, ids in (
            ("statistical_observation_ids", self.statistical_observation_ids),
            ("current_observation_ids", self.current_observation_ids),
            ("baseline_observation_ids", self.baseline_observation_ids),
        ):
            if len(set(ids)) != len(ids):
                raise ValueError(f"{name} must be unique")


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
        or statistical_evidence.first_window != trend.baseline_window
        or statistical_evidence.second_window != trend.current_window
    ):
        return _result(
            trend=trend,
            business_id=business_id,
            inferential_status=InferentialStatus.UNAVAILABLE,
            posture=CombinedEvidencePosture.CONTEXT_INVALID,
            statistical_evidence=statistical_evidence,
        )

    descriptive = _descriptive_direction(trend)
    inferential = _inferential_status(statistical_evidence)

    if inferential is InferentialStatus.UNAVAILABLE:
        posture = CombinedEvidencePosture.INFERENTIAL_EVIDENCE_UNAVAILABLE
    elif descriptive is DescriptiveDirection.NO_CHANGE:
        posture = CombinedEvidencePosture.NO_DESCRIPTIVE_CHANGE
    elif inferential is InferentialStatus.STATISTICAL_DIFFERENCE_DETECTED:
        difference = _difference_direction(statistical_evidence)
        if not _directions_align(descriptive, difference):
            posture = CombinedEvidencePosture.STATISTICAL_AND_DESCRIPTIVE_DIRECTION_CONFLICT
        else:
            posture = CombinedEvidencePosture.DESCRIPTIVE_CHANGE_WITH_STATISTICAL_DETECTION
    else:
        posture = CombinedEvidencePosture.DESCRIPTIVE_CHANGE_WITHOUT_STATISTICAL_DETECTION

    return _result(
        trend=trend,
        business_id=business_id,
        inferential_status=inferential,
        posture=posture,
        statistical_evidence=statistical_evidence,
    )


def _result(
    *,
    trend: PerformanceTrend,
    business_id: str,
    inferential_status: InferentialStatus,
    posture: CombinedEvidencePosture,
    statistical_evidence: StatisticalEvidenceComposition,
) -> PerformanceEvidenceDecisionSupport:
    return PerformanceEvidenceDecisionSupport(
        business_id=business_id,
        metric_name=trend.metric_name,
        unit=trend.unit,
        descriptive_direction=_descriptive_direction(trend),
        inferential_status=inferential_status,
        posture=posture,
        statistical_observation_ids=statistical_evidence.observation_ids,
        statistical_difference_direction=_difference_direction(statistical_evidence),
        current_observation_ids=trend.current_observation_ids,
        baseline_observation_ids=trend.baseline_observation_ids,
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
    if (
        evidence.interpretation
        is StatisticalEvidenceInterpretation.STATISTICALLY_DETECTED_DIFFERENCE
    ):
        return InferentialStatus.STATISTICAL_DIFFERENCE_DETECTED
    if (
        evidence.interpretation
        is StatisticalEvidenceInterpretation.NO_STATISTICALLY_DETECTED_DIFFERENCE
    ):
        return InferentialStatus.NO_STATISTICALLY_DETECTED_DIFFERENCE
    return InferentialStatus.UNAVAILABLE


def _difference_direction(
    evidence: StatisticalEvidenceComposition,
) -> DescriptiveDirection:
    if evidence.mean_difference is None:
        return DescriptiveDirection.UNAVAILABLE
    if evidence.mean_difference > 0:
        return DescriptiveDirection.IMPROVING
    if evidence.mean_difference < 0:
        return DescriptiveDirection.DECLINING
    return DescriptiveDirection.NO_CHANGE


def _directions_align(
    left: DescriptiveDirection,
    right: DescriptiveDirection,
) -> bool:
    return left is right
