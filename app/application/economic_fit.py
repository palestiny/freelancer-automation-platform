from math import isfinite

from app.domain.economic_fit import (
    EconomicComparisonOperator,
    EconomicMetric,
)
from app.domain.evaluation_context import (
    CriterionApplicability,
    EvaluationContext,
    EvidenceKind,
    EvidenceQuality,
)
from app.domain.opportunity import Opportunity
from app.domain.opportunity_intelligence import (
    CriterionEvaluation,
    CriterionId,
    CriterionOutcome,
    EvaluationPolicy,
)


class EconomicFitEvaluator:
    """Deterministically evaluates explicit economic evidence against policy."""

    def evaluate(
        self,
        opportunity: Opportunity,
        policy: EvaluationPolicy,
        context: EvaluationContext,
    ) -> CriterionEvaluation:
        if context.subject != opportunity:
            raise ValueError("evaluation context subject does not match opportunity")
        if CriterionId.ECONOMIC_FIT not in policy.required_criteria:
            raise ValueError(
                "economic fit policy must require the Economic Fit criterion"
            )

        if (
            context.applicability.get(CriterionId.ECONOMIC_FIT)
            is CriterionApplicability.NOT_APPLICABLE
        ):
            return self._result(policy, CriterionOutcome.NOT_APPLICABLE)

        constraints = policy.economic_fit_constraints
        if not constraints:
            return self._result(policy, CriterionOutcome.NOT_APPLICABLE)

        evidence_by_id = {item.evidence_id: item for item in context.evidence}
        evidence_refs: list[str] = []
        missing_evidence: list[str] = []
        uncertainty: list[str] = []
        has_violation = False
        has_uncertainty = False

        for economic_constraint in constraints:
            values: list[float] = []
            constraint_uncertain = False

            for evidence_id in economic_constraint.evidence_refs:
                evidence = evidence_by_id.get(evidence_id)
                if evidence is None:
                    if evidence_id not in missing_evidence:
                        missing_evidence.append(evidence_id)
                    has_uncertainty = True
                    constraint_uncertain = True
                    continue

                if evidence_id not in evidence_refs:
                    evidence_refs.append(evidence_id)

                if evidence.quality is EvidenceQuality.MISSING:
                    if evidence_id not in missing_evidence:
                        missing_evidence.append(evidence_id)
                    has_uncertainty = True
                    constraint_uncertain = True
                    continue

                if evidence.quality is not EvidenceQuality.PRESENT_AND_USABLE:
                    has_uncertainty = True
                    constraint_uncertain = True
                    continue

                if evidence.kind is not EvidenceKind.ESTIMATE:
                    has_uncertainty = True
                    constraint_uncertain = True
                    continue

                value = evidence.value
                if not isinstance(value, dict):
                    has_uncertainty = True
                    constraint_uncertain = True
                    continue

                metric = value.get("metric")
                numeric_value = value.get("value")
                unit = value.get("unit")
                currency = value.get("currency")

                if metric != economic_constraint.metric.value:
                    has_uncertainty = True
                    constraint_uncertain = True
                    continue

                if (
                    isinstance(numeric_value, bool)
                    or not isinstance(numeric_value, (int, float))
                    or not isfinite(float(numeric_value))
                ):
                    has_uncertainty = True
                    constraint_uncertain = True
                    continue

                if unit != economic_constraint.unit:
                    has_uncertainty = True
                    constraint_uncertain = True
                    continue

                if currency != economic_constraint.currency:
                    has_uncertainty = True
                    constraint_uncertain = True
                    continue

                values.append(float(numeric_value))
                if evidence.uncertainty:
                    uncertainty.extend(evidence.uncertainty)

            if len(set(values)) > 1:
                has_uncertainty = True
                constraint_uncertain = True
            elif len(values) == 1:
                measured_value = values[0]
                if (
                    economic_constraint.operator
                    is EconomicComparisonOperator.MINIMUM
                    and measured_value < economic_constraint.threshold
                ):
                    has_violation = True
                elif (
                    economic_constraint.operator
                    is EconomicComparisonOperator.MAXIMUM
                    and measured_value > economic_constraint.threshold
                ):
                    has_violation = True
            else:
                has_uncertainty = True
                constraint_uncertain = True

            if constraint_uncertain:
                uncertainty.append(
                    f"constraint {economic_constraint.constraint_id} lacks decisive evidence"
                )

        if has_violation and has_uncertainty:
            outcome = CriterionOutcome.INSUFFICIENT_DATA
        elif has_violation:
            outcome = CriterionOutcome.FAIL
        elif has_uncertainty:
            outcome = CriterionOutcome.INSUFFICIENT_DATA
        else:
            outcome = CriterionOutcome.PASS

        return self._result(
            policy,
            outcome,
            evidence_refs=tuple(evidence_refs),
            missing_evidence=tuple(dict.fromkeys(missing_evidence)),
            uncertainty=tuple(dict.fromkeys(uncertainty)),
        )

    @staticmethod
    def _result(
        policy: EvaluationPolicy,
        outcome: CriterionOutcome,
        *,
        evidence_refs: tuple[str, ...] = (),
        missing_evidence: tuple[str, ...] = (),
        uncertainty: tuple[str, ...] = (),
    ) -> CriterionEvaluation:
        return CriterionEvaluation(
            policy_id=policy.policy_id,
            policy_version=policy.policy_version,
            criterion_id=CriterionId.ECONOMIC_FIT,
            outcome=outcome,
            evidence_refs=evidence_refs,
            missing_evidence=missing_evidence,
            uncertainty=uncertainty,
        )
