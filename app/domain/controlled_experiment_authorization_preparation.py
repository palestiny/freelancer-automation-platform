from dataclasses import dataclass

from .action_authorization import ActionClass, AutonomyLevel
from .controlled_experiment_policy_review_decision import (
    ExperimentPolicyReviewDecision,
    ExperimentPolicyReviewDecisionOutcome,
)


@dataclass(frozen=True)
class ExperimentAuthorizationRequest:
    request_id: str
    decision_id: str
    handoff_id: str
    experiment_id: str
    metric_name: str
    policy_id: str
    policy_version: str
    action_class: ActionClass
    requested_autonomy: AutonomyLevel
    reviewer_id: str
    rationale: str
    policy_outcome: str
    observation_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        for name in (
            "request_id",
            "decision_id",
            "handoff_id",
            "experiment_id",
            "metric_name",
            "policy_id",
            "policy_version",
            "reviewer_id",
            "rationale",
            "policy_outcome",
        ):
            if not getattr(self, name).strip():
                raise ValueError(f"{name} cannot be empty")
        if not self.observation_ids:
            raise ValueError("observation_ids cannot be empty")
        if len(set(self.observation_ids)) != len(self.observation_ids):
            raise ValueError("observation_ids must be unique")


def prepare_experiment_authorization_request(
    *,
    decision: ExperimentPolicyReviewDecision,
    policy_id: str,
    policy_version: str,
    action_class: ActionClass,
    requested_autonomy: AutonomyLevel,
    request_id: str = "experiment-authorization-request",
) -> ExperimentAuthorizationRequest:
    if not isinstance(decision, ExperimentPolicyReviewDecision):
        raise TypeError("decision must be an ExperimentPolicyReviewDecision")
    if decision.outcome is not ExperimentPolicyReviewDecisionOutcome.ACCEPT:
        raise ValueError("only an accepted review decision can produce an authorization request")
    return ExperimentAuthorizationRequest(
        request_id=request_id,
        decision_id=decision.decision_id,
        handoff_id=decision.handoff_id,
        experiment_id=decision.experiment_id,
        metric_name=decision.metric_name,
        policy_id=policy_id,
        policy_version=policy_version,
        action_class=action_class,
        requested_autonomy=requested_autonomy,
        reviewer_id=decision.reviewer_id,
        rationale=decision.rationale,
        policy_outcome=decision.policy_outcome.value,
        observation_ids=decision.observation_ids,
    )
