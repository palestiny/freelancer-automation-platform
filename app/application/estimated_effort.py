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


class EstimatedEffortEvaluator:
    """Deterministically evaluates explicit effort evidence against policy constraints."""

    def evaluate(
        self,
        opportunity: Opportunity,
        policy: EvaluationPolicy,
        context: EvaluationContext,
    ) -> CriterionEvaluation:
        if context.subject != opportunity:
            raise ValueError("evaluation context subject does not match opportunity")
        if CriterionId.ESTIMATED_EFFORT not in policy.required_criteria:
            raise ValueError(
                "estimated effort policy must require the Estimated Effort criterion"
            )
        if (
            context.applicability.get(CriterionId.ESTIMATED_EFFORT)
            is CriterionApplicability.NOT_APPLICABLE
        ):
            return self._result(policy, CriterionOutcome.NOT_APPLICABLE)
        constraints = policy.estimated_effort_constraints
        if not constraints:
            return self._result(policy, CriterionOutcome.NOT_APPLICABLE)

        evidence_by_id = {item.evidence_id: item for item in context.evidence}
        evidence_refs: list[str] = []
        missing_evidence: list[str] = []
        uncertainty: list[str] = []
        has_violation = False
        has_uncertainty = False

        for effort_constraint in constraints:
            estimates = []
            constraint_uncertain = False

            for evidence_id in effort_constraint.evidence_refs:
                evidence = evidence_by_id.get(evidence_id)
                if evidence is None:
                    missing_evidence.append(evidence_id)
                    has_uncertainty = True
                    constraint_uncertain = True
                    continue

                if evidence_id not in evidence_refs:
                    evidence_refs.append(evidence_id)

                if evidence.quality is EvidenceQuality.MISSING:
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

                estimate_value = value.get("value")
                estimate_unit = value.get("unit")
                scope_refs = value.get("scope_refs")

                if (
                    isinstance(estimate_value, bool)
                    or not isinstance(estimate_value, (int, float))
                    or estimate_value < 0
                    or not isinstance(estimate_unit, str)
                    or not estimate_unit.strip()
                    or not isinstance(scope_refs, (tuple, list))
                    or any(not isinstance(ref, str) or not ref.strip() for ref in scope_refs)
                ):
                    has_uncertainty = True
                    constraint_uncertain = True
                    continue

                if estimate_unit != effort_constraint.unit:
                    has_uncertainty = True
                    constraint_uncertain = True
                    continue

                if not set(effort_constraint.required_scope_refs).issubset(scope_refs):
                    has_uncertainty = True
                    constraint_uncertain = True
                    continue

                if evidence.uncertainty:
                    uncertainty.extend(evidence.uncertainty)

                estimates.append((estimate_value, tuple(scope_refs)))

            if len({item[0] for item in estimates}) > 1:
                has_uncertainty = True
                constraint_uncertain = True
            elif estimates:
                estimate_value = estimates[0][0]
                if estimate_value > effort_constraint.maximum_value:
                    has_violation = True
            else:
                has_uncertainty = True
                constraint_uncertain = True

            if constraint_uncertain:
                uncertainty.append(
                    f"constraint {effort_constraint.constraint_id} lacks decisive evidence"
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
            criterion_id=CriterionId.ESTIMATED_EFFORT,
            outcome=outcome,
            evidence_refs=evidence_refs,
            missing_evidence=missing_evidence,
            uncertainty=uncertainty,
        )
