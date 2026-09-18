import pytest

from app.domain.economic_profile import EconomicProfile


def make_profile(**overrides):
    values = {
        "profitability_score": 80,
        "profit_potential_score": 60,
        "profit_stability_score": 90,
        "demand_stability_score": 85,
        "safety_score": 88,
        "recurring_revenue_score": 75,
        "automation_score": 70,
        "capital_efficiency_score": 82,
        "scalability_score": 65,
        "evidence_quality_score": 95,
    }
    values.update(overrides)
    return EconomicProfile(**values)


def test_economic_profile_accepts_valid_bounded_scores():
    profile = make_profile()

    assert profile.profitability_score == 80
    assert profile.profit_stability_score == 90
    assert profile.safety_score == 88


@pytest.mark.parametrize(
    "field",
    [
        "profitability_score",
        "profit_potential_score",
        "profit_stability_score",
        "demand_stability_score",
        "safety_score",
        "recurring_revenue_score",
        "automation_score",
        "capital_efficiency_score",
        "scalability_score",
        "evidence_quality_score",
    ],
)
def test_scores_must_be_between_zero_and_one_hundred(field):
    with pytest.raises(ValueError):
        make_profile(**{field: -1})

    with pytest.raises(ValueError):
        make_profile(**{field: 101})


def test_scores_must_be_integers():
    with pytest.raises(TypeError):
        make_profile(profitability_score=80.5)


def test_profile_is_immutable():
    profile = make_profile()

    with pytest.raises(Exception):
        profile.profitability_score = 100
