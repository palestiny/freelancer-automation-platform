from datetime import datetime, timezone

import pytest

from app.application.opportunity_prioritizer import OpportunityPrioritizer
from app.domain.opportunity_intelligence import (
    CriterionEvaluation,
    CriterionId,
    CriterionOutcome,
    OpportunityEvaluation,
    OverallOutcome,
)
from app.domain.opportunity_prioritization import (
    OpportunityPriorityDecision,
    PrioritizationOutcome,
    PrioritizationPolicy,
    PriorityTierRule,
)


NOW = datetime(2026, 10, 9, 0, 0, tzinfo=timezone.utc)


def evaluation(outcome=OverallOutcome.QUALIFIED, evidence=("eligibility.status", "economic.profit")):
    return OpportunityEvaluation(
        policy_id="evaluation-policy",
        policy_version="3",
        criteria=(
            CriterionEvaluation(
                policy_id="evaluation-policy",
                policy_version="3",
                criterion_id=CriterionId.ELIGIBILITY,
                outcome=CriterionOutcome.PASS,
                evidence_refs=tuple(evidence),
            ),
        ),
        overall_outcome=outcome,
    )


def policy(*rules, mandatory=("eligibility.status",)):
    return PrioritizationPolicy(
        policy_id="priority-policy",
        policy_version="1",
        mandatory_evidence_refs=mandatory,
        tier_rules=tuple(rules),
    )


def rule(rule_id="profit-evidence", tier="P1", evidence=("eligibility.status", "economic.profit")):
    return PriorityTierRule(rule_id, tier, tuple(evidence))


def decide(evaluation_value=None, policy_value=None):
    return OpportunityPrioritizer().prioritize(
        opportunity_ref="example_marketplace:job-17",
        evaluation_ref="evaluation:job-17:3",
        evaluation=evaluation_value or evaluation(),
        policy=policy_value or policy(rule()),
        evaluated_at=NOW,
    )


def test_qualified_evaluation_with_one_matching_rule_is_prioritized_and_traced():
    result = decide()
    assert result.outcome is PrioritizationOutcome.PRIORITIZED
    assert result.tier_id == "P1"
    assert result.matched_rule_ids == ("profit-evidence",)
    assert result.evaluation_ref == "evaluation:job-17:3"
    assert result.evaluation_policy_version == "3"
    assert result.prioritization_policy_version == "1"
    assert result.evidence_refs == ("economic.profit", "eligibility.status")


def test_not_qualified_evaluation_is_blocked():
    result = decide(evaluation_value=evaluation(OverallOutcome.NOT_QUALIFIED))
    assert result.outcome is PrioritizationOutcome.BLOCKED
    assert result.tier_id is None


def test_review_required_evaluation_never_gets_tier():
    result = decide(evaluation_value=evaluation(OverallOutcome.REVIEW_REQUIRED))
    assert result.outcome is PrioritizationOutcome.REVIEW_REQUIRED
    assert result.tier_id is None


def test_missing_mandatory_evidence_requires_review():
    result = decide(
        evaluation_value=evaluation(evidence=("eligibility.status",)),
        policy_value=policy(rule(evidence=("eligibility.status",)), mandatory=("eligibility.status", "economic.profit")),
    )
    assert result.outcome is PrioritizationOutcome.REVIEW_REQUIRED
    assert result.tier_id is None


def test_qualified_evaluation_without_matching_rule_is_unprioritized():
    result = decide(
        evaluation_value=evaluation(evidence=("eligibility.status",)),
        policy_value=policy(rule(evidence=("eligibility.status", "economic.profit"))),
    )
    assert result.outcome is PrioritizationOutcome.UNPRIORITIZED
    assert result.tier_id is None


def test_overlapping_tier_rules_are_not_selected_arbitrarily():
    selected_policy = policy(
        rule("evidence-only", "P1", ("eligibility.status",)),
        rule("evidence-plus-profit", "P2", ("eligibility.status", "economic.profit")),
    )
    result = decide(policy_value=selected_policy)
    assert result.outcome is PrioritizationOutcome.UNPRIORITIZED
    assert result.tier_id is None
    assert result.reasons == ("multiple tier rules matched",)


def test_duplicate_evidence_conditions_are_rejected_at_policy_construction():
    with pytest.raises(ValueError, match="duplicate evidence conditions"):
        policy(
            rule("one", "P1", ("eligibility.status",)),
            rule("two", "P2", ("eligibility.status",)),
        )


def test_policy_requires_mandatory_evidence_in_each_rule():
    with pytest.raises(ValueError, match="include all mandatory evidence"):
        policy(rule(evidence=("economic.profit",)), mandatory=("eligibility.status",))


def test_decision_requires_timezone_aware_timestamp():
    with pytest.raises(ValueError, match="timezone-aware"):
        OpportunityPriorityDecision(
            opportunity_ref="market:1",
            evaluation_ref="evaluation:1",
            evaluation_policy_id="eval",
            evaluation_policy_version="1",
            prioritization_policy_id="priority",
            prioritization_policy_version="1",
            outcome=PrioritizationOutcome.UNPRIORITIZED,
            tier_id=None,
            matched_rule_ids=(),
            reasons=("no tier rule matched",),
            evidence_refs=(),
            evaluated_at=datetime(2026, 10, 9),
        )


def test_same_semantic_inputs_produce_same_decision():
    assert decide() == decide()
