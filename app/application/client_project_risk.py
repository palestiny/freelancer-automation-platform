from app.domain.client_project_risk import RiskComparisonOperator
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


_ALLOWED_EVIDENCE_KINDS = {
    EvidenceKind.FACT,
    EvidenceKind.OBSERVATION,
    EvidenceKind.ESTIMATE,
    EvidenceKind.EXPERIMENT_RESULT,
}


class ClientProjectRiskEvaluator:
    """Deterministically evaluates explicit client/project risk constraints."""

    def evaluate(
        self,
        opportunity: Opportunity,
        policy: EvaluationPolicy,
        context: EvaluationContext,
    ) -> CriterionEvaluation:
        if context.subject != opportunity:
            raise ValueError("evaluation context subject does not match opportunity")
        if CriterionId.CLIENT_PROJECT_RISK not in policy.required_criteria:
            raise ValueError(
                "client/project risk policy must require the Client / Project Risk criterion"
            )

        if (
            context.applicability.get(CriterionId.CLIENT_PROJECT_RISK)
            is CriterionApplicability.NOT_APPLICABLE
        ):
            return self._result(policy, CriterionOutcome.NOT_APPLICABLE)

        constraints = policy.client_project_risk_constraints
        if not constraints:
            return self._result(policy, CriterionOutcome.NOT_APPLICABLE)

        evidence_by_id = {item.evidence_id: item for item in context.evidence}
        evidence_refs: list[str] = []
        missing_evidence: list[str] = []
        uncertainty: list[str] = []
        has_violation = False
        has_uncertainty = False

        for risk_constraint in constraints:
            values: list[object] = []
            constraint_uncertain = False

            for evidence_id in risk_constraint.evidence_refs:
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

                if evidence.kind not in _ALLOWED_EVIDENCE_KINDS:
                    has_uncertainty = True
                    constraint_uncertain = True
                    continue

                value = evidence.value
                if not isinstance(value, dict):
                    has_uncertainty = True
                    constraint_uncertain = True
                    continue

                if (
                    value.get("scope") != risk_constraint.scope.value
                    or value.get("signal") != risk_constraint.signal
                ):
                    has_uncertainty = True
                    constraint_uncertain = True
                    continue

                values.append(value.get("value"))
                if evidence.uncertainty:
                    uncertainty.extend(evidence.uncertainty)

            if risk_constraint.operator is not RiskComparisonOperator.ALLOWED_VALUES:
                raise ValueError("unsupported risk comparison operator")

            if len(set(values)) > 1:
                has_uncertainty = True
                constraint_uncertain = True
            elif len(values) == 1:
                if values[0] not in risk_constraint.expected_values:
                    has_violation = True
            else:
                has_uncertainty = True
                constraint_uncertain = True

            if constraint_uncertain:
                uncertainty.append(
                    f"constraint {risk_constraint.constraint_id} lacks decisive evidence"
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
            criterion_id=CriterionId.CLIENT_PROJECT_RISK,
            outcome=outcome,
            evidence_refs=evidence_refs,
            missing_evidence=missing_evidence,
            uncertainty=uncertainty,
        )
