from dataclasses import dataclass
from enum import Enum

from .controlled_experiment_hypothesis_policy import (
    ExperimentHypothesisDirection,
    HypothesisPolicyOutcome,
)
from .controlled_experiment_policy_review_handoff import ExperimentPolicyReviewHandoff


class ExperimentPolicyReviewDecisionOutcome(str, Enum):
    ACCEPT = "accept"
    REJECT = "reject"
    REQUEST_MORE_EVIDENCE = "request_more_evidence"


@dataclass(frozen=True)
class ExperimentPolicyReviewDecision:
    decision_id: str
    handoff_id: str
    experiment_id: str
    metric_name: str
    direction: ExperimentHypothesisDirection
    policy_outcome: HypothesisPolicyOutcome
    outcome: ExperimentPolicyReviewDecisionOutcome
    reviewer_id: str
    rationale: str
    observation_ids: tuple[str, ...]
    authorized: bool = False

    def __post_init__(self) -> None:
        for name in (
            "decision_id",
            "handoff_id",
            "experiment_id",
            "metric_name",
            "reviewer_id",
            "rationale",
        ):
            if not getattr(self, name).strip():
                raise ValueError(f"{name} cannot be empty")
        if not self.observation_ids:
            raise ValueError("observation_ids cannot be empty")
        if len(set(self.observation_ids)) != len(self.observation_ids):
            raise ValueError("observation_ids must be unique")
        if self.authorized:
            raise ValueError("review decision cannot authorize execution")
        if not isinstance(self.outcome, ExperimentPolicyReviewDecisionOutcome):
            raise TypeError("outcome must be an ExperimentPolicyReviewDecisionOutcome")


def create_experiment_policy_review_decision(
    *,
    handoff: ExperimentPolicyReviewHandoff,
    reviewer_id: str,
    outcome: ExperimentPolicyReviewDecisionOutcome,
    rationale: str,
    decision_id: str = "review-decision",
) -> ExperimentPolicyReviewDecision:
    if not isinstance(handoff, ExperimentPolicyReviewHandoff):
        raise TypeError("handoff must be an ExperimentPolicyReviewHandoff")
    return ExperimentPolicyReviewDecision(
        decision_id=decision_id,
        handoff_id=handoff.handoff_id,
        experiment_id=handoff.experiment_id,
        metric_name=handoff.metric_name,
        direction=handoff.direction,
        policy_outcome=handoff.policy_outcome,
        outcome=outcome,
        reviewer_id=reviewer_id,
        rationale=rationale,
        observation_ids=handoff.observation_ids,
        authorized=False,
    )
