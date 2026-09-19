import pytest
from datetime import datetime

from app.domain.economic_health import EconomicHealthEvidence
from app.domain.economic_performance_aggregation import EconomicPerformanceWindow
from app.domain.economic_stability_policy import (
    EconomicStabilityAssessment,
    EconomicStabilityEligibilityReason,
)
from app.domain.economic_stability_evidence_support import compose_economic_stability_evidence


def _window():
    return EconomicPerformanceWindow(datetime(2026, 1, 1), datetime(2026, 2, 1))


def _health():
    return EconomicHealthEvidence(
        business_id="b1",
        window=_window(),
        outcome_ids=("o1", "o2", "o3"),
        outcome_count=3,
        profitable_outcome_count=3,
        loss_outcome_count=0,
        profitable_outcome_rate=1.0,
        average_actual_profit=100.0,
        minimum_actual_profit=80.0,
        maximum_actual_profit=120.0,
        sample_profit_standard_deviation=20.0,
        average_actual_margin=0.5,
        average_actual_profit_per_effort_hour=50.0,
    )


def _assessment(*, eligible=True):
    return EconomicStabilityAssessment(
        business_id="b1",
        window=_window(),
        outcome_ids=("o1", "o2", "o3"),
        eligible=eligible,
        reason=(
            EconomicStabilityEligibilityReason.ELIGIBLE
            if eligible else EconomicStabilityEligibilityReason.PROFIT_VARIABILITY_ABOVE_THRESHOLD
        ),
        profit_stddev_ratio=0.2,
    )


def test_composes_health_and_stability_without_scoring():
    result = compose_economic_stability_evidence(health=_health(), stability=_assessment())
    assert result.business_id == "b1"
    assert result.outcome_ids == ("o1", "o2", "o3")
    assert result.profitable_outcome_rate == 1.0
    assert result.average_actual_profit == 100.0
    assert result.stability_eligible is True
    assert result.profit_stddev_ratio == 0.2


def test_ineligible_stability_does_not_erase_health_metrics():
    result = compose_economic_stability_evidence(
        health=_health(), stability=_assessment(eligible=False)
    )
    assert result.stability_eligible is False
    assert result.average_actual_profit == 100.0


def test_context_mismatch_is_rejected():
    stability = _assessment()
    mismatched = EconomicStabilityAssessment(
        business_id="other",
        window=stability.window,
        outcome_ids=stability.outcome_ids,
        eligible=True,
        reason=EconomicStabilityEligibilityReason.ELIGIBLE,
        profit_stddev_ratio=0.2,
    )
    with pytest.raises(ValueError):
        compose_economic_stability_evidence(health=_health(), stability=mismatched)


def test_lineage_mismatch_is_rejected():
    stability = _assessment()
    mismatched = EconomicStabilityAssessment(
        business_id="b1",
        window=stability.window,
        outcome_ids=("o1", "different", "o3"),
        eligible=True,
        reason=EconomicStabilityEligibilityReason.ELIGIBLE,
        profit_stddev_ratio=0.2,
    )
    with pytest.raises(ValueError):
        compose_economic_stability_evidence(health=_health(), stability=mismatched)


def test_missing_variability_remains_missing():
    health = _health()
    health = EconomicHealthEvidence(
        business_id=health.business_id,
        window=health.window,
        outcome_ids=health.outcome_ids,
        outcome_count=health.outcome_count,
        profitable_outcome_count=health.profitable_outcome_count,
        loss_outcome_count=health.loss_outcome_count,
        profitable_outcome_rate=health.profitable_outcome_rate,
        average_actual_profit=health.average_actual_profit,
        minimum_actual_profit=health.minimum_actual_profit,
        maximum_actual_profit=health.maximum_actual_profit,
        sample_profit_standard_deviation=None,
        average_actual_margin=health.average_actual_margin,
        average_actual_profit_per_effort_hour=health.average_actual_profit_per_effort_hour,
    )
    stability = EconomicStabilityAssessment(
        business_id="b1",
        window=_window(),
        outcome_ids=("o1", "o2", "o3"),
        eligible=False,
        reason=EconomicStabilityEligibilityReason.INSUFFICIENT_VARIABILITY_DATA,
        profit_stddev_ratio=None,
    )
    result = compose_economic_stability_evidence(health=health, stability=stability)
    assert result.profit_stddev_ratio is None
