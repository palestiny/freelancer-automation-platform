from dataclasses import dataclass
from enum import Enum


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


def evaluate_experiment_hypothesis(*, synthesis: dict, policy: ControlledExperimentHypothesisPolicy) -> ControlledExperimentHypothesisPolicyResult:
    required = (
        "experiment_id",
        "metric_name",
        "descriptive_direction",
        "statistical_difference_detected",
        "evidence_eligible",
        "observation_ids",
    )
    if any(key not in synthesis for key in required):
        return ControlledExperimentHypothesisPolicyResult(
            policy.experiment_id,
            policy.metric_name,
            policy.direction,
            HypothesisPolicyOutcome.POLICY_INAPPLICABLE,
            tuple(synthesis.get("observation_ids", ())),
        )
    if synthesis["experiment_id"] != policy.experiment_id or synthesis["metric_name"] != policy.metric_name:
        outcome = HypothesisPolicyOutcome.POLICY_INAPPLICABLE
    elif not synthesis["evidence_eligible"]:
        outcome = HypothesisPolicyOutcome.INSUFFICIENT_EVIDENCE
    else:
        direction = synthesis["descriptive_direction"]
        detected = synthesis["statistical_difference_detected"]
        aligned = (
            direction == "increased" and policy.direction is ExperimentHypothesisDirection.INCREASES
        ) or (
            direction == "decreased" and policy.direction is ExperimentHypothesisDirection.DECREASES
        )
        if not aligned or (policy.require_statistical_difference and not detected):
            outcome = HypothesisPolicyOutcome.DOES_NOT_SUPPORT_HYPOTHESIS
        else:
            outcome = HypothesisPolicyOutcome.SUPPORTS_HYPOTHESIS
    return ControlledExperimentHypothesisPolicyResult(
        policy.experiment_id,
        policy.metric_name,
        policy.direction,
        outcome,
        tuple(synthesis["observation_ids"]),
    )
