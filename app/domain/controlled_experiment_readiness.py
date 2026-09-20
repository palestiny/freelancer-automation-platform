from dataclasses import dataclass
from enum import Enum

from .controlled_experiment_evidence import ExperimentAssignment, ExperimentObservation
from .validation_experiment import ValidationExperiment


class ExperimentReadinessStatus(str, Enum):
    COLLECTING = "collecting"
    READY = "ready"
    INVALID_CONTEXT = "invalid_context"


@dataclass(frozen=True)
class ExperimentReadiness:
    experiment_id: str
    status: ExperimentReadinessStatus
    missing_variants: tuple[str, ...]
    usable_observation_ids: tuple[str, ...]


def assess_experiment_readiness(
    *,
    experiment: ValidationExperiment,
    assignments: tuple[ExperimentAssignment, ...],
    observations: tuple[ExperimentObservation, ...],
    minimum_observations_per_variant: int = 2,
    minimum_evidence_quality: int = 60,
) -> ExperimentReadiness:
    if minimum_observations_per_variant <= 0:
        raise ValueError("minimum_observations_per_variant must be greater than zero")
    if not 0 <= minimum_evidence_quality <= 100:
        raise ValueError("minimum_evidence_quality must be between 0 and 100")
    if not experiment.variants:
        raise ValueError("experiment must declare at least one variant")

    assignment_ids = tuple(a.id for a in assignments)
    if len(set(assignment_ids)) != len(assignment_ids):
        raise ValueError("assignment identities must be unique")

    observation_ids = tuple(o.id for o in observations)
    if len(set(observation_ids)) != len(observation_ids):
        raise ValueError("observation identities must be unique")

    assignment_by_id = {a.id: a for a in assignments}
    counts = {variant: 0 for variant in experiment.variants}
    usable_ids: list[str] = []

    for assignment in assignments:
        if assignment.experiment_id != experiment.id or assignment.variant not in experiment.variants:
            raise ValueError("assignment is incompatible with experiment")

    for observation in observations:
        if observation.experiment_id != experiment.id or observation.variant not in experiment.variants:
            raise ValueError("observation is incompatible with experiment")
        assignment = assignment_by_id.get(observation.assignment_id)
        if assignment is None:
            raise ValueError("observation references an unknown assignment")
        if (
            assignment.subject_id != observation.subject_id
            or assignment.variant != observation.variant
        ):
            raise ValueError("observation lineage does not match assignment")
        if observation.evidence_quality < minimum_evidence_quality:
            continue
        counts[observation.variant] += 1
        usable_ids.append(observation.id)

    missing = tuple(
        variant for variant in experiment.variants
        if counts[variant] < minimum_observations_per_variant
    )
    status = (
        ExperimentReadinessStatus.READY
        if not missing
        else ExperimentReadinessStatus.COLLECTING
    )
    return ExperimentReadiness(
        experiment_id=experiment.id,
        status=status,
        missing_variants=missing,
        usable_observation_ids=tuple(usable_ids),
    )
