import pytest

from app.domain.business_economics import EconomicEstimate


def test_expected_cost_is_sum_of_explicit_cost_components():
    estimate = EconomicEstimate(
        expected_revenue=500,
        expected_effort_hours=10,
        platform_fee=50,
        capability_cost=20,
        operating_cost=10,
        revision_allowance=20,
    )

    assert estimate.expected_cost == 100


def test_expected_profit_is_revenue_minus_expected_cost():
    estimate = EconomicEstimate(
        expected_revenue=500,
        expected_effort_hours=10,
        platform_fee=50,
        capability_cost=20,
        operating_cost=10,
        revision_allowance=20,
    )

    assert estimate.expected_profit == 400


def test_expected_margin_is_profit_divided_by_revenue():
    estimate = EconomicEstimate(
        expected_revenue=500,
        expected_effort_hours=10,
        platform_fee=50,
        capability_cost=20,
        operating_cost=10,
        revision_allowance=20,
    )

    assert estimate.expected_margin == pytest.approx(0.8)


def test_expected_profit_per_hour_uses_expected_effort():
    estimate = EconomicEstimate(
        expected_revenue=500,
        expected_effort_hours=10,
        platform_fee=50,
    )

    assert estimate.expected_profit_per_hour == 45


def test_risk_adjusted_profit_uses_explicit_success_confidence():
    estimate = EconomicEstimate(
        expected_revenue=500,
        expected_effort_hours=10,
        platform_fee=100,
        success_confidence=0.5,
    )

    assert estimate.expected_profit == 400
    assert estimate.risk_adjusted_profit == 200


@pytest.mark.parametrize(
    "field,value",
    [
        ("expected_revenue", -1),
        ("expected_effort_hours", 0),
        ("platform_fee", -1),
        ("capability_cost", -1),
        ("operating_cost", -1),
        ("revision_allowance", -1),
    ],
)
def test_negative_or_invalid_economic_inputs_are_rejected(field, value):
    values = {
        "expected_revenue": 500,
        "expected_effort_hours": 10,
        "platform_fee": 0,
        "capability_cost": 0,
        "operating_cost": 0,
        "revision_allowance": 0,
        "success_confidence": 1,
    }
    values[field] = value

    with pytest.raises(ValueError):
        EconomicEstimate(**values)


def test_success_confidence_must_be_between_zero_and_one():
    with pytest.raises(ValueError):
        EconomicEstimate(
            expected_revenue=500,
            expected_effort_hours=10,
            success_confidence=1.1,
        )


def test_zero_revenue_has_no_defined_margin():
    estimate = EconomicEstimate(
        expected_revenue=0,
        expected_effort_hours=10,
    )

    assert estimate.expected_margin is None

@pytest.mark.parametrize("field", [
    "expected_revenue",
    "expected_effort_hours",
    "platform_fee",
    "capability_cost",
    "operating_cost",
    "revision_allowance",
    "success_confidence",
])
def test_non_finite_estimate_values_are_rejected(field):
    kwargs = dict(
        expected_revenue=100.0,
        expected_effort_hours=2.0,
        platform_fee=1.0,
        capability_cost=1.0,
        operating_cost=1.0,
        revision_allowance=1.0,
        success_confidence=0.8,
    )
    kwargs[field] = float("nan")
    with pytest.raises(ValueError, match="finite"):
        EconomicEstimate(**kwargs)
