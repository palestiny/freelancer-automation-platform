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


class RequirementFitEvaluator:
    """Deterministically evaluates explicit mandatory capability requirements."""

    def evaluate(
        self,
        opportunity: Opportunity,
        policy: EvaluationPolicy,
        context: EvaluationContext,
    ) -> CriterionEvaluation:
        if context.subject != opportunity:
            raise ValueError("evaluation context subject does not match opportunity")
        if CriterionId.REQUIREMENT_FIT not in policy.required_criteria:
            raise ValueError(
                "requirement fit policy must require the Requirement Fit criterion"
            )

        if (
            context.applicability.get(CriterionId.REQUIREMENT_FIT)
            is CriterionApplicability.NOT_APPLICABLE
        ):
            return self._result(policy, CriterionOutcome.NOT_APPLICABLE)

        requirements = policy.requirement_fit_requirements
        if not requirements:
            return self._result(policy, CriterionOutcome.NOT_APPLICABLE)

        evidence_by_id = {item.evidence_id: item for item in context.evidence}
        evidence_refs: list[str] = []
        missing_evidence: list[str] = []
        uncertainty: list[str] = []
        has_violation = False
        has_uncertainty = False

        for requirement in requirements:
            supported: list[object] = []
            incompatible: list[object] = []
            requirement_uncertain = False

            for evidence_id in requirement.evidence_refs:
                evidence = evidence_by_id.get(evidence_id)
                if evidence is None:
                    if evidence_id not in missing_evidence:
                        missing_evidence.append(evidence_id)
                    has_uncertainty = True
                    requirement_uncertain = True
                    continue

                if evidence_id not in evidence_refs:
                    evidence_refs.append(evidence_id)

                if evidence.quality is EvidenceQuality.MISSING:
                    if evidence_id not in missing_evidence:
                        missing_evidence.append(evidence_id)
                    has_uncertainty = True
                    requirement_uncertain = True
                    continue

                if evidence.quality is not EvidenceQuality.PRESENT_AND_USABLE:
                    has_uncertainty = True
                    requirement_uncertain = True
                    continue

                value = evidence.value
                if not isinstance(value, dict):
                    has_uncertainty = True
                    requirement_uncertain = True
                    continue

                capability_id = value.get("capability_id")
                compatibility = value.get("compatibility")

                if capability_id != requirement.capability_id:
                    has_uncertainty = True
                    requirement_uncertain = True
                    continue

                if compatibility == "INCOMPATIBLE":
                    incompatible.append(value)
                elif compatibility == "SUPPORTED":
                    supported.append(value)
                else:
                    has_uncertainty = True
                    requirement_uncertain = True

            if incompatible and supported:
                has_uncertainty = True
                requirement_uncertain = True
            elif incompatible:
                has_violation = True
            elif not supported:
                has_uncertainty = True
                requirement_uncertain = True

            if requirement_uncertain:
                uncertainty.append(
                    f"requirement {requirement.requirement_id} lacks decisive evidence"
                )

        if has_violation:
            outcome = CriterionOutcome.FAIL
        elif has_uncertainty:
            outcome = CriterionOutcome.INSUFFICIENT_DATA
        else:
            outcome = CriterionOutcome.PASS

        return self._result(
            policy,
            outcome,
            evidence_refs=tuple(evidence_refs),
            missing_evidence=tuple(missing_evidence),
            uncertainty=tuple(uncertainty),
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
            criterion_id=CriterionId.REQUIREMENT_FIT,
            outcome=outcome,
            evidence_refs=evidence_refs,
            missing_evidence=missing_evidence,
            uncertainty=uncertainty,
        )
