from dataclasses import dataclass
from enum import Enum

from .controlled_experiment_variant_comparison import ExperimentVariantComparison
from .controlled_experiment_statistical_comparison import (
    ExperimentStatisticalComparisonResult,
    ExperimentStatisticalComparisonStatus,
)


class ExperimentEvidenceSynthesisStatus(str, Enum):
    DESCRIPTIVE_AND_STATISTICAL_ALIGNMENT = "descriptive_and_statistical_alignment"
    DESCRIPTIVE_CHANGE_WITHOUT_STATISTICAL_DETECTION = "descriptive_change_without_statistical_detection"
    STATISTICAL_AND_DESCRIPTIVE_DIRECTION_CONFLICT = "statistical_and_descriptive_direction_conflict"
    NO_DETECTED_DIFFERENCE = "no_detected_difference"
    STATISTICAL_EVIDENCE_UNAVAILABLE = "statistical_evidence_unavailable"
    CONTEXT_INVALID = "context_invalid"


@dataclass(frozen=True)
class ExperimentEvidenceSynthesis:
    experiment_id: str
    metric_name: str
    first_variant: str
    second_variant: str
    descriptive_difference: float | None
    statistical_difference: float | None
    statistical_detected: bool | None
    status: ExperimentEvidenceSynthesisStatus
    observation_ids: tuple[str, ...]


def synthesize_experiment_evidence(
    *,
    comparison: ExperimentVariantComparison,
    statistical: ExperimentStatisticalComparisonResult,
) -> ExperimentEvidenceSynthesis:
    context = (
        comparison.experiment_id == statistical.experiment_id
        and comparison.metric_name == statistical.metric_name
        and comparison.first_variant == statistical.first_variant
        and comparison.second_variant == statistical.second_variant
        and comparison.first_observation_ids == statistical.first_observation_ids
        and comparison.second_observation_ids == statistical.second_observation_ids
    )
    ids = comparison.first_observation_ids + comparison.second_observation_ids
    if not context:
        return ExperimentEvidenceSynthesis(
            experiment_id=comparison.experiment_id,
            metric_name=comparison.metric_name,
            first_variant=comparison.first_variant,
            second_variant=comparison.second_variant,
            descriptive_difference=comparison.average_difference,
            statistical_difference=statistical.mean_difference,
            statistical_detected=None,
            status=ExperimentEvidenceSynthesisStatus.CONTEXT_INVALID,
            observation_ids=ids,
        )

    if comparison.average_difference is None:
        descriptive = None
    else:
        descriptive = comparison.average_difference

    if statistical.status is not ExperimentStatisticalComparisonStatus.APPLICABLE:
        return ExperimentEvidenceSynthesis(
            experiment_id=comparison.experiment_id,
            metric_name=comparison.metric_name,
            first_variant=comparison.first_variant,
            second_variant=comparison.second_variant,
            descriptive_difference=descriptive,
            statistical_difference=statistical.mean_difference,
            statistical_detected=None,
            status=ExperimentEvidenceSynthesisStatus.STATISTICAL_EVIDENCE_UNAVAILABLE,
            observation_ids=ids,
        )

    detected = bool(statistical.rejects_null)
    if descriptive == 0:
        status = ExperimentEvidenceSynthesisStatus.NO_DETECTED_DIFFERENCE if not detected else ExperimentEvidenceSynthesisStatus.STATISTICAL_AND_DESCRIPTIVE_DIRECTION_CONFLICT
    elif not detected:
        status = ExperimentEvidenceSynthesisStatus.DESCRIPTIVE_CHANGE_WITHOUT_STATISTICAL_DETECTION
    elif (descriptive > 0) != (statistical.mean_difference > 0):
        status = ExperimentEvidenceSynthesisStatus.STATISTICAL_AND_DESCRIPTIVE_DIRECTION_CONFLICT
    else:
        status = ExperimentEvidenceSynthesisStatus.DESCRIPTIVE_AND_STATISTICAL_ALIGNMENT

    return ExperimentEvidenceSynthesis(
        experiment_id=comparison.experiment_id,
        metric_name=comparison.metric_name,
        first_variant=comparison.first_variant,
        second_variant=comparison.second_variant,
        descriptive_difference=descriptive,
        statistical_difference=statistical.mean_difference,
        statistical_detected=detected,
        status=status,
        observation_ids=ids,
    )
