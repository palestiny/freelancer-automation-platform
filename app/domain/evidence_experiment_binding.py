from dataclasses import dataclass

from .evidence_learning_handoff import EvidenceHandoffType, EvidenceLearningHandoff
from .validation_experiment import ValidationExperiment


@dataclass(frozen=True)
class EvidenceExperimentBinding:
    handoff_id: str
    experiment_id: str
    business_id: str
    metric_name: str
    unit: str
    observation_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        for name in ("handoff_id", "experiment_id", "business_id", "metric_name", "unit"):
            if not getattr(self, name).strip():
                raise ValueError(f"{name} cannot be empty")
        if not self.observation_ids:
            raise ValueError("observation_ids cannot be empty")
        if len(set(self.observation_ids)) != len(self.observation_ids):
            raise ValueError("observation_ids must be unique")


def bind_evidence_to_experiment(
    *,
    handoff: EvidenceLearningHandoff,
    experiment: ValidationExperiment,
) -> EvidenceExperimentBinding:
    if handoff.handoff_type is not EvidenceHandoffType.EXPERIMENT:
        raise ValueError("handoff must have EXPERIMENT type")
    if handoff.target != experiment.id:
        raise ValueError("handoff target must match experiment id")
    return EvidenceExperimentBinding(
        handoff_id=handoff.handoff_id,
        experiment_id=experiment.id,
        business_id=handoff.business_id,
        metric_name=handoff.metric_name,
        unit=handoff.unit,
        observation_ids=handoff.observation_ids,
    )
