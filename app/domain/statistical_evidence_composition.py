from dataclasses import dataclass
from enum import Enum

from .performance_history import PerformanceWindow

from .performance_history import PerformanceWindow
from .performance_reliability import SourceReliabilityAssessment
from .statistical_mean_comparison import MeanComparisonResult, MeanComparisonStatus


class StatisticalEvidenceEligibilityReason(str, Enum):
    ELIGIBLE = "eligible"
    STATISTICAL_RESULT_NOT_APPLICABLE = "statistical_result_not_applicable"
    INSUFFICIENT_EVIDENCE_QUALITY = "insufficient_evidence_quality"
    INSUFFICIENT_SOURCE_RELIABILITY = "insufficient_source_reliability"


class StatisticalEvidenceInterpretation(str, Enum):
    STATISTICALLY_DETECTED_DIFFERENCE = "statistically_detected_difference"
    NO_STATISTICALLY_DETECTED_DIFFERENCE = "no_statistically_detected_difference"
    STATISTICAL_RESULT_NOT_APPLICABLE = "statistical_result_not_applicable"


@dataclass(frozen=True)
class StatisticalEvidenceComposition:
    business_id: str
    metric_name: str
    unit: str
    method: str
    observation_ids: tuple[str, ...]
    eligible: bool
    reason: StatisticalEvidenceEligibilityReason
    interpretation: StatisticalEvidenceInterpretation
    alpha: float
    first_window: PerformanceWindow
    second_window: PerformanceWindow
    current_evidence_quality: float
    baseline_evidence_quality: float
    current_source_reliability: SourceReliabilityAssessment
    baseline_source_reliability: SourceReliabilityAssessment
    first_window: PerformanceWindow
    second_window: PerformanceWindow
    current_evidence_quality: float
    baseline_evidence_quality: float
    current_source_reliability: SourceReliabilityAssessment
    baseline_source_reliability: SourceReliabilityAssessment

    def __post_init__(self) -> None:
        if not self.business_id.strip() or not self.metric_name.strip() or not self.unit.strip():
            raise ValueError("business_id, metric_name, and unit cannot be empty")
        if not self.method.strip():
            raise ValueError("method cannot be empty")
        if not 0 < self.alpha < 1:
            raise ValueError("alpha must be between zero and one")
        if self.first_window.end > self.second_window.start:
            raise ValueError("statistical evidence windows cannot overlap")
        for name, quality in ((
            "current_evidence_quality", self.current_evidence_quality),
            ("baseline_evidence_quality", self.baseline_evidence_quality),
        ):
            if not 0 <= quality <= 100:
                raise ValueError(f"{name} must be between 0 and 100")
        if self.first_window.end > self.second_window.start:
            raise ValueError("statistical evidence windows must not overlap")
        for name, value in (("current_evidence_quality", self.current_evidence_quality), ("baseline_evidence_quality", self.baseline_evidence_quality)):
            if not 0 <= value <= 100:
                raise ValueError(f"{name} must be between 0 and 100")
        if not self.observation_ids:
            raise ValueError("observation_ids cannot be empty")
        if len(set(self.observation_ids)) != len(self.observation_ids):
            raise ValueError("observation_ids must be unique")
        if self.eligible != (
            self.reason is StatisticalEvidenceEligibilityReason.ELIGIBLE
        ):
            raise ValueError("eligible state must match reason")


def compose_statistical_evidence(
    *,
    comparison: MeanComparisonResult,
    current_evidence_quality: float,
    baseline_evidence_quality: float,
    current_source_reliability: SourceReliabilityAssessment,
    baseline_source_reliability: SourceReliabilityAssessment,
    minimum_evidence_quality: float = 60,
) -> StatisticalEvidenceComposition:
    if not 0 <= current_evidence_quality <= 100:
        raise ValueError("current_evidence_quality must be between 0 and 100")
    if not 0 <= baseline_evidence_quality <= 100:
        raise ValueError("baseline_evidence_quality must be between 0 and 100")
    if not 0 <= minimum_evidence_quality <= 100:
        raise ValueError("minimum_evidence_quality must be between 0 and 100")

    observation_ids = comparison.first_observation_ids + comparison.second_observation_ids

    if comparison.status is not MeanComparisonStatus.APPLICABLE:
        return _compose(
            comparison=comparison,
            eligible=False,
            reason=StatisticalEvidenceEligibilityReason.STATISTICAL_RESULT_NOT_APPLICABLE,
            interpretation=StatisticalEvidenceInterpretation.STATISTICAL_RESULT_NOT_APPLICABLE,
            current_evidence_quality=current_evidence_quality,
            baseline_evidence_quality=baseline_evidence_quality,
            current_source_reliability=current_source_reliability,
            baseline_source_reliability=baseline_source_reliability,
        )

    if (
        current_evidence_quality < minimum_evidence_quality
        or baseline_evidence_quality < minimum_evidence_quality
    ):
        return _compose(
            comparison=comparison,
            eligible=False,
            reason=StatisticalEvidenceEligibilityReason.INSUFFICIENT_EVIDENCE_QUALITY,
            interpretation=_interpretation(comparison),
            current_evidence_quality=current_evidence_quality,
            baseline_evidence_quality=baseline_evidence_quality,
            current_source_reliability=current_source_reliability,
            baseline_source_reliability=baseline_source_reliability,
        )

    if not current_source_reliability.eligible or not baseline_source_reliability.eligible:
        return _compose(
            comparison=comparison,
            eligible=False,
            reason=StatisticalEvidenceEligibilityReason.INSUFFICIENT_SOURCE_RELIABILITY,
            interpretation=_interpretation(comparison),
            current_evidence_quality=current_evidence_quality,
            baseline_evidence_quality=baseline_evidence_quality,
            current_source_reliability=current_source_reliability,
            baseline_source_reliability=baseline_source_reliability,
        )

    return _compose(
        comparison=comparison,
        eligible=True,
        reason=StatisticalEvidenceEligibilityReason.ELIGIBLE,
        interpretation=_interpretation(comparison),
        current_evidence_quality=current_evidence_quality,
        baseline_evidence_quality=baseline_evidence_quality,
        current_source_reliability=current_source_reliability,
        baseline_source_reliability=baseline_source_reliability,
    )


def _interpretation(comparison: MeanComparisonResult) -> StatisticalEvidenceInterpretation:
    if comparison.rejects_null:
        return StatisticalEvidenceInterpretation.STATISTICALLY_DETECTED_DIFFERENCE
    return StatisticalEvidenceInterpretation.NO_STATISTICALLY_DETECTED_DIFFERENCE


def _compose(
    *,
    comparison: MeanComparisonResult,
    eligible: bool,
    reason: StatisticalEvidenceEligibilityReason,
    interpretation: StatisticalEvidenceInterpretation,
    current_evidence_quality: float,
    baseline_evidence_quality: float,
    current_source_reliability: SourceReliabilityAssessment,
    baseline_source_reliability: SourceReliabilityAssessment,
) -> StatisticalEvidenceComposition:
    return StatisticalEvidenceComposition(
        business_id=comparison.business_id,
        metric_name=comparison.metric_name,
        unit=comparison.unit,
        method=comparison.method,
        observation_ids=(
            comparison.first_observation_ids + comparison.second_observation_ids
        ),
        eligible=eligible,
        reason=reason,
        interpretation=interpretation,
        alpha=comparison.alpha,
        first_window=comparison.first_window,
        second_window=comparison.second_window,
        current_evidence_quality=current_evidence_quality,
        baseline_evidence_quality=baseline_evidence_quality,
        current_source_reliability=current_source_reliability,
        baseline_source_reliability=baseline_source_reliability,
    )
