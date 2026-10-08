from dataclasses import dataclass
from datetime import datetime

from app.application.opportunity_intelligence import OpportunityIntelligenceEvaluator
from app.application.opportunity_prioritizer import OpportunityPrioritizer
from app.domain.opportunity import Opportunity
from app.domain.opportunity_intelligence import (
    EvaluationPolicy,
    OpportunityEvaluation,
)
from app.domain.opportunity_prioritization import (
    OpportunityPriorityDecision,
    PrioritizationPolicy,
)


@dataclass(frozen=True)
class OpportunityDecisionResult:
    """Immutable result of evaluating and prioritizing one opportunity."""

    opportunity_ref: str
    evaluation_ref: str
    evaluation: OpportunityEvaluation
    priority_decision: OpportunityPriorityDecision


class OpportunityDecisionPipeline:
    """Compose existing evaluation and prioritization services without side effects."""

    def __init__(
        self,
        evaluator: OpportunityIntelligenceEvaluator,
        prioritizer: OpportunityPrioritizer,
    ) -> None:
        if not callable(getattr(evaluator, "evaluate", None)):
            raise TypeError("evaluator must provide evaluate()")
        if not callable(getattr(prioritizer, "prioritize", None)):
            raise TypeError("prioritizer must provide prioritize()")
        self._evaluator = evaluator
        self._prioritizer = prioritizer

    def run(
        self,
        *,
        opportunity: Opportunity,
        evaluation_policy: EvaluationPolicy,
        prioritization_policy: PrioritizationPolicy,
        opportunity_ref: str,
        evaluation_ref: str,
        evaluated_at: datetime,
    ) -> OpportunityDecisionResult:
        if not isinstance(opportunity, Opportunity):
            raise TypeError("opportunity must be an Opportunity")
        if not isinstance(evaluation_policy, EvaluationPolicy):
            raise TypeError("evaluation_policy must be an EvaluationPolicy")
        if not isinstance(prioritization_policy, PrioritizationPolicy):
            raise TypeError("prioritization_policy must be a PrioritizationPolicy")
        for name, value in (
            ("opportunity_ref", opportunity_ref),
            ("evaluation_ref", evaluation_ref),
        ):
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} reference must not be empty")
        if not isinstance(evaluated_at, datetime) or evaluated_at.tzinfo is None:
            raise ValueError("evaluated_at must be a timezone-aware datetime")

        evaluation = self._evaluator.evaluate(opportunity, evaluation_policy)
        if not isinstance(evaluation, OpportunityEvaluation):
            raise TypeError("evaluator must return an OpportunityEvaluation")
        if (
            evaluation.policy_id != evaluation_policy.policy_id
            or evaluation.policy_version != evaluation_policy.policy_version
        ):
            raise ValueError("evaluation policy identity/version does not match requested policy")

        decision = self._prioritizer.prioritize(
            opportunity_ref=opportunity_ref,
            evaluation_ref=evaluation_ref,
            evaluation=evaluation,
            policy=prioritization_policy,
            evaluated_at=evaluated_at,
        )
        if not isinstance(decision, OpportunityPriorityDecision):
            raise TypeError("prioritizer must return an OpportunityPriorityDecision")

        return OpportunityDecisionResult(
            opportunity_ref=opportunity_ref,
            evaluation_ref=evaluation_ref,
            evaluation=evaluation,
            priority_decision=decision,
        )
