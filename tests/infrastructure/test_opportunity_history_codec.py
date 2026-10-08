from datetime import datetime, timezone
import json
from decimal import Decimal

import pytest

from app.domain.client_project_risk import (
    RiskComparisonOperator,
    RiskConstraint,
    RiskScope,
)
from app.domain.economic_fit import (
    EconomicComparisonOperator,
    EconomicConstraint,
    EconomicMetric,
)
from app.domain.eligibility import EligibilityConstraint
from app.domain.estimated_effort import EffortConstraint
from app.domain.opportunity import Opportunity
from app.domain.opportunity_intelligence import (
    CriterionEvaluation,
    CriterionId,
    CriterionOutcome,
    EvaluationPolicy,
    OpportunityEvaluation,
    OverallOutcome,
)
from app.domain.opportunity_prioritization import (
    OpportunityPriorityDecision,
    PrioritizationOutcome,
    PrioritizationPolicy,
    PriorityTierRule,
)
from app.domain.opportunity_type import OpportunityType
from app.domain.requirement_fit import CapabilityRequirement
from app.domain.success_confidence import (
    SuccessComparisonOperator,
    SuccessCondition,
    SuccessConditionScope,
)
from app.infrastructure.persistence.opportunity_history_codec import (
    OpportunityHistoryCodecV1,
    UnsupportedCanonicalValue,
)

UTC = timezone.utc
NOW = datetime(2026, 10, 9, 12, 30, tzinfo=UTC)


def sample_domain_values():
    opportunity = Opportunity(
        source_platform="synthetic",
        source_opportunity_id="job-17",
        title="Build a dashboard",
        description="Synthetic opportunity",
        required_capabilities=frozenset({"react", "python"}),
        budget_min=Decimal("100.00"),
        budget_max=Decimal("250.0"),
        budget_currency="USD",
        opportunity_type=OpportunityType.FREELANCE,
    )
    evaluation_policy = EvaluationPolicy(
        policy_id="evaluation-policy",
        policy_version="3",
        required_criteria=(CriterionId.ELIGIBILITY,),
        eligibility_constraints=(
            EligibilityConstraint(
                "eligible", ("eligibility.status",), ("eligible",)
            ),
        ),
        requirement_fit_requirements=(
            CapabilityRequirement("react", "react", ("requirements.react",)),
        ),
        estimated_effort_constraints=(
            EffortConstraint(
                "effort", 10.5, "hours", ("effort.estimate",), ("scope.deliverables",)
            ),
        ),
        economic_fit_constraints=(
            EconomicConstraint(
                "profit",
                EconomicMetric.EXPECTED_PROFIT,
                EconomicComparisonOperator.MINIMUM,
                100,
                "USD",
                "USD",
                ("economic.profit",),
            ),
        ),
        client_project_risk_constraints=(
            RiskConstraint(
                "risk",
                RiskScope.CLIENT,
                "client.verified",
                RiskComparisonOperator.ALLOWED_VALUES,
                ("true",),
                ("client.verified",),
            ),
        ),
        success_confidence_conditions=(
            SuccessCondition(
                "delivery",
                SuccessConditionScope.DELIVERY,
                "delivery.acceptance",
                SuccessComparisonOperator.ALLOWED_VALUES,
                ("accepted",),
                ("delivery.acceptance",),
            ),
        ),
    )
    prioritization_policy = PrioritizationPolicy(
        policy_id="priority-policy",
        policy_version="1",
        mandatory_evidence_refs=("eligibility.status",),
        tier_rules=(
            PriorityTierRule(
                rule_id="eligible",
                tier_id="P1",
                required_evidence_refs=("eligibility.status",),
            ),
        ),
    )
    evaluation = OpportunityEvaluation(
        policy_id="evaluation-policy",
        policy_version="3",
        criteria=(
            CriterionEvaluation(
                policy_id="evaluation-policy",
                policy_version="3",
                criterion_id=CriterionId.ELIGIBILITY,
                outcome=CriterionOutcome.PASS,
                evidence_refs=("eligibility.status",),
                missing_evidence=(),
                uncertainty=("client history unavailable",),
                rationale="Synthetic fixture",
            ),
        ),
        overall_outcome=OverallOutcome.QUALIFIED,
    )
    decision = OpportunityPriorityDecision(
        opportunity_ref="opp-17",
        evaluation_ref="eval-17",
        evaluation_policy_id="evaluation-policy",
        evaluation_policy_version="3",
        prioritization_policy_id="priority-policy",
        prioritization_policy_version="1",
        outcome=PrioritizationOutcome.PRIORITIZED,
        tier_id="P1",
        matched_rule_ids=("eligible",),
        reasons=("tier rule matched: eligible",),
        evidence_refs=("eligibility.status",),
        criterion_snapshots=(),
        evaluated_at=NOW,
    )
    return opportunity, evaluation_policy, prioritization_policy, evaluation, decision


def test_mapping_key_order_and_json_formatting_do_not_change_canonical_bytes():
    codec = OpportunityHistoryCodecV1()

    left = codec.dumps({"z": [1, "x"], "a": {"second": True, "first": None}})
    right = codec.dumps({"a": {"first": None, "second": True}, "z": [1, "x"]})

    assert left == right
    assert b": " not in left
    assert b", " not in left


def test_whitespace_inside_string_values_remains_significant():
    codec = OpportunityHistoryCodecV1()

    assert codec.dumps({"title": "build dashboard"}) != codec.dumps(
        {"title": " build dashboard "}
    )


def test_tuple_order_is_significant_but_frozenset_order_is_not():
    codec = OpportunityHistoryCodecV1()

    assert codec.dumps(("first", "second")) != codec.dumps(("second", "first"))
    assert codec.dumps(frozenset({"first", "second"})) == codec.dumps(
        frozenset({"second", "first"})
    )


def test_decimal_normalization_and_signed_zero_are_deterministic():
    codec = OpportunityHistoryCodecV1()

    assert codec.dumps(Decimal("1.2300")) == codec.dumps(Decimal("1.23"))
    assert codec.dumps(Decimal("-0.000")) == codec.dumps(Decimal("0"))
    very_precise = Decimal("123456789012345678901234567890.123450000")
    assert codec.dumps(very_precise) == codec.dumps(
        Decimal("123456789012345678901234567890.12345")
    )


def test_finite_float_encoding_is_exact_and_non_finite_values_fail_closed():
    codec = OpportunityHistoryCodecV1()

    assert codec.dumps(1) != codec.dumps(1.0)
    assert codec.dumps(0.1) != codec.dumps(0.10000000000000002)
    for value in (float("nan"), float("inf"), float("-inf")):
        with pytest.raises(UnsupportedCanonicalValue):
            codec.dumps(value)


def test_aware_datetimes_compare_by_utc_instant_and_naive_values_are_rejected():
    codec = OpportunityHistoryCodecV1()
    same_instant = datetime.fromisoformat("2026-10-09T15:30:00+03:00")

    assert codec.dumps(NOW) == codec.dumps(same_instant)
    with pytest.raises(UnsupportedCanonicalValue):
        codec.dumps(datetime(2026, 10, 9, 12, 30))


def test_domain_types_round_trip_through_explicit_versioned_serializers():
    codec = OpportunityHistoryCodecV1()
    opportunity, evaluation_policy, prioritization_policy, evaluation, decision = (
        sample_domain_values()
    )

    for value in (
        opportunity,
        evaluation_policy,
        prioritization_policy,
        evaluation,
        decision,
    ):
        encoded = codec.dumps(value)
        restored = codec.loads(encoded, expected_type=type(value))
        assert restored == value


def test_unknown_domain_types_and_unsupported_any_values_fail_closed():
    codec = OpportunityHistoryCodecV1()

    class UnregisteredDomainValue:
        pass

    with pytest.raises(UnsupportedCanonicalValue):
        codec.dumps(UnregisteredDomainValue())
    with pytest.raises(UnsupportedCanonicalValue):
        codec.dumps({"runtime_object": object()})


def test_schema_version_mismatch_is_not_silently_coerced():
    codec = OpportunityHistoryCodecV1()
    opportunity, *_ = sample_domain_values()
    encoded = codec.dumps(opportunity)
    envelope = json.loads(encoded)
    envelope["schema_version"] = 999

    with pytest.raises(UnsupportedCanonicalValue):
        codec.loads(json.dumps(envelope), expected_type=Opportunity)
    with pytest.raises(UnsupportedCanonicalValue):
        codec.loads(encoded, expected_type=Opportunity, schema_version=999)


def test_typed_envelopes_reject_unexpected_fields():
    codec = OpportunityHistoryCodecV1()
    envelope = json.loads(codec.dumps("value"))
    envelope["unexpected"] = "must fail closed"

    with pytest.raises(UnsupportedCanonicalValue):
        codec.loads(json.dumps(envelope))
