from datetime import datetime

import pytest

from app.domain.operational_learning import (
    OperationalLearningPolicy,
    derive_learning_signal,
)
from app.domain.operational_measurement import OperationalMeasurement


NOW = datetime(2026, 1, 1, 12, 0, 0)


def measurement(id: str, actual: float, business_id: str = "business-1"):
    return OperationalMeasurement(
        id=id,
        business_id=business_id,
        metric_name="delivery_hours",
        unit="hours",
        expected_value=10,
        actual_value=actual,
        measured_at=NOW,
    )


def test_learning_requires_minimum_observations():
    signal = derive_learning_signal(
        (measurement("m1", 12), measurement("m2", 13)),
        policy=OperationalLearningPolicy(minimum_observations=3),
        signal_id="l1",
        statement="Delivery is consistently slower than expected.",
    )

    assert signal is None


def test_learning_signal_is_derived_from_repeated_variance():
    signal = derive_learning_signal(
        (measurement("m1", 12), measurement("m2", 13), measurement("m3", 12)),
        policy=OperationalLearningPolicy(minimum_observations=3),
        signal_id="l1",
        statement="Delivery is consistently slower than expected.",
    )

    assert signal is not None
    assert signal.source_measurement_ids == ("m1", "m2", "m3")
    assert signal.business_id == "business-1"


def test_small_variance_does_not_create_learning_signal():
    signal = derive_learning_signal(
        (measurement("m1", 10.2), measurement("m2", 10.3), measurement("m3", 10.1)),
        policy=OperationalLearningPolicy(
            minimum_observations=3,
            minimum_average_relative_variance=0.10,
        ),
        signal_id="l1",
        statement="Delivery variance is material.",
    )

    assert signal is None


def test_learning_rejects_cross_business_measurements():
    with pytest.raises(ValueError):
        derive_learning_signal(
            (measurement("m1", 12), measurement("m2", 13, business_id="business-2"), measurement("m3", 12)),
            policy=OperationalLearningPolicy(),
            signal_id="l1",
            statement="Cross-business evidence must not be combined.",
        )


def test_learning_rejects_mixed_metrics():
    mixed = OperationalMeasurement(
        id="m2",
        business_id="business-1",
        metric_name="defects",
        unit="count",
        expected_value=1,
        actual_value=2,
        measured_at=NOW,
    )

    with pytest.raises(ValueError):
        derive_learning_signal(
            (measurement("m1", 12), mixed, measurement("m3", 12)),
            policy=OperationalLearningPolicy(),
            signal_id="l1",
            statement="Metrics must match.",
        )


def test_learning_signal_carries_average_measurement_evidence_quality():
    measurements = (
        OperationalMeasurement(
            id="m1",
            business_id="business-1",
            metric_name="delivery_hours",
            unit="hours",
            expected_value=10,
            actual_value=12,
            measured_at=NOW,
            evidence_quality=80,
        ),
        OperationalMeasurement(
            id="m2",
            business_id="business-1",
            metric_name="delivery_hours",
            unit="hours",
            expected_value=10,
            actual_value=13,
            measured_at=NOW,
            evidence_quality=60,
        ),
        OperationalMeasurement(
            id="m3",
            business_id="business-1",
            metric_name="delivery_hours",
            unit="hours",
            expected_value=10,
            actual_value=12,
            measured_at=NOW,
            evidence_quality=100,
        ),
    )

    signal = derive_learning_signal(
        measurements,
        policy=OperationalLearningPolicy(),
        signal_id="l1",
        statement="Delivery variance is repeatedly material.",
    )

    assert signal is not None
    assert signal.evidence_quality == 80


def test_learning_requires_minimum_average_evidence_quality():
    measurements = (
        OperationalMeasurement(
            id="m1",
            business_id="business-1",
            metric_name="delivery_hours",
            unit="hours",
            expected_value=10,
            actual_value=12,
            measured_at=NOW,
            evidence_quality=40,
        ),
        OperationalMeasurement(
            id="m2",
            business_id="business-1",
            metric_name="delivery_hours",
            unit="hours",
            expected_value=10,
            actual_value=13,
            measured_at=NOW,
            evidence_quality=50,
        ),
        OperationalMeasurement(
            id="m3",
            business_id="business-1",
            metric_name="delivery_hours",
            unit="hours",
            expected_value=10,
            actual_value=12,
            measured_at=NOW,
            evidence_quality=50,
        ),
    )

    signal = derive_learning_signal(
        measurements,
        policy=OperationalLearningPolicy(minimum_average_evidence_quality=60),
        signal_id="l1",
        statement="Delivery variance is repeatedly material.",
    )

    assert signal is None


@pytest.mark.parametrize(
    "kwargs",
    [
        {"minimum_average_evidence_quality": -1},
        {"minimum_average_evidence_quality": 101},
    ],
)
def test_learning_policy_rejects_invalid_evidence_quality(kwargs):
    with pytest.raises(ValueError):
        OperationalLearningPolicy(**kwargs)
