import pytest
from datetime import datetime, timezone

from app.application.economic_fit import EconomicFitEvaluator
from app.domain.economic_fit import EconomicConstraint
from app.domain.evaluation_context import (
    CriterionApplicability,
    EvaluationContext,
    Evidence,
    EvidenceKind,
    EvidenceQuality,
)
from app.domain.opportunity import Opportunity
from app.domain.opportunity_intelligence import (
    CriterionId,
    CriterionOutcome,
    EvaluationPolicy,
)


def make_opportunity() -> Opportunity:
    return Opportunity(
        source_platform="example_marketplace",
        source_opportunity_id="synthetic-economic-fit-001",
        title="Build a React dashboard",
        description="Implement a professional dashboard.",
    )


def make_context(*evidence: Evidence, applicable=True) -> EvaluationContext:
    return EvaluationContext(
        subject=make_opportunity(),
        evidence=evidence,
        evaluation_time=datetime(2026, 9, 28, 12, tzinfo=timezone.utc),
        applicability={
            CriterionId.ECONOMIC_FIT: (
                CriterionApplicability.APPLICABLE
                if applicable
                else CriterionApplicability.NOT_APPLICABLE
            )
        },
    )


def policy(*constraints: EconomicConstraint) -> EvaluationPolicy:
    return EvaluationPolicy(
        policy_id="economic-fit-v1",
        policy_version="1",
        required_criteria=(CriterionId.ECONOMIC_FIT,),
        economic_fit_constraints=constraints,
    )


def economic_evidence(
    evidence_id: str,
    metric: str,
    value: float,
    *,
    unit: str,
    currency: str | None = None,
    quality=EvidenceQuality.PRESENT_AND_USABLE,
    kind=EvidenceKind.ESTIMATE,
    uncertainty=(),
) -> Evidence:
    return Evidence(
        evidence_id=evidence_id,
        kind=kind,
        value={
            "metric": metric,
            "value": value,
            "unit": unit,
            "currency": currency,
        },
        provenance="synthetic:test",
        observed_at=datetime(2026, 9, 28, 11, tzinfo=timezone.utc),
        quality=quality,
        uncertainty=uncertainty,
    )


def constraint(
    metric: str = "expected_profit",
    *,
    operator="MINIMUM",
    threshold=100,
    unit="USD",
    currency="USD",
    evidence_refs=("economic.estimate",),
) -> EconomicConstraint:
    return EconomicConstraint(
        constraint_id=f"{metric}-constraint",
        metric=metric,
        operator=operator,
        threshold=threshold,
        unit=unit,
        currency=currency,
        evidence_refs=evidence_refs,
    )


@pytest.mark.parametrize(
    ("metric", "value", "unit", "currency"),
    [
        ("expected_profit", 150, "USD", "USD"),
        ("expected_margin", 0.25, "RATIO", None),
        ("expected_profit_per_hour", 50, "USD_PER_HOUR", "USD"),
        ("expected_cost", 100, "USD", "USD"),
        ("expected_revenue", 250, "USD", "USD"),
    ],
)
def test_each_v1_metric_can_be_evaluated_from_matching_evidence(
    metric, value, unit, currency
):
    context = make_context(
        economic_evidence(
            "economic.estimate",
            metric,
            value,
            unit=unit,
            currency=currency,
        )
    )
    threshold = value if metric != "expected_cost" else value
    operator = "MAXIMUM" if metric == "expected_cost" else "MINIMUM"

    result = EconomicFitEvaluator().evaluate(
        make_opportunity(),
        policy(
            EconomicConstraint(
                constraint_id=f"{metric}-constraint",
                metric=metric,
                operator=operator,
                threshold=threshold,
                unit=unit,
                currency=currency,
                evidence_refs=("economic.estimate",),
            )
        ),
        context,
    )

    assert result.outcome is CriterionOutcome.PASS
    assert result.evidence_refs == ("economic.estimate",)


def test_minimum_constraint_violation_returns_fail():
    context = make_context(
        economic_evidence(
            "economic.estimate",
            "expected_profit",
            75,
            unit="USD",
            currency="USD",
        )
    )

    result = EconomicFitEvaluator().evaluate(
        make_opportunity(),
        policy(constraint(threshold=100)),
        context,
    )

    assert result.outcome is CriterionOutcome.FAIL


def test_maximum_constraint_violation_returns_fail():
    context = make_context(
        economic_evidence(
            "economic.cost",
            "expected_cost",
            125,
            unit="USD",
            currency="USD",
        )
    )

    result = EconomicFitEvaluator().evaluate(
        make_opportunity(),
        policy(
            EconomicConstraint(
                constraint_id="max-cost",
                metric="expected_cost",
                operator="MAXIMUM",
                threshold=100,
                unit="USD",
                currency="USD",
                evidence_refs=("economic.cost",),
            )
        ),
        context,
    )

    assert result.outcome is CriterionOutcome.FAIL


@pytest.mark.parametrize(
    "quality",
    [
        EvidenceQuality.PRESENT_BUT_AMBIGUOUS,
        EvidenceQuality.PRESENT_BUT_STALE,
        EvidenceQuality.PRESENT_BUT_LOW_QUALITY,
        EvidenceQuality.MISSING,
    ],
)
def test_unusable_required_evidence_returns_insufficient_data(quality):
    context = make_context(
        economic_evidence(
            "economic.estimate",
            "expected_profit",
            150,
            unit="USD",
            currency="USD",
            quality=quality,
        )
    )

    result = EconomicFitEvaluator().evaluate(
        make_opportunity(),
        policy(),
        context,
    )

    assert result.outcome is CriterionOutcome.INSUFFICIENT_DATA


def test_missing_referenced_evidence_returns_insufficient_data():
    result = EconomicFitEvaluator().evaluate(
        make_opportunity(),
        policy(),
        make_context(),
    )

    assert result.outcome is CriterionOutcome.INSUFFICIENT_DATA
    assert result.missing_evidence == ("economic.estimate",)


def test_wrong_metric_identity_is_not_accepted():
    context = make_context(
        economic_evidence(
            "economic.estimate",
            "expected_revenue",
            150,
            unit="USD",
            currency="USD",
        )
    )

    result = EconomicFitEvaluator().evaluate(
        make_opportunity(),
        policy(),
        context,
    )

    assert result.outcome is CriterionOutcome.INSUFFICIENT_DATA


def test_unit_mismatch_is_not_silently_converted():
    context = make_context(
        economic_evidence(
            "economic.estimate",
            "expected_profit",
            150,
            unit="EUR",
            currency="EUR",
        )
    )

    result = EconomicFitEvaluator().evaluate(
        make_opportunity(),
        policy(),
        context,
    )

    assert result.outcome is CriterionOutcome.INSUFFICIENT_DATA


def test_currency_mismatch_is_not_silently_converted():
    context = make_context(
        economic_evidence(
            "economic.estimate",
            "expected_profit",
            150,
            unit="USD",
            currency="EUR",
        )
    )

    result = EconomicFitEvaluator().evaluate(
        make_opportunity(),
        policy(),
        context,
    )

    assert result.outcome is CriterionOutcome.INSUFFICIENT_DATA


def test_conflicting_usable_values_without_precedence_return_insufficient_data():
    context = make_context(
        economic_evidence(
            "economic-a",
            "expected_profit",
            150,
            unit="USD",
            currency="USD",
        ),
        economic_evidence(
            "economic-b",
            "expected_profit",
            75,
            unit="USD",
            currency="USD",
        ),
    )

    result = EconomicFitEvaluator().evaluate(
        make_opportunity(),
        policy(evidence_refs=("economic-a", "economic-b")),
        context,
    )

    assert result.outcome is CriterionOutcome.INSUFFICIENT_DATA
    assert result.evidence_refs == ("economic-a", "economic-b")


def test_violation_plus_unresolved_evidence_is_conservative():
    context = make_context(
        economic_evidence(
            "economic-a",
            "expected_profit",
            75,
            unit="USD",
            currency="USD",
        ),
        economic_evidence(
            "economic-b",
            "expected_profit",
            150,
            unit="USD",
            currency="USD",
            quality=EvidenceQuality.PRESENT_BUT_AMBIGUOUS,
        ),
    )

    result = EconomicFitEvaluator().evaluate(
        make_opportunity(),
        policy(evidence_refs=("economic-a", "economic-b")),
        context,
    )

    assert result.outcome is CriterionOutcome.INSUFFICIENT_DATA


def test_uncertainty_is_preserved_without_becoming_a_score():
    context = make_context(
        economic_evidence(
            "economic.estimate",
            "expected_profit",
            150,
            unit="USD",
            currency="USD",
            uncertainty=("forecast range is wide",),
        )
    )

    result = EconomicFitEvaluator().evaluate(
        make_opportunity(),
        policy(),
        context,
    )

    assert result.outcome is CriterionOutcome.PASS
    assert result.uncertainty == ("forecast range is wide",)
    assert not hasattr(result, "score")
    assert not hasattr(result, "confidence")


def test_not_applicable_requires_explicit_context():
    result = EconomicFitEvaluator().evaluate(
        make_opportunity(),
        policy(),
        make_context(applicable=False),
    )

    assert result.outcome is CriterionOutcome.NOT_APPLICABLE


def test_economic_fit_does_not_infer_from_opportunity_fields():
    context = EvaluationContext(
        subject=make_opportunity(),
        evidence=(),
        evaluation_time=datetime(2026, 9, 28, 12, tzinfo=timezone.utc),
    )

    result = EconomicFitEvaluator().evaluate(
        make_opportunity(),
        policy(),
        context,
    )

    assert result.outcome is CriterionOutcome.INSUFFICIENT_DATA


def test_policy_identity_and_evidence_provenance_are_preserved():
    evidence = economic_evidence(
        "economic.estimate",
        "expected_profit",
        150,
        unit="USD",
        currency="USD",
    )
    result = EconomicFitEvaluator().evaluate(
        make_opportunity(),
        policy(),
        make_context(evidence),
    )

    assert result.policy_id == "economic-fit-v1"
    assert result.policy_version == "1"
    assert result.evidence_refs == ("economic.estimate",)


def test_context_for_different_opportunity_is_rejected():
    context = make_context(
        economic_evidence(
            "economic.estimate",
            "expected_profit",
            150,
            unit="USD",
            currency="USD",
        )
    )
    other = Opportunity(
        source_platform="example_marketplace",
        source_opportunity_id="different",
        title="Different opportunity",
        description="Different description.",
    )

    with pytest.raises(ValueError, match="subject"):
        EconomicFitEvaluator().evaluate(
            other,
            policy(),
            context,
        )


def test_policy_rejects_duplicate_economic_constraint_ids():
    first = constraint(metric="expected_profit")
    second = EconomicConstraint(
        constraint_id=first.constraint_id,
        metric="expected_revenue",
        operator="MINIMUM",
        threshold=100,
        unit="USD",
        currency="USD",
        evidence_refs=("economic.revenue",),
    )

    with pytest.raises(ValueError, match="duplicate ids"):
        EvaluationPolicy(
            policy_id="economic-fit-v1",
            policy_version="1",
            required_criteria=(CriterionId.ECONOMIC_FIT,),
            economic_fit_constraints=(first, second),
        )


def test_constraint_rejects_duplicate_evidence_references():
    with pytest.raises(ValueError, match="duplicates"):
        EconomicConstraint(
            constraint_id="invalid",
            metric="expected_profit",
            operator="MINIMUM",
            threshold=100,
            unit="USD",
            currency="USD",
            evidence_refs=("economic.estimate", "economic.estimate"),
        )


def test_non_estimate_expected_economic_value_is_not_promoted_implicitly():
    context = make_context(
        economic_evidence(
            "economic.fact",
            "expected_profit",
            150,
            unit="USD",
            currency="USD",
            kind=EvidenceKind.FACT,
        )
    )

    result = EconomicFitEvaluator().evaluate(
        make_opportunity(),
        policy(evidence_refs=("economic.fact",)),
        context,
    )

    assert result.outcome is CriterionOutcome.INSUFFICIENT_DATA
