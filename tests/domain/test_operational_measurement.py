from datetime import datetime, timedelta

import pytest

from app.domain.operational_measurement import (
    BusinessPerformanceSnapshot,
    ImprovementHandoff,
    ImprovementRecommendation,
    LearningSignal,
    OperationalMeasurement,
    WorkItemOutcomeObservation,
    WorkOutcome,
)


NOW = datetime(2026, 1, 1, 12, 0, 0)


def test_work_item_outcome_observation_preserves_business_context():
    observation = WorkItemOutcomeObservation(
        id="outcome-1",
        business_id="business-1",
        work_item_id="work-1",
        observed_at=NOW,
        outcome=WorkOutcome.SUCCEEDED,
        evidence_quality=80,
    )

    assert observation.business_id == "business-1"
    assert observation.work_item_id == "work-1"
    assert observation.outcome is WorkOutcome.SUCCEEDED


def test_work_item_outcome_observation_validates_evidence_quality():
    with pytest.raises(ValueError):
        WorkItemOutcomeObservation(
            id="outcome-1",
            business_id="business-1",
            work_item_id="work-1",
            observed_at=NOW,
            outcome=WorkOutcome.SUCCEEDED,
            evidence_quality=101,
        )


def test_operational_measurement_derives_variance():
    measurement = OperationalMeasurement(
        id="measurement-1",
        business_id="business-1",
        metric_name="delivery_hours",
        unit="hours",
        expected_value=10,
        actual_value=12,
        measured_at=NOW,
        evidence_quality=85,
    )

    assert measurement.evidence_quality == 85
    assert measurement.variance == 2
    assert measurement.relative_variance == 0.2


def test_operational_measurement_handles_zero_expected_value():
    measurement = OperationalMeasurement(
        id="measurement-1",
        business_id="business-1",
        metric_name="defects",
        unit="count",
        expected_value=0,
        actual_value=2,
        measured_at=NOW,
    )

    assert measurement.variance == 2
    assert measurement.relative_variance is None


def test_business_performance_snapshot_requires_one_business_context():
    measurement = OperationalMeasurement(
        id="measurement-1",
        business_id="business-2",
        metric_name="delivery_hours",
        unit="hours",
        expected_value=10,
        actual_value=12,
        measured_at=NOW,
    )

    with pytest.raises(ValueError):
        BusinessPerformanceSnapshot(
            id="snapshot-1",
            business_id="business-1",
            period_start=NOW,
            period_end=NOW + timedelta(days=1),
            measurements=(measurement,),
        )


def test_business_performance_snapshot_accepts_matching_measurements():
    measurement = OperationalMeasurement(
        id="measurement-1",
        business_id="business-1",
        metric_name="delivery_hours",
        unit="hours",
        expected_value=10,
        actual_value=12,
        measured_at=NOW,
    )

    snapshot = BusinessPerformanceSnapshot(
        id="snapshot-1",
        business_id="business-1",
        period_start=NOW,
        period_end=NOW + timedelta(days=1),
        measurements=(measurement,),
    )

    assert snapshot.measurements == (measurement,)


def test_learning_signal_is_derived_evidence():
    signal = LearningSignal(
        id="learning-1",
        business_id="business-1",
        source_measurement_ids=("measurement-1",),
        statement="Delivery consistently takes longer than expected.",
        evidence_quality=90,
    )

    assert signal.business_id == "business-1"
    assert signal.source_measurement_ids == ("measurement-1",)


def test_improvement_recommendation_requires_explicit_handoff():
    recommendation = ImprovementRecommendation(
        id="recommendation-1",
        business_id="business-1",
        learning_signal_id="learning-1",
        statement="Run an experiment on the delivery process.",
        handoff=ImprovementHandoff.EXPERIMENT,
    )

    assert recommendation.handoff is ImprovementHandoff.EXPERIMENT


def test_improvement_recommendation_is_not_an_execution_command():
    recommendation = ImprovementRecommendation(
        id="recommendation-1",
        business_id="business-1",
        learning_signal_id="learning-1",
        statement="Review the delivery policy.",
        handoff=ImprovementHandoff.POLICY_REVIEW,
    )

    assert not hasattr(recommendation, "execute")
