from collections.abc import Callable, Mapping

from app.domain.opportunity import Opportunity
from app.domain.opportunity_intelligence import (
    CriterionEvaluation,
    CriterionId,
    EvaluationPolicy,
    OpportunityEvaluation,
    compose_overall_outcome,
)

CriterionEvaluator = Callable[
    [Opportunity, EvaluationPolicy],
    CriterionEvaluation,
]


class OpportunityIntelligenceEvaluator:
    def __init__(
        self,
        evaluators: Mapping[CriterionId, CriterionEvaluator],
    ) -> None:
        self._evaluators = dict(evaluators)

    def evaluate(
        self,
        opportunity: Opportunity,
        policy: EvaluationPolicy,
    ) -> OpportunityEvaluation:
        results = []

        for criterion_id in policy.required_criteria:
            evaluator = self._evaluators.get(criterion_id)
            if evaluator is None:
                raise ValueError(
                    f"no evaluator registered for criterion {criterion_id.value}"
                )

            result = evaluator(opportunity, policy)
            self._validate_result(result, policy, criterion_id)
            results.append(result)

        criteria = tuple(results)
        return OpportunityEvaluation(
            policy_id=policy.policy_id,
            policy_version=policy.policy_version,
            criteria=criteria,
            overall_outcome=compose_overall_outcome(criteria),
        )

    @staticmethod
    def _validate_result(
        result: CriterionEvaluation,
        policy: EvaluationPolicy,
        criterion_id: CriterionId,
    ) -> None:
        if not isinstance(result, CriterionEvaluation):
            raise TypeError("criterion evaluator must return CriterionEvaluation")
        if result.policy_id != policy.policy_id:
            raise ValueError("criterion result policy identity does not match policy")
        if result.policy_version != policy.policy_version:
            raise ValueError("criterion result policy version does not match policy")
        if result.criterion_id is not criterion_id:
            raise ValueError("criterion result identity does not match requested criterion")
