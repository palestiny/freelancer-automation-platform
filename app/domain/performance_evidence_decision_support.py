from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from .metric_direction_policy import (
    MetricDirectionInterpretation,
    MetricDirectionPolicy,
    interpret_metric_direction,
)
from .performance_history import PerformanceWindow
from .performance_trend import PerformanceTrend
from .statistical_evidence_composition import (
    StatisticalEvidenceComposition,
    StatisticalEvidenceInterpretation,
)


class DescriptiveDirection(str, Enum):
    INCREASED = "increased"
    DECREASED = "decreased"
    # Legacy business-semantic values retained for existing consumers.
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

    current_window_start: datetime | None = None
    current_window_end: datetime | None = None
    baseline_window_start: datetime | None = None
    baseline_window_end: datetime | None = None
    statistical_method: str = ""
    statistical_first_window: PerformanceWindow | None = None
    statistical_second_window: PerformanceWindow | None = None
    statistical_difference_direction: DescriptiveDirection = DescriptiveDirection.UNAVAILABLE
    current_observation_ids: tuple[str, ...] = ()
    baseline_observation_ids: tuple[str, ...] = ()
    metric_direction_interpretation: MetricDirectionInterpretation = MetricDirectionInterpretation.NOT_INTERPRETABLE

    def __post_init__(self) -> None:
        for name in ("business_id", "metric_name", "unit"):
            if not getattr(self, name).strip():
                raise ValueError(f"{name} cannot be empty")

        for name, ids in (
            ("statistical_observation_ids", self.statistical_observation_ids),
            ("current_observation_ids", self.current_observation_ids),
            ("baseline_observation_ids", self.baseline_observation_ids),
        ):
            if not ids:
                raise ValueError(f"{name} cannot be empty")
            if any(not isinstance(value, str) or not value.strip() for value in ids):
                raise ValueError(f"{name} must contain non-empty strings")
            if len(set(ids)) != len(ids):
                raise ValueError(f"{name} must be unique")

        if set(self.current_observation_ids) & set(self.baseline_observation_ids):
            raise ValueError(
                "current_observation_ids and baseline_observation_ids must be disjoint"
            )


        for name, value in (("current_window_start", self.current_window_start), ("current_window_end", self.current_window_end), ("baseline_window_start", self.baseline_window_start), ("baseline_window_end", self.baseline_window_end)):
            if value is not None and not isinstance(value, datetime):
                raise TypeError(f"{name} must be a datetime or None")

        if self.current_window_start is not None and self.current_window_end is not None and self.current_window_end <= self.current_window_start:
            raise ValueError("current window must end after it starts")
        if self.baseline_window_start is not None and self.baseline_window_end is not None and self.baseline_window_end <= self.baseline_window_start:
            raise ValueError("baseline window must end after it starts")

        if self.inferential_status is not InferentialStatus.UNAVAILABLE:
            if not self.statistical_method.strip():
                raise ValueError(
                    "statistical_method is required when inferential evidence is available"
                )
            if self.statistical_first_window is None or self.statistical_second_window is None:
                raise ValueError(
                    "statistical windows are required when inferential evidence is available"
                )

        if (
            self.inferential_status is InferentialStatus.STATISTICAL_DIFFERENCE_DETECTED
            and self.statistical_difference_direction is DescriptiveDirection.UNAVAILABLE
        ):
            raise ValueError(
                "statistical difference direction is required when a difference is detected"
            )

        if (
            self.inferential_status is InferentialStatus.STATISTICAL_DIFFERENCE_DETECTED
            and self.posture is CombinedEvidencePosture.DESCRIPTIVE_CHANGE_WITH_STATISTICAL_DETECTION
            and self.descriptive_direction is not self.statistical_difference_direction
        ):
            raise ValueError(
                "descriptive and statistical directions must be matching for the detection posture"
            )

        if (
            self.inferential_status is InferentialStatus.STATISTICAL_DIFFERENCE_DETECTED
            and self.posture is CombinedEvidencePosture.STATISTICAL_AND_DESCRIPTIVE_DIRECTION_CONFLICT
            and self.descriptive_direction is self.statistical_difference_direction
        ):
            raise ValueError(
                "conflict posture requires opposite descriptive and statistical directions"
            )

        if (
            self.inferential_status is InferentialStatus.UNAVAILABLE
            and self.statistical_difference_direction is not DescriptiveDirection.UNAVAILABLE
        ):
            raise ValueError(
                "statistical_difference_direction must be unavailable when inferential evidence is unavailable"
            )

        if (
            self.inferential_status is InferentialStatus.UNAVAILABLE
            and self.posture
            not in (
                CombinedEvidencePosture.INFERENTIAL_EVIDENCE_UNAVAILABLE,
                CombinedEvidencePosture.CONTEXT_INVALID,
            )
        ):
            raise ValueError(
                "unavailable inferential evidence cannot use an inferential-result posture"
            )



def compose_performance_evidence(
    *,
    trend: PerformanceTrend,
    statistical_evidence: StatisticalEvidenceComposition,
    business_id: str,
    metric_direction_policy: MetricDirectionPolicy | None = None,
) -> PerformanceEvidenceDecisionSupport:
    if not isinstance(business_id, str) or not business_id.strip():
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
            metric_direction_interpretation=interpret_metric_direction(
                direction=_descriptive_direction(trend), policy=metric_direction_policy
            ),
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
        metric_direction_interpretation=interpret_metric_direction(
            direction=descriptive, policy=metric_direction_policy
        ),
    )


def _result(
    *,
    trend: PerformanceTrend,
    business_id: str,
    inferential_status: InferentialStatus,
    posture: CombinedEvidencePosture,
    statistical_evidence: StatisticalEvidenceComposition,
    metric_direction_interpretation: MetricDirectionInterpretation,
) -> PerformanceEvidenceDecisionSupport:
    difference_direction = (
        _difference_direction(statistical_evidence)
        if inferential_status is not InferentialStatus.UNAVAILABLE
        else DescriptiveDirection.UNAVAILABLE
    )
    return PerformanceEvidenceDecisionSupport(
        business_id=business_id,
        metric_name=trend.metric_name,
        unit=trend.unit,
        descriptive_direction=_descriptive_direction(trend),
        inferential_status=inferential_status,
        posture=posture,
        statistical_observation_ids=statistical_evidence.observation_ids,
        current_window_start=trend.current_window.start,
        current_window_end=trend.current_window.end,
        baseline_window_start=trend.baseline_window.start,
        baseline_window_end=trend.baseline_window.end,
        statistical_method=statistical_evidence.method,
        statistical_first_window=statistical_evidence.first_window,
        statistical_second_window=statistical_evidence.second_window,
        statistical_difference_direction=difference_direction,
        current_observation_ids=trend.current_observation_ids,
        baseline_observation_ids=trend.baseline_observation_ids,
        metric_direction_interpretation=metric_direction_interpretation,
    )


def _descriptive_direction(trend: PerformanceTrend) -> DescriptiveDirection:
    if trend.absolute_change > 0:
        return DescriptiveDirection.INCREASED
    if trend.absolute_change < 0:
        return DescriptiveDirection.DECREASED
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
        return DescriptiveDirection.INCREASED
    if evidence.mean_difference < 0:
        return DescriptiveDirection.DECREASED
    return DescriptiveDirection.NO_CHANGE


def _directions_align(
    left: DescriptiveDirection,
    right: DescriptiveDirection,
) -> bool:
    return left is right



def _sign(value: float | None) -> int:
    if value is None or value == 0:
        return 0
    return 1 if value > 0 else -1
