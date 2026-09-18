from dataclasses import dataclass
from enum import Enum

from app.domain.opportunity import Opportunity


class CriterionOutcome(Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    INSUFFICIENT_DATA = "INSUFFICIENT_DATA"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class OverallOutcome(Enum):
    QUALIFIED = "QUALIFIED"
    NOT_QUALIFIED = "NOT_QUALIFIED"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"


@dataclass(frozen=True)
class EvaluationPolicy:
    allowed_project_types: frozenset[str] = frozenset()
    required_capabilities: frozenset[str] = frozenset()
    minimum_budget: float | None = None
    maximum_budget: float | None = None


@dataclass(frozen=True)
class CriterionEvaluation:
    outcome: CriterionOutcome
    evidence: tuple[str, ...] = ()


@dataclass(frozen=True)
class OpportunityEvaluation:
    overall_outcome: OverallOutcome
    criteria: dict[str, CriterionEvaluation]


class OpportunityEvaluator:
    def evaluate(
        self,
        opportunity: Opportunity,
        policy: EvaluationPolicy,
    ) -> OpportunityEvaluation:
        eligibility = self._evaluate_eligibility(opportunity, policy)

        overall = (
            OverallOutcome.QUALIFIED
            if eligibility.outcome is CriterionOutcome.PASS
            else OverallOutcome.NOT_QUALIFIED
        )

        return OpportunityEvaluation(
            overall_outcome=overall,
            criteria={"eligibility": eligibility},
        )

    def _evaluate_eligibility(
        self,
        opportunity: Opportunity,
        policy: EvaluationPolicy,
    ) -> CriterionEvaluation:
        evidence: list[str] = []

        if policy.allowed_project_types:
            if opportunity.project_type is None:
                return CriterionEvaluation(
                    CriterionOutcome.INSUFFICIENT_DATA,
                    ("project_type is missing",),
                )

            if opportunity.project_type not in policy.allowed_project_types:
                return CriterionEvaluation(
                    CriterionOutcome.FAIL,
                    ("project_type is not allowed by policy",),
                )

            evidence.append("project_type satisfies policy")

        if policy.required_capabilities:
            missing = policy.required_capabilities - opportunity.required_capabilities
            if missing:
                return CriterionEvaluation(
                    CriterionOutcome.FAIL,
                    (f"missing required capabilities: {sorted(missing)}",),
                )

            evidence.append("required capabilities satisfy policy")

        if policy.minimum_budget is not None:
            if opportunity.budget_max is None:
                return CriterionEvaluation(
                    CriterionOutcome.INSUFFICIENT_DATA,
                    ("budget_max is missing",),
                )

            if opportunity.budget_max < policy.minimum_budget:
                return CriterionEvaluation(
                    CriterionOutcome.FAIL,
                    ("opportunity budget is below policy minimum",),
                )

            evidence.append("budget satisfies minimum")

        if policy.maximum_budget is not None:
            if opportunity.budget_min is None:
                return CriterionEvaluation(
                    CriterionOutcome.INSUFFICIENT_DATA,
                    ("budget_min is missing",),
                )

            if opportunity.budget_min > policy.maximum_budget:
                return CriterionEvaluation(
                    CriterionOutcome.FAIL,
                    ("opportunity budget is above policy maximum",),
                )

            evidence.append("budget satisfies maximum")

        return CriterionEvaluation(CriterionOutcome.PASS, tuple(evidence))
