from dataclasses import dataclass
from enum import Enum

from .controlled_experiment_outcome_summary import ControlledExperimentOutcomeSummary


class ExperimentVariantComparisonStatus(str, Enum):
    APPLICABLE = "applicable"
    VARIANT_NOT_FOUND = "variant_not_found"
    SAME_VARIANT = "same_variant"
    INSUFFICIENT_VARIANT_EVIDENCE = "insufficient_variant_evidence"
    INCOMPATIBLE_CONTEXT = "incompatible_context"


@dataclass(frozen=True)
class ExperimentVariantComparison:
    experiment_id: str
    metric_name: str
    first_variant: str
    second_variant: str
    first_count: int
    second_count: int
    first_average: float | None
    second_average: float | None
    average_difference: float | None
    relative_difference: float | None
    first_observation_ids: tuple[str, ...]
    second_observation_ids: tuple[str, ...]
    status: ExperimentVariantComparisonStatus


def compare_experiment_variants(
    *,
    summary: ControlledExperimentOutcomeSummary,
    first_variant: str,
    second_variant: str,
) -> ExperimentVariantComparison:
    if not first_variant.strip() or not second_variant.strip():
        raise ValueError("variant names cannot be empty")

    base = dict(
        experiment_id=summary.experiment_id,
        metric_name=summary.metric_name,
        first_variant=first_variant,
        second_variant=second_variant,
    )

    if first_variant == second_variant:
        return ExperimentVariantComparison(
            **base, first_count=0, second_count=0, first_average=None,
            second_average=None, average_difference=None, relative_difference=None,
            first_observation_ids=(), second_observation_ids=(),
            status=ExperimentVariantComparisonStatus.SAME_VARIANT,
        )

    first = summary.variants.get(first_variant)
    second = summary.variants.get(second_variant)
    if first is None or second is None:
        return ExperimentVariantComparison(
            **base, first_count=first.count if first else 0,
            second_count=second.count if second else 0,
            first_average=first.average if first else None,
            second_average=second.average if second else None,
            average_difference=None, relative_difference=None,
            first_observation_ids=first.observation_ids if first else (),
            second_observation_ids=second.observation_ids if second else (),
            status=ExperimentVariantComparisonStatus.VARIANT_NOT_FOUND,
        )

    difference = second.average - first.average
    relative = None if first.average == 0 else difference / first.average

    return ExperimentVariantComparison(
        **base,
        first_count=first.count,
        second_count=second.count,
        first_average=first.average,
        second_average=second.average,
        average_difference=difference,
        relative_difference=relative,
        first_observation_ids=first.observation_ids,
        second_observation_ids=second.observation_ids,
        status=ExperimentVariantComparisonStatus.APPLICABLE,
    )
