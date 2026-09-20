from dataclasses import dataclass
from enum import Enum

from .controlled_experiment_hypothesis_policy import (
    ControlledExperimentHypothesisPolicyResult,
    ExperimentHypothesisDirection,
    HypothesisPolicyOutcome,
)


class ExperimentPolicyReviewPosture(str, Enum):
    REVIEW_SUPPORTS_HYPOTHESIS = "review_supports_hypothesis"
    REVIEW_DOES_NOT_SUPPORT_HYPOTHESIS = "review_does_not_support_hypothesis"
    REVIEW_INSUFFICIENT_EVIDENCE = "review_insufficient_evidence"
    REVIEW_POLICY_INAPPLICABLE = "review_policy_inapplicable"


@dataclass(frozen=True)
class ExperimentPolicyReviewHandoff:
    handoff_id: str
    experiment_id: str
    metric_name: str
    direction: ExperimentHypothesisDirection
    policy_outcome: HypothesisPolicyOutcome
    posture: ExperimentPolicyReviewPosture
    observation_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.handoff_id.strip() or not self.experiment_id.strip() or not self.metric_name.strip():
            raise ValueError("handoff_id, experiment_id, and metric_name cannot be empty")
        if not self.observation_ids:
            raise ValueError("observation_ids cannot be empty")
        if len(set(self.observation_ids)) != len(self.observation_ids):
            raise ValueError("observation_ids must be unique")


def create_experiment_policy_review_handoff(
    *,
    handoff_id: str,
    policy_result: ControlledExperimentHypothesisPolicyResult,
) -> ExperimentPolicyReviewHandoff:
    if not handoff_id.strip():
        raise ValueError("handoff_id cannot be empty")
    mapping = {
        HypothesisPolicyOutcome.SUPPORTS_HYPOTHESIS: ExperimentPolicyReviewPosture.REVIEW_SUPPORTS_HYPOTHESIS,
        HypothesisPolicyOutcome.DOES_NOT_SUPPORT_HYPOTHESIS: ExperimentPolicyReviewPosture.REVIEW_DOES_NOT_SUPPORT_HYPOTHESIS,
        HypothesisPolicyOutcome.INSUFFICIENT_EVIDENCE: ExperimentPolicyReviewPosture.REVIEW_INSUFFICIENT_EVIDENCE,
        HypothesisPolicyOutcome.POLICY_INAPPLICABLE: ExperimentPolicyReviewPosture.REVIEW_POLICY_INAPPLICABLE,
    }
    return ExperimentPolicyReviewHandoff(
        handoff_id=handoff_id,
        experiment_id=policy_result.experiment_id,
        metric_name=policy_result.metric_name,
        direction=policy_result.direction,
        policy_outcome=policy_result.outcome,
        posture=mapping[policy_result.outcome],
        observation_ids=policy_result.observation_ids,
    )
