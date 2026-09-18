from datetime import datetime, timezone

import pytest

from app.domain.market_intelligence import DemandSignal, MarketObservation


def make_observation(**overrides):
    values = {
        "topic": "automated bookkeeping",
        "observed_value": "multiple customers requested recurring bookkeeping",
        "source": "customer_interviews",
        "observed_at": datetime.now(timezone.utc),
        "evidence_quality": 80,
    }
    values.update(overrides)
    return MarketObservation(**values)


def test_market_observation_preserves_provenance_and_quality():
    observation = make_observation()

    assert observation.source == "customer_interviews"
    assert observation.evidence_quality == 80


@pytest.mark.parametrize("field", ["topic", "observed_value", "source"])
def test_market_observation_requires_non_empty_fields(field):
    with pytest.raises(ValueError):
        make_observation(**{field: "   "})


@pytest.mark.parametrize("value", [-1, 101])
def test_market_observation_rejects_invalid_evidence_quality(value):
    with pytest.raises(ValueError):
        make_observation(evidence_quality=value)


def test_demand_signal_requires_supporting_observations():
    with pytest.raises(ValueError):
        DemandSignal(
            topic="automated bookkeeping",
            demand_strength=80,
            evidence_quality=75,
            supporting_observation_count=0,
        )


def test_demand_signal_preserves_bounded_derived_assessments():
    signal = DemandSignal(
        topic="automated bookkeeping",
        demand_strength=80,
        evidence_quality=75,
        supporting_observation_count=3,
    )

    assert signal.demand_strength == 80
    assert signal.evidence_quality == 75
    assert signal.supporting_observation_count == 3


@pytest.mark.parametrize("field", ["demand_strength", "evidence_quality"])
def test_demand_signal_scores_are_bounded(field):
    for value in (-1, 101):
        with pytest.raises(ValueError):
            DemandSignal(
                topic="automation",
                demand_strength=80 if field != "demand_strength" else value,
                evidence_quality=75 if field != "evidence_quality" else value,
                supporting_observation_count=1,
            )
