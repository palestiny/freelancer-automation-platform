from datetime import datetime, timedelta

import pytest

from app.domain.business_performance import PerformanceSourceType\nfrom app.domain.performance_aggregation import aggregate_performance
from app.domain.performance_baseline import PerformanceBaselinePolicy
from app.domain.performance_comparison import (
    ComparisonRejectionReason,
    PerformanceComparisonPolicy,
    assess_performance_comparison,
)
from app.domain.performance_history import PerformanceWindow
from tests.domain.test_performance_aggregation import item


START = datetime(2026, 1, 1)


def aggregate(
    *,
    start_day: int,
    value: float,
    count: int = 3,
    evidence_quality: int = 80,
    business_id: str = "business-1",
):
    window = PerformanceWindow(
        START + timedelta(days=start_day),
        START + timedelta(days=start_day + 1),
    )
    observations = tuple(
        item(
            f"{start_day}-{i}",
            value + i,
            at=START + timedelta(days=start_day, hours=i + 1),
            evidence_quality=evidence_quality,
            business_id=business_id,
        )
        for i in range(count)
    )
    return aggregate_performance(observations, window=window)


def test_comparison_returns_trend_for_sufficient_non_overlapping_evidence():
    baseline = aggregate(start_day=0, value=10)
    current = aggregate(start_day=1, value=15)

    result = assess_performance_comparison(
        current=current,
        baseline=baseline,
        baseline_policy=PerformanceBaselinePolicy(),
        comparison_policy=PerformanceComparisonPolicy(),
        as_of=START + timedelta(days=2),
    )

    assert result.trend is not None
    assert result.rejection_reason is None
    assert result.trend.absolute_change == 5


def test_comparison_rejects_ineligible_baseline():
    baseline = aggregate(start_day=0, value=10, count=2)
    current = aggregate(start_day=1, value=15)

    result = assess_performance_comparison(
        current=current,
        baseline=baseline,
        baseline_policy=PerformanceBaselinePolicy(),
        comparison_policy=PerformanceComparisonPolicy(),
        as_of=START + timedelta(days=2),
    )

    assert result.trend is None
    assert result.rejection_reason is ComparisonRejectionReason.BASELINE_NOT_ELIGIBLE


def test_comparison_requires_current_observations():
    baseline = aggregate(start_day=0, value=10)
    current = aggregate(start_day=1, value=15, count=2)

    result = assess_performance_comparison(
        current=current,
        baseline=baseline,
        baseline_policy=PerformanceBaselinePolicy(),
        comparison_policy=PerformanceComparisonPolicy(minimum_current_observations=3),
        as_of=START + timedelta(days=2),
    )

    assert result.rejection_reason is ComparisonRejectionReason.INSUFFICIENT_CURRENT_OBSERVATIONS


def test_comparison_requires_current_evidence_quality():
    baseline = aggregate(start_day=0, value=10)
    current = aggregate(start_day=1, value=15, evidence_quality=59)

    result = assess_performance_comparison(
        current=current,
        baseline=baseline,
        baseline_policy=PerformanceBaselinePolicy(),
        comparison_policy=PerformanceComparisonPolicy(
            minimum_current_evidence_quality=60
        ),
        as_of=START + timedelta(days=2),
    )

    assert result.rejection_reason is ComparisonRejectionReason.INSUFFICIENT_CURRENT_EVIDENCE_QUALITY


def test_comparison_rejects_incompatible_context():
    baseline = aggregate(start_day=0, value=10)
    current = aggregate(start_day=1, value=15, business_id="business-2")

    result = assess_performance_comparison(
        current=current,
        baseline=baseline,
        baseline_policy=PerformanceBaselinePolicy(),
        comparison_policy=PerformanceComparisonPolicy(),
        as_of=START + timedelta(days=2),
    )

    assert result.rejection_reason is ComparisonRejectionReason.INCOMPATIBLE_CONTEXT


def test_comparison_rejects_overlapping_windows():
    baseline = aggregate(start_day=0, value=10)
    current_window = PerformanceWindow(START, START + timedelta(days=2))
    current = aggregate_performance(
        tuple(
            item(
                f"overlap-{i}",
                15 + i,
                at=START + timedelta(hours=i + 1),
            )
            for i in range(3)
        ),
        window=current_window,
    )

    result = assess_performance_comparison(
        current=current,
        baseline=baseline,
        baseline_policy=PerformanceBaselinePolicy(),
        comparison_policy=PerformanceComparisonPolicy(),
        as_of=START + timedelta(days=2),
    )

    assert result.rejection_reason is ComparisonRejectionReason.OVERLAPPING_WINDOWS


@pytest.mark.parametrize(
    "kwargs",
    [
        {"minimum_current_observations": 0},
        {"minimum_current_evidence_quality": -1},
        {"minimum_current_evidence_quality": 101},
    ],
)
def test_comparison_policy_rejects_invalid_values(kwargs):
    with pytest.raises(ValueError):
        PerformanceComparisonPolicy(**kwargs)


def test_comparison_rejects_incompatible_provenance():
    baseline = aggregate(start_day=0, value=10)
    current = aggregate(
        start_day=1,
        value=15,
        source_type=PerformanceSourceType.REVENUE,
    )

    result = assess_performance_comparison(
        current=current,
        baseline=baseline,
        baseline_policy=PerformanceBaselinePolicy(),
        comparison_policy=PerformanceComparisonPolicy(),
        as_of=START + timedelta(days=2),
    )

    assert result.rejection_reason is ComparisonRejectionReason.INCOMPATIBLE_CONTEXT
