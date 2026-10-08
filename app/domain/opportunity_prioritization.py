from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from app.domain.opportunity_intelligence import OpportunityEvaluation, OverallOutcome


class PrioritizationOutcome(str, Enum):
    BLOCKED = "BLOCKED"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"
    PRIORITIZED = "PRIORITIZED"
    UNPRIORITIZED = "UNPRIORITIZED"


@dataclass(frozen=True)
class PriorityTierRule:
    rule_id: str
    tier_id: str
    required_evidence_refs: tuple[str, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.rule_id, str) or not self.rule_id.strip():
            raise ValueError("rule_id must not be empty")
        if not isinstance(self.tier_id, str) or not self.tier_id.strip():
            raise ValueError("tier_id must not be empty")
        if not isinstance(self.required_evidence_refs, tuple):
            raise TypeError("required_evidence_refs must be a tuple")
        if any(not isinstance(ref, str) or not ref.strip() for ref in self.required_evidence_refs):
            raise ValueError("required_evidence_refs must contain non-empty strings")
        if len(set(self.required_evidence_refs)) != len(self.required_evidence_refs):
            raise ValueError("required_evidence_refs must not contain duplicates")


@dataclass(frozen=True)
class PrioritizationPolicy:
    policy_id: str
    policy_version: str
    mandatory_evidence_refs: tuple[str, ...]
    tier_rules: tuple[PriorityTierRule, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.policy_id, str) or not self.policy_id.strip():
            raise ValueError("policy_id must not be empty")
        if not isinstance(self.policy_version, str) or not self.policy_version.strip():
            raise ValueError("policy_version must not be empty")
        if not isinstance(self.mandatory_evidence_refs, tuple):
            raise TypeError("mandatory_evidence_refs must be a tuple")
        if any(not isinstance(ref, str) or not ref.strip() for ref in self.mandatory_evidence_refs):
            raise ValueError("mandatory_evidence_refs must contain non-empty strings")
        if len(set(self.mandatory_evidence_refs)) != len(self.mandatory_evidence_refs):
            raise ValueError("mandatory_evidence_refs must not contain duplicates")
        if not self.tier_rules:
            raise ValueError("at least one tier rule is required")
        if any(not isinstance(rule, PriorityTierRule) for rule in self.tier_rules):
            raise TypeError("tier_rules must contain PriorityTierRule values")
        rule_ids = [rule.rule_id for rule in self.tier_rules]
        if len(set(rule_ids)) != len(rule_ids):
            raise ValueError("tier rule ids must be unique")
        tier_ids = [rule.tier_id for rule in self.tier_rules]
        if len(set(tier_ids)) != len(tier_ids):
            raise ValueError("each tier may be defined by only one rule in V1")
        signatures = [frozenset(rule.required_evidence_refs) for rule in self.tier_rules]
        if len(set(signatures)) != len(signatures):
            raise ValueError("tier rules must not have duplicate evidence conditions")
        for rule in self.tier_rules:
            if not set(self.mandatory_evidence_refs).issubset(rule.required_evidence_refs):
                raise ValueError("each tier rule must include all mandatory evidence refs")


@dataclass(frozen=True)
class OpportunityPriorityDecision:
    opportunity_ref: str
    evaluation_ref: str
    evaluation_policy_id: str
    evaluation_policy_version: str
    prioritization_policy_id: str
    prioritization_policy_version: str
    outcome: PrioritizationOutcome
    tier_id: str | None
    matched_rule_ids: tuple[str, ...]
    reasons: tuple[str, ...]
    evidence_refs: tuple[str, ...]
    evaluated_at: datetime

    def __post_init__(self) -> None:
        for name in (
            "opportunity_ref",
            "evaluation_ref",
            "evaluation_policy_id",
            "evaluation_policy_version",
            "prioritization_policy_id",
            "prioritization_policy_version",
        ):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} must not be empty")
        if not isinstance(self.outcome, PrioritizationOutcome):
            raise TypeError("outcome must be a PrioritizationOutcome")
        if (self.outcome is PrioritizationOutcome.PRIORITIZED) != (self.tier_id is not None):
            raise ValueError("only PRIORITIZED decisions may have a tier")
        if not isinstance(self.evaluated_at, datetime) or self.evaluated_at.tzinfo is None:
            raise ValueError("evaluated_at must be a timezone-aware datetime")
        for name, values in (
            ("matched_rule_ids", self.matched_rule_ids),
            ("reasons", self.reasons),
            ("evidence_refs", self.evidence_refs),
        ):
            if not isinstance(values, tuple):
                raise TypeError(f"{name} must be a tuple")
            if any(not isinstance(value, str) or not value.strip() for value in values):
                raise ValueError(f"{name} must contain non-empty strings")


def prioritize_opportunity(
    *,
    opportunity_ref: str,
    evaluation_ref: str,
    evaluation: OpportunityEvaluation,
    policy: PrioritizationPolicy,
    evaluated_at: datetime,
) -> OpportunityPriorityDecision:
    if not isinstance(evaluation, OpportunityEvaluation):
        raise TypeError("evaluation must be an OpportunityEvaluation")
    if not isinstance(policy, PrioritizationPolicy):
        raise TypeError("policy must be a PrioritizationPolicy")
    if not isinstance(evaluated_at, datetime) or evaluated_at.tzinfo is None:
        raise ValueError("evaluated_at must be a timezone-aware datetime")

    evidence_refs = tuple(sorted({ref for item in evaluation.criteria for ref in item.evidence_refs}))
    evidence_set = set(evidence_refs)

    common = dict(
        opportunity_ref=opportunity_ref,
        evaluation_ref=evaluation_ref,
        evaluation_policy_id=evaluation.policy_id,
        evaluation_policy_version=evaluation.policy_version,
        prioritization_policy_id=policy.policy_id,
        prioritization_policy_version=policy.policy_version,
        matched_rule_ids=(),
        evidence_refs=evidence_refs,
        evaluated_at=evaluated_at,
    )
    if evaluation.overall_outcome is OverallOutcome.NOT_QUALIFIED:
        return OpportunityPriorityDecision(
            **common, outcome=PrioritizationOutcome.BLOCKED, tier_id=None,
            reasons=("opportunity evaluation is NOT_QUALIFIED",),
        )
    if evaluation.overall_outcome is OverallOutcome.REVIEW_REQUIRED:
        return OpportunityPriorityDecision(
            **common, outcome=PrioritizationOutcome.REVIEW_REQUIRED, tier_id=None,
            reasons=("opportunity evaluation requires review",),
        )

    missing = tuple(sorted(set(policy.mandatory_evidence_refs) - evidence_set))
    if missing:
        return OpportunityPriorityDecision(
            **common, outcome=PrioritizationOutcome.REVIEW_REQUIRED, tier_id=None,
            reasons=tuple(f"mandatory evidence missing: {ref}" for ref in missing),
        )

    matches = tuple(rule for rule in policy.tier_rules if set(rule.required_evidence_refs).issubset(evidence_set))
    if len(matches) != 1:
        reason = "no tier rule matched" if not matches else "multiple tier rules matched"
        return OpportunityPriorityDecision(
            **common, outcome=PrioritizationOutcome.UNPRIORITIZED, tier_id=None,
            reasons=(reason,),
        )

    selected = matches[0]
    return OpportunityPriorityDecision(
        **{**common, "matched_rule_ids": (selected.rule_id,)},
        outcome=PrioritizationOutcome.PRIORITIZED,
        tier_id=selected.tier_id,
        reasons=(f"tier rule matched: {selected.rule_id}",),
    )
