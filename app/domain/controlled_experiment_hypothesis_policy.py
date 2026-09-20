from dataclasses import dataclass
from enum import Enum

from .controlled_experiment_evidence_synthesis import ExperimentEvidenceSynthesis, ExperimentEvidenceSynthesisStatus


class ExperimentHypothesisDirection(str, Enum):
    INCREASES = "increases"
    DECREASES = "decreases"


class HypothesisPolicyOutcome(str, Enum):
    SUPPORTS_HYPOTHESIS = "supports_hypothesis"
    DOES_NOT_SUPPORT_HYPOTHESIS = "does_not_support_hypothesis"
    INSUFFICIENT_EVIDENCE = "insufficient_evidence"
    POLICY_INAPPLICABLE = "policy_inapplicable"


@dataclass(frozen=True)
class ControlledExperimentHypothesisPolicy:
    experiment_id: str
    metric_name: str
    direction: ExperimentHypothesisDirection
    require_statistical_difference: bool = True

    def __post_init__(self) -> None:
        if not self.experiment_id.strip() or not self.metric_name.strip():
            raise ValueError("experiment_id and metric_name cannot be empty")
        if not isinstance(self.direction, ExperimentHypothesisDirection):
            raise TypeError("direction must be an ExperimentHypothesisDirection")
        if not isinstance(self.require_statistical_difference, bool):
            raise TypeError("require_statistical_difference must be a bool")


@dataclass(frozen=True)
class ControlledExperimentHypothesisPolicyResult:
    experiment_id: str
    metric_name: str
    direction: ExperimentHypothesisDirection
    outcome: HypothesisPolicyOutcome
    observation_ids: tuple[str, ...]


def evaluate_experiment_hypothesis(
    *,
    synthesis: ExperimentEvidenceSynthesis,
    policy: ControlledExperimentHypothesisPolicy,
) -> ControlledExperimentHypothesisPolicyResult:
    if not isinstance(synthesis, ExperimentEvidenceSynthesis):
        raise TypeError("synthesis must be an ExperimentEvidenceSynthesis")

    if (
        synthesis.experiment_id != policy.experiment_id
        or synthesis.metric_name != policy.metric_name
    ):
        outcome = HypothesisPolicyOutcome.POLICY_INAPPLICABLE
    elif synthesis.status in (
        ExperimentEvidenceSynthesisStatus.CONTEXT_INVALID,
        ExperimentEvidenceSynthesisStatus.STATISTICAL_EVIDENCE_UNAVAILABLE,
    ):
        outcome = HypothesisPolicyOutcome.INSUFFICIENT_EVIDENCE
    else:
        difference = synthesis.descriptive_difference
        aligned = difference is not None and (
            (difference > 0 and policy.direction is ExperimentHypothesisDirection.INCREASES)
            or (difference < 0 and policy.direction is ExperimentHypothesisDirection.DECREASES)
        )
        if not aligned or (
            policy.require_statistical_difference
            and synthesis.statistical_detected is not True
        ):
            outcome = HypothesisPolicyOutcome.DOES_NOT_SUPPORT_HYPOTHESIS
        else:
            outcome = HypothesisPolicyOutcome.SUPPORTS_HYPOTHESIS

    return ControlledExperimentHypothesisPolicyResult(
        experiment_id=policy.experiment_id,
        metric_name=policy.metric_name,
        direction=policy.direction,
        outcome=outcome,
        observation_ids=synthesis.observation_ids,
    )
