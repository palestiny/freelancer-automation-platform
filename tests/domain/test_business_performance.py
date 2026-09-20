from datetime import datetime, timedelta, timezone

import pytest

from app.domain.business_performance import (
    BusinessPerformanceHistory,
    BusinessPerformanceObservation,
    PerformanceSourceType,
)


NOW = datetime(2026, 1, 1, 12, 0, 0)


def observation(
    id: str,
    actual: float,
    *,
    observed_at: datetime = NOW,
    expected: float | None = 10,
    business_id: str = "business-1",
    source_type: PerformanceSourceType = PerformanceSourceType.OPERATIONAL,
    evidence_quality: int = 50,
    metric_name: str = "delivery_hours",
    unit: str = "hours",
) -> BusinessPerformanceObservation:
    return BusinessPerformanceObservation(
        id=id,
        business_id=business_id,
        source_type=source_type,
        source_id=f"source-{id}",
        metric_name=metric_name,
        unit=unit,
        expected_value=expected,
        actual_value=actual,
        observed_at=observed_at,
        evidence_quality=evidence_quality,
    )


def test_observation_preserves_source_and_business_context():
    item = observation("o1", 12, source_type=PerformanceSourceType.REVENUE)

    assert item.business_id == "business-1"
    assert item.source_type is PerformanceSourceType.REVENUE
    assert item.source_id == "source-o1"


def test_observation_derives_variance_when_expected_exists():
    item = observation("o1", 12)

    assert item.variance == 2
    assert item.relative_variance == 0.2


def test_observation_does_not_invent_variance_without_expected_value():
    item = observation("o1", 12, expected=None)

    assert item.variance is None
    assert item.relative_variance is None


def test_history_rejects_cross_business_observations():
    with pytest.raises(ValueError):
        BusinessPerformanceHistory(
            business_id="business-1",
            observations=(observation("o1", 12, business_id="business-2"),),
        )


def test_history_orders_observations_by_observation_time():
    history = BusinessPerformanceHistory(
        business_id="business-1",
        observations=(
            observation("later", 13, observed_at=NOW + timedelta(days=2)),
            observation("earlier", 11, observed_at=NOW),
        ),
    )

    assert [item.id for item in history.ordered_observations] == ["earlier", "later"]


def test_history_filters_one_metric_and_unit():
    history = BusinessPerformanceHistory(
        business_id="business-1",
        observations=(
            observation("delivery", 12),
            observation(
                "defects",
                2,
                expected=1,
                metric_name="defects",
                unit="count",
            ),
        ),
    )

    assert [item.id for item in history.for_metric("delivery_hours", "hours")] == [
        "delivery"
    ]


def test_history_exposes_latest_observation():
    history = BusinessPerformanceHistory(
        business_id="business-1",
        observations=(
            observation("old", 11),
            observation("new", 14, observed_at=NOW + timedelta(days=1)),
        ),
    )

    assert history.latest_observation.id == "new"


def test_empty_history_has_no_latest_observation():
    history = BusinessPerformanceHistory(business_id="business-1")

    assert history.latest_observation is None


def test_evidence_quality_is_bounded():
    with pytest.raises(ValueError):
        observation("o1", 12, evidence_quality=101)


def test_observed_at_must_be_timezone_aware():
    from datetime import datetime, timezone
    import pytest

    with pytest.raises(ValueError, match="timezone-aware"):
        BusinessPerformanceObservation(
            id="obs-naive",
            business_id="biz-1",
            source_type=PerformanceSourceType.OPERATIONAL,
            source_id="work-1",
            metric_name="profit",
            unit="EGP",
            expected_value=100,
            actual_value=120,
            observed_at=datetime(2026, 9, 20),
            evidence_quality=80,
        )
