from datetime import datetime, timedelta

import pytest

from app.domain.performance_aggregation import aggregate_performance
from app.domain.performance_baseline import (
    BaselineEligibilityReason,
    PerformanceBaselinePolicy,
    assess_baseline,
)
from app.domain.performance_history import PerformanceWindow
from tests.domain.test_performance_aggregation import item


START = datetime(2026, 1, 1)


def aggregate(*, count: int = 3, evidence_quality: int = 80, end_offset: int = 1):
    window = PerformanceWindow(
        START,
        START + timedelta(days=end_offset),
    )
    observations = tuple(
        item(
            f"o{i}",
            10 + i,
            at=START + timedelta(hours=i + 1),
            evidence_quality=evidence_quality,
        )
        for i in range(count)
    )
    return aggregate_performance(observations, window=window)


def test_eligible_baseline_meets_all_policy_requirements():
    result = assess_baseline(
        aggregate=aggregate(),
        policy=PerformanceBaselinePolicy(),
        as_of=START + timedelta(days=2),
    )

    assert result.eligible is True
    assert result.reason is BaselineEligibilityReason.ELIGIBLE


def test_baseline_requires_minimum_observations():
    result = assess_baseline(
        aggregate=aggregate(count=2),
        policy=PerformanceBaselinePolicy(minimum_observations=3),
        as_of=START + timedelta(days=2),
    )

    assert result.eligible is False
    assert result.reason is BaselineEligibilityReason.INSUFFICIENT_OBSERVATIONS


def test_baseline_requires_minimum_evidence_quality():
    result = assess_baseline(
        aggregate=aggregate(evidence_quality=59),
        policy=PerformanceBaselinePolicy(minimum_average_evidence_quality=60),
        as_of=START + timedelta(days=2),
    )

    assert result.eligible is False
    assert result.reason is BaselineEligibilityReason.INSUFFICIENT_EVIDENCE_QUALITY


def test_baseline_requires_freshness():
    result = assess_baseline(
        aggregate=aggregate(end_offset=1),
        policy=PerformanceBaselinePolicy(maximum_age=timedelta(days=1)),
        as_of=START + timedelta(days=3),
    )

    assert result.eligible is False
    assert result.reason is BaselineEligibilityReason.STALE_BASELINE


def test_future_baseline_is_rejected():
    result = assess_baseline(
        aggregate=aggregate(end_offset=3),
        policy=PerformanceBaselinePolicy(),
        as_of=START + timedelta(days=2),
    )

    assert result.eligible is False
    assert result.reason is BaselineEligibilityReason.FUTURE_BASELINE


def test_missing_aggregate_is_not_eligible():
    result = assess_baseline(
        aggregate=None,
        policy=PerformanceBaselinePolicy(),
        as_of=START + timedelta(days=2),
    )

    assert result.eligible is False
    assert result.reason is BaselineEligibilityReason.INSUFFICIENT_OBSERVATIONS


@pytest.mark.parametrize(
    "kwargs",
    [
        {"minimum_observations": 0},
        {"minimum_average_evidence_quality": -1},
        {"minimum_average_evidence_quality": 101},
        {"maximum_age": timedelta(0)},
    ],
)
def test_policy_rejects_invalid_values(kwargs):
    with pytest.raises(ValueError):
        PerformanceBaselinePolicy(**kwargs)


def test_baseline_can_require_source_reliability():
    from app.domain.business_performance import PerformanceSourceType
    from app.domain.performance_reliability import PerformanceSourceReliabilityPolicy

    result = assess_baseline(
        aggregate=aggregate(),
        policy=PerformanceBaselinePolicy(
            source_reliability_policy=PerformanceSourceReliabilityPolicy(
                minimum_reliability=70,
                reliability_by_source_type=(
                    (PerformanceSourceType.OPERATIONAL, 60),
                ),
            )
        ),
        as_of=START + timedelta(days=2),
    )

    assert result.eligible is False
    assert result.reason is BaselineEligibilityReason.INSUFFICIENT_SOURCE_RELIABILITY


def test_baseline_rejects_unconfigured_source_when_reliability_is_required():
    from app.domain.business_performance import PerformanceSourceType
    from app.domain.performance_reliability import PerformanceSourceReliabilityPolicy

    result = assess_baseline(
        aggregate=aggregate(),
        policy=PerformanceBaselinePolicy(
            source_reliability_policy=PerformanceSourceReliabilityPolicy(
                reliability_by_source_type=(
                    (PerformanceSourceType.REVENUE, 90),
                ),
            )
        ),
        as_of=START + timedelta(days=2),
    )

    assert result.eligible is False
    assert result.reason is BaselineEligibilityReason.MISSING_SOURCE_RELIABILITY_POLICY
