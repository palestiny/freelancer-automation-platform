from app.domain.evaluation_context import (
    CriterionApplicability,
    EvaluationContext,
    EvidenceQuality,
)
from app.domain.opportunity import Opportunity
from app.domain.opportunity_intelligence import (
    CriterionEvaluation,
    CriterionId,
    CriterionOutcome,
    EvaluationPolicy,
)


class EligibilityEvaluator:
    """Deterministically evaluates explicit policy-defined eligibility constraints."""

    def evaluate(
        self,
        opportunity: Opportunity,
        policy: EvaluationPolicy,
        context: EvaluationContext,
    ) -> CriterionEvaluation:
        if context.subject != opportunity:
            raise ValueError("evaluation context subject does not match opportunity")
        if CriterionId.ELIGIBILITY not in policy.required_criteria:
            raise ValueError("eligibility policy must require the Eligibility criterion")

        applicability = context.applicability.get(CriterionId.ELIGIBILITY)
        if applicability is CriterionApplicability.NOT_APPLICABLE:
            return self._result(
                policy,
                CriterionOutcome.NOT_APPLICABLE,
            )

        if not policy.eligibility_constraints:
            return self._result(
                policy,
                CriterionOutcome.NOT_APPLICABLE,
            )

        evidence_by_id = {item.evidence_id: item for item in context.evidence}
        evidence_refs: list[str] = []
        missing_evidence: list[str] = []
        has_uncertainty = False
        has_violation = False

        for constraint in policy.eligibility_constraints:
            values: list[object] = []

            for evidence_id in constraint.evidence_refs:
                evidence = evidence_by_id.get(evidence_id)
                if evidence is None:
                    if evidence_id not in missing_evidence:
                        missing_evidence.append(evidence_id)
                    has_uncertainty = True
                    continue

                if evidence_id not in evidence_refs:
                    evidence_refs.append(evidence_id)

                if evidence.quality is EvidenceQuality.MISSING:
                    if evidence_id not in missing_evidence:
                        missing_evidence.append(evidence_id)
                    has_uncertainty = True
                    continue

                if evidence.quality is not EvidenceQuality.PRESENT_AND_USABLE:
                    has_uncertainty = True
                    continue

                values.append(evidence.value)

            if len(values) != len(constraint.evidence_refs):
                continue

            if any(not isinstance(value, str) for value in values):
                has_uncertainty = True
                continue

            normalized_values = set(values)
            if len(normalized_values) != 1:
                has_uncertainty = True
                continue

            if next(iter(normalized_values)) not in constraint.allowed_values:
                has_violation = True

        if has_violation:
            outcome = CriterionOutcome.FAIL
        elif has_uncertainty:
            outcome = CriterionOutcome.INSUFFICIENT_DATA
        else:
            outcome = CriterionOutcome.PASS

        uncertainty = ()
        if has_uncertainty and not missing_evidence:
            uncertainty = ("eligibility evidence is insufficient or contradictory",)

        return self._result(
            policy,
            outcome,
            evidence_refs=tuple(evidence_refs),
            missing_evidence=tuple(missing_evidence),
            uncertainty=uncertainty,
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
            criterion_id=CriterionId.ELIGIBILITY,
            outcome=outcome,
            evidence_refs=evidence_refs,
            missing_evidence=missing_evidence,
            uncertainty=uncertainty,
        )
