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
from app.domain.success_confidence import SuccessComparisonOperator


_ALLOWED_EVIDENCE_KINDS = {
    EvidenceKind.FACT,
    EvidenceKind.OBSERVATION,
    EvidenceKind.ESTIMATE,
    EvidenceKind.EXPERIMENT_RESULT,
}


class SuccessConfidenceEvaluator:
    """Deterministically evaluates explicit success conditions against policy."""

    def evaluate(
        self,
        opportunity: Opportunity,
        policy: EvaluationPolicy,
        context: EvaluationContext,
    ) -> CriterionEvaluation:
        if context.subject != opportunity:
            raise ValueError("evaluation context subject does not match opportunity")
        if CriterionId.SUCCESS_CONFIDENCE not in policy.required_criteria:
            raise ValueError(
                "success confidence policy must require the Success Confidence criterion"
            )

        if (
            context.applicability.get(CriterionId.SUCCESS_CONFIDENCE)
            is CriterionApplicability.NOT_APPLICABLE
        ):
            return self._result(policy, CriterionOutcome.NOT_APPLICABLE)

        conditions = policy.success_confidence_conditions
        if not conditions:
            return self._result(policy, CriterionOutcome.NOT_APPLICABLE)

        evidence_by_id = {item.evidence_id: item for item in context.evidence}
        evidence_refs: list[str] = []
        missing_evidence: list[str] = []
        uncertainty: list[str] = []
        has_violation = False
        has_uncertainty = False

        for success_condition in conditions:
            values: list[object] = []
            condition_uncertain = False

            for evidence_id in success_condition.evidence_refs:
                evidence = evidence_by_id.get(evidence_id)
                if evidence is None:
                    if evidence_id not in missing_evidence:
                        missing_evidence.append(evidence_id)
                    has_uncertainty = True
                    condition_uncertain = True
                    continue

                if evidence_id not in evidence_refs:
                    evidence_refs.append(evidence_id)

                if evidence.quality is EvidenceQuality.MISSING:
                    if evidence_id not in missing_evidence:
                        missing_evidence.append(evidence_id)
                    has_uncertainty = True
                    condition_uncertain = True
                    continue

                if evidence.quality is not EvidenceQuality.PRESENT_AND_USABLE:
                    has_uncertainty = True
                    condition_uncertain = True
                    continue

                if evidence.kind not in _ALLOWED_EVIDENCE_KINDS:
                    has_uncertainty = True
                    condition_uncertain = True
                    continue

                value = evidence.value
                if not isinstance(value, dict):
                    has_uncertainty = True
                    condition_uncertain = True
                    continue

                if (
                    value.get("scope") != success_condition.scope.value
                    or value.get("signal") != success_condition.signal
                ):
                    has_uncertainty = True
                    condition_uncertain = True
                    continue

                values.append(value.get("value"))
                if evidence.uncertainty:
                    uncertainty.extend(evidence.uncertainty)

            if success_condition.operator is not SuccessComparisonOperator.ALLOWED_VALUES:
                raise ValueError("unsupported success comparison operator")

            if len(set(values)) > 1:
                has_uncertainty = True
                condition_uncertain = True
            elif len(values) == 1:
                if values[0] not in success_condition.expected_values:
                    has_violation = True
            else:
                has_uncertainty = True
                condition_uncertain = True

            if condition_uncertain:
                uncertainty.append(
                    f"condition {success_condition.condition_id} lacks decisive evidence"
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
            criterion_id=CriterionId.SUCCESS_CONFIDENCE,
            outcome=outcome,
            evidence_refs=evidence_refs,
            missing_evidence=missing_evidence,
            uncertainty=uncertainty,
        )
