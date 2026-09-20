from dataclasses import dataclass

from .controlled_experiment_evidence import ExperimentObservation
from .controlled_experiment_readiness import ExperimentReadiness
from .validation_experiment import ValidationExperiment


@dataclass(frozen=True)
class ExperimentVariantSummary:
    variant: str
    count: int
    average: float
    minimum: float
    maximum: float
    average_evidence_quality: float
    observation_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.variant.strip():
            raise ValueError("variant cannot be empty")
        if self.count <= 0:
            raise ValueError("count must be greater than zero")
        if self.minimum > self.maximum:
            raise ValueError("minimum cannot exceed maximum")
        if len(self.observation_ids) != self.count:
            raise ValueError("observation_ids count must match count")
        if len(set(self.observation_ids)) != self.count:
            raise ValueError("observation_ids must be unique")


@dataclass(frozen=True)
class ControlledExperimentOutcomeSummary:
    experiment_id: str
    metric_name: str
    variants: dict[str, ExperimentVariantSummary]
    readiness_status: str

    def __post_init__(self) -> None:
        if not self.experiment_id.strip() or not self.metric_name.strip():
            raise ValueError("experiment_id and metric_name cannot be empty")
        if not self.variants:
            raise ValueError("variants cannot be empty")


def summarize_experiment_outcomes(
    *,
    experiment: ValidationExperiment,
    observations: tuple[ExperimentObservation, ...],
    readiness: ExperimentReadiness,
    metric_name: str,
    minimum_evidence_quality: int = 60,
) -> ControlledExperimentOutcomeSummary:
    if not metric_name.strip():
        raise ValueError("metric_name cannot be empty")
    if not 0 <= minimum_evidence_quality <= 100:
        raise ValueError("minimum_evidence_quality must be between 0 and 100")
    if readiness.experiment_id != experiment.id:
        raise ValueError("readiness does not belong to experiment")

    if any(
        observation.experiment_id != experiment.id
        or observation.metric_name != metric_name
        for observation in observations
    ):
        raise ValueError("observation context does not match experiment or metric")

    ids = tuple(observation.id for observation in observations)
    if len(set(ids)) != len(ids):
        raise ValueError("observation identities must be unique")

    variants: dict[str, ExperimentVariantSummary] = {}
    for variant in experiment.variants:
        selected = tuple(
            observation
            for observation in observations
            if observation.variant == variant
            and observation.evidence_quality >= minimum_evidence_quality
        )
        if not selected:
            continue
        values = tuple(float(observation.observed_value) for observation in selected)
        observation_ids = tuple(observation.id for observation in selected)
        variants[variant] = ExperimentVariantSummary(
            variant=variant,
            count=len(values),
            average=sum(values) / len(values),
            minimum=min(values),
            maximum=max(values),
            average_evidence_quality=sum(
                observation.evidence_quality for observation in selected
            ) / len(selected),
            observation_ids=observation_ids,
        )

    return ControlledExperimentOutcomeSummary(
        experiment_id=experiment.id,
        metric_name=metric_name,
        variants=variants,
        readiness_status=readiness.status.value,
    )
