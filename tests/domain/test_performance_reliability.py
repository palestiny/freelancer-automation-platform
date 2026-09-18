from app.domain.performance_aggregation import PerformanceAggregate
from app.domain.business_performance import PerformanceSourceType
from app.domain.performance_reliability import (
    PerformanceSourceReliabilityPolicy,
    SourceReliabilityReason,
    assess_source_reliability,
)


def test_reliability_policy_accepts_sources_meeting_minimum():
    policy = PerformanceSourceReliabilityPolicy(
        minimum_reliability=60,
        reliability_by_source_type=(
            (PerformanceSourceType.OPERATIONAL, 80),
            (PerformanceSourceType.REVENUE, 70),
        ),
    )

    aggregate = PerformanceAggregate(
        business_id="business-1",
        metric_name="delivery_hours",
        unit="hours",
        window=__import__("app.domain.performance_history", fromlist=["PerformanceWindow"]).PerformanceWindow(
            __import__("datetime").datetime(2026, 1, 1),
            __import__("datetime").datetime(2026, 1, 2),
        ),
        observation_ids=("o1", "o2"),
        source_types=(
            PerformanceSourceType.OPERATIONAL,
            PerformanceSourceType.REVENUE,
        ),
        actual_count=2,
        actual_average=10,
        actual_min=8,
        actual_max=12,
        expected_count=0,
        expected_average=None,
        average_variance=None,
        average_relative_variance=None,
        average_evidence_quality=80,
    )

    result = assess_source_reliability(aggregate=aggregate, policy=policy)

    assert result.eligible is True
    assert result.reason is SourceReliabilityReason.ELIGIBLE
    assert result.minimum_reliability == 70


def test_reliability_policy_uses_weakest_source_in_mixed_evidence():
    policy = PerformanceSourceReliabilityPolicy(
        minimum_reliability=70,
        reliability_by_source_type=(
            (PerformanceSourceType.OPERATIONAL, 90),
            (PerformanceSourceType.REVENUE, 60),
        ),
    )
    aggregate = _aggregate(
        source_types=(
            PerformanceSourceType.OPERATIONAL,
            PerformanceSourceType.REVENUE,
        )
    )

    result = assess_source_reliability(aggregate=aggregate, policy=policy)

    assert result.eligible is False
    assert result.reason is SourceReliabilityReason.INSUFFICIENT_RELIABILITY
    assert result.minimum_reliability == 60


def test_reliability_policy_rejects_missing_source_configuration():
    policy = PerformanceSourceReliabilityPolicy(
        reliability_by_source_type=((PerformanceSourceType.OPERATIONAL, 80),)
    )
    aggregate = _aggregate(source_types=(PerformanceSourceType.REVENUE,))

    result = assess_source_reliability(aggregate=aggregate, policy=policy)

    assert result.eligible is False
    assert result.reason is SourceReliabilityReason.MISSING_SOURCE_POLICY
    assert result.minimum_reliability is None


def test_reliability_policy_rejects_invalid_configuration():
    try:
        PerformanceSourceReliabilityPolicy(
            minimum_reliability=101,
            reliability_by_source_type=(
                (PerformanceSourceType.OPERATIONAL, 80),
            ),
        )
    except ValueError:
        pass
    else:
        raise AssertionError("invalid minimum reliability must fail")


def _aggregate(*, source_types: tuple[PerformanceSourceType, ...]) -> PerformanceAggregate:
    from datetime import datetime
    from app.domain.performance_history import PerformanceWindow

    return PerformanceAggregate(
        business_id="business-1",
        metric_name="delivery_hours",
        unit="hours",
        window=PerformanceWindow(datetime(2026, 1, 1), datetime(2026, 1, 2)),
        observation_ids=tuple(f"o{i}" for i in range(len(source_types))),
        source_types=source_types,
        actual_count=len(source_types),
        actual_average=10,
        actual_min=10,
        actual_max=10,
        expected_count=0,
        expected_average=None,
        average_variance=None,
        average_relative_variance=None,
        average_evidence_quality=80,
    )
