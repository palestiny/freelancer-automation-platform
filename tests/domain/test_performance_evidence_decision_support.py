from datetime import datetime, timezone

from app.domain.business_performance import PerformanceSourceType
from app.domain.performance_reliability import (
    SourceReliabilityAssessment,
    SourceReliabilityReason,
)
from app.domain.performance_history import PerformanceWindow
from app.domain.statistical_mean_comparison import (
    MeanComparisonResult,
    MeanComparisonStatus,
)
from app.domain.statistical_evidence_composition import (
    StatisticalEvidenceComposition,
    StatisticalEvidenceEligibilityReason,
    StatisticalEvidenceInterpretation,
    compose_statistical_evidence,
)


def _window():
    return PerformanceWindow(
        start=datetime(2026, 1, 1, tzinfo=timezone.utc),
        end=datetime(2026, 1, 8, tzinfo=timezone.utc),
    )


def _result(*, status=MeanComparisonStatus.APPLICABLE, rejects_null=False):
    return MeanComparisonResult(
        business_id="b1",
        metric_name="profit",
        unit="EGP",
        first_window=_window(),
        second_window=PerformanceWindow(
            start=datetime(2026, 1, 8, tzinfo=timezone.utc),
            end=datetime(2026, 1, 15, tzinfo=timezone.utc),
        ),
        first_observation_ids=("a", "b"),
        second_observation_ids=("c", "d"),
        sample_size_first=2,
        sample_size_second=2,
        mean_first=100.0 if status is MeanComparisonStatus.APPLICABLE else None,
        mean_second=90.0 if status is MeanComparisonStatus.APPLICABLE else None,
        mean_difference=10.0 if status is MeanComparisonStatus.APPLICABLE else None,
        t_statistic=2.5 if status is MeanComparisonStatus.APPLICABLE else None,
        degrees_of_freedom=2.0 if status is MeanComparisonStatus.APPLICABLE else None,
        p_value=0.05 if status is MeanComparisonStatus.APPLICABLE else None,
        alpha=0.05,
        method="welch_two_sample_t_test",
        rejects_null=rejects_null if status is MeanComparisonStatus.APPLICABLE else None,
        status=status,
    )


def _eligible():
    return SourceReliabilityAssessment(
        eligible=True,
        reason=SourceReliabilityReason.ELIGIBLE,
        minimum_reliability=80,
    )


def test_detected_difference_is_eligible_when_evidence_gates_pass():
    result = compose_statistical_evidence(
        comparison=_result(rejects_null=True),
        current_evidence_quality=80,
        baseline_evidence_quality=75,
        current_source_reliability=_eligible(),
        baseline_source_reliability=_eligible(),
        minimum_evidence_quality=60,
    )

    assert result.eligible is True
    assert result.interpretation is StatisticalEvidenceInterpretation.STATISTICALLY_DETECTED_DIFFERENCE
    assert result.reason is StatisticalEvidenceEligibilityReason.ELIGIBLE
    assert result.observation_ids == ("a", "b", "c", "d")


def test_non_significant_result_remains_eligible_evidence():
    result = compose_statistical_evidence(
        comparison=_result(rejects_null=False),
        current_evidence_quality=80,
        baseline_evidence_quality=75,
        current_source_reliability=_eligible(),
        baseline_source_reliability=_eligible(),
        minimum_evidence_quality=60,
    )

    assert result.eligible is True
    assert result.interpretation is StatisticalEvidenceInterpretation.NO_STATISTICALLY_DETECTED_DIFFERENCE


def test_inapplicable_statistical_result_is_not_eligible():
    result = compose_statistical_evidence(
        comparison=_result(status=MeanComparisonStatus.INSUFFICIENT_OBSERVATIONS),
        current_evidence_quality=80,
        baseline_evidence_quality=75,
        current_source_reliability=_eligible(),
        baseline_source_reliability=_eligible(),
        minimum_evidence_quality=60,
    )

    assert result.eligible is False
    assert result.reason is StatisticalEvidenceEligibilityReason.STATISTICAL_RESULT_NOT_APPLICABLE
    assert result.interpretation is StatisticalEvidenceInterpretation.STATISTICAL_RESULT_NOT_APPLICABLE


def test_low_evidence_quality_blocks_statistical_evidence():
    result = compose_statistical_evidence(
        comparison=_result(rejects_null=True),
        current_evidence_quality=59,
        baseline_evidence_quality=80,
        current_source_reliability=_eligible(),
        baseline_source_reliability=_eligible(),
        minimum_evidence_quality=60,
    )

    assert result.eligible is False
    assert result.reason is StatisticalEvidenceEligibilityReason.INSUFFICIENT_EVIDENCE_QUALITY


def test_low_source_reliability_blocks_statistical_evidence():
    ineligible = SourceReliabilityAssessment(
        eligible=False,
        reason=SourceReliabilityReason.INSUFFICIENT_RELIABILITY,
        minimum_reliability=40,
    )
    result = compose_statistical_evidence(
        comparison=_result(rejects_null=True),
        current_evidence_quality=80,
        baseline_evidence_quality=80,
        current_source_reliability=ineligible,
        baseline_source_reliability=_eligible(),
        minimum_evidence_quality=60,
    )

    assert result.eligible is False
    assert result.reason is StatisticalEvidenceEligibilityReason.INSUFFICIENT_SOURCE_RELIABILITY


def test_result_rejects_overlapping_windows():
    import pytest
    comparison = _result()
    with pytest.raises(ValueError):
        StatisticalEvidenceComposition(
            business_id=comparison.business_id,
            metric_name=comparison.metric_name,
            unit=comparison.unit,
            method=comparison.method,
            observation_ids=("a", "b"),
            eligible=True,
            reason=StatisticalEvidenceEligibilityReason.ELIGIBLE,
            interpretation=StatisticalEvidenceInterpretation.STATISTICALLY_DETECTED_DIFFERENCE,
            alpha=0.05,
            mean_difference=10.0,
            first_window=PerformanceWindow(datetime(2026, 1, 1), datetime(2026, 1, 10)),
            second_window=PerformanceWindow(datetime(2026, 1, 9), datetime(2026, 1, 15)),
            current_evidence_quality=80,
            baseline_evidence_quality=80,
            current_source_reliability=_eligible(),
            baseline_source_reliability=_eligible(),
        )


def test_result_rejects_invalid_evidence_quality():
    import pytest
    comparison = _result()
    with pytest.raises(ValueError):
        StatisticalEvidenceComposition(
            business_id=comparison.business_id,
            metric_name=comparison.metric_name,
            unit=comparison.unit,
            method=comparison.method,
            observation_ids=("a", "b"),
            eligible=True,
            reason=StatisticalEvidenceEligibilityReason.ELIGIBLE,
            interpretation=StatisticalEvidenceInterpretation.STATISTICALLY_DETECTED_DIFFERENCE,
            alpha=0.05,
            mean_difference=10.0,
            first_window=comparison.first_window,
            second_window=comparison.second_window,
            current_evidence_quality=101,
            baseline_evidence_quality=80,
            current_source_reliability=_eligible(),
            baseline_source_reliability=_eligible(),
        )

def test_result_rejects_non_finite_mean_difference():
    import math
    import pytest

    source_reliability = _eligible()
    with pytest.raises(ValueError):
        StatisticalEvidenceComposition(
            business_id="b1",
            metric_name="profit",
            unit="EGP",
            method="welch_two_sample_t_test",
            observation_ids=("b1", "c1"),
            eligible=True,
            reason=StatisticalEvidenceEligibilityReason.ELIGIBLE,
            interpretation=StatisticalEvidenceInterpretation.STATISTICALLY_DETECTED_DIFFERENCE,
            alpha=0.05,
            mean_difference=math.nan,
            first_window=_window(),
            second_window=PerformanceWindow(datetime(2026, 1, 8, tzinfo=timezone.utc), datetime(2026, 1, 15, tzinfo=timezone.utc)),
            current_evidence_quality=80,
            baseline_evidence_quality=80,
            current_source_reliability=source_reliability,
            baseline_source_reliability=source_reliability,
        )


def test_result_rejects_blank_observation_ids():
    import pytest

    source_reliability = _eligible()
    with pytest.raises(ValueError):
        StatisticalEvidenceComposition(
            business_id="b1",
            metric_name="profit",
            unit="EGP",
            method="welch_two_sample_t_test",
            observation_ids=("b1", ""),
            eligible=True,
            reason=StatisticalEvidenceEligibilityReason.ELIGIBLE,
            interpretation=StatisticalEvidenceInterpretation.STATISTICALLY_DETECTED_DIFFERENCE,
            alpha=0.05,
            mean_difference=1.0,
            first_window=_window(),
            second_window=PerformanceWindow(datetime(2026, 1, 8, tzinfo=timezone.utc), datetime(2026, 1, 15, tzinfo=timezone.utc)),
            current_evidence_quality=80,
            baseline_evidence_quality=80,
            current_source_reliability=source_reliability,
            baseline_source_reliability=source_reliability,
        )

def test_eligible_result_rejects_ineligible_source_assessment():
    import pytest
    from app.domain.performance_reliability import SourceReliabilityAssessment, SourceReliabilityReason

    with pytest.raises(ValueError):
        StatisticalEvidenceComposition(
            business_id="b1", metric_name="profit", unit="EGP",
            method="welch_two_sample_t_test", observation_ids=("a", "b"),
            eligible=True, reason=StatisticalEvidenceEligibilityReason.ELIGIBLE,
            interpretation=StatisticalEvidenceInterpretation.STATISTICALLY_DETECTED_DIFFERENCE,
            alpha=0.05, first_window=_window(),
            second_window=PerformanceWindow(datetime(2026, 1, 8, tzinfo=timezone.utc), datetime(2026, 1, 15, tzinfo=timezone.utc)),
            current_evidence_quality=80, baseline_evidence_quality=80,
            current_source_reliability=SourceReliabilityAssessment(
                eligible=False, reason=SourceReliabilityReason.INSUFFICIENT_RELIABILITY,
                minimum_reliability=40,
            ),
            baseline_source_reliability=_eligible(), mean_difference=10.0,
        )


def test_source_reliability_reason_requires_an_ineligible_source():
    import pytest
    with pytest.raises(ValueError):
        StatisticalEvidenceComposition(
            business_id="b1", metric_name="profit", unit="EGP",
            method="welch_two_sample_t_test", observation_ids=("a", "b"),
            eligible=False,
            reason=StatisticalEvidenceEligibilityReason.INSUFFICIENT_SOURCE_RELIABILITY,
            interpretation=StatisticalEvidenceInterpretation.STATISTICALLY_DETECTED_DIFFERENCE,
            alpha=0.05, first_window=_window(),
            second_window=PerformanceWindow(datetime(2026, 1, 8, tzinfo=timezone.utc), datetime(2026, 1, 15, tzinfo=timezone.utc)),
            current_evidence_quality=80, baseline_evidence_quality=80,
            current_source_reliability=_eligible(), baseline_source_reliability=_eligible(),
            mean_difference=10.0,
        )


from datetime import datetime
import pytest
from app.domain.performance_history import PerformanceWindow
from app.domain.performance_trend import PerformanceTrend
from app.domain.statistical_evidence_composition import StatisticalEvidenceComposition, StatisticalEvidenceEligibilityReason, StatisticalEvidenceInterpretation
from app.domain.performance_evidence_decision_support import CombinedEvidencePosture, compose_performance_evidence

def trend(change=10.0):
 return PerformanceTrend(metric_name='profit',unit='EGP',current_window=PerformanceWindow(datetime(2026,2,1),datetime(2026,2,8)),baseline_window=PerformanceWindow(datetime(2026,1,25),datetime(2026,2,1)),current_average=100+change,baseline_average=100,absolute_change=change,relative_change=change/100,current_observation_ids=('c1',),baseline_observation_ids=('b1',),current_evidence_quality=80,baseline_evidence_quality=80)

def stat():
 return StatisticalEvidenceComposition(business_id='b1',metric_name='profit',unit='EGP',method='welch_two_sample_t_test',observation_ids=('b1','b2','c1','c2'),eligible=True,reason=StatisticalEvidenceEligibilityReason.ELIGIBLE,interpretation=StatisticalEvidenceInterpretation.STATISTICALLY_DETECTED_DIFFERENCE,alpha=.05,first_window=PerformanceWindow(datetime(2026,1,25),datetime(2026,2,1)),second_window=PerformanceWindow(datetime(2026,2,1),datetime(2026,2,8)),current_evidence_quality=80,baseline_evidence_quality=80,current_source_reliability=SourceReliabilityAssessment(eligible=True,reason=SourceReliabilityReason.ELIGIBLE,minimum_reliability=80),baseline_source_reliability=SourceReliabilityAssessment(eligible=True,reason=SourceReliabilityReason.ELIGIBLE,minimum_reliability=80),mean_difference=10.0)

def test_identity_and_lineage_are_preserved():
 r=compose_performance_evidence(trend=trend(),statistical_evidence=stat(),business_id='b1')
 assert r.business_id=='b1'
 assert r.statistical_observation_ids==('b1','b2','c1','c2')

@pytest.mark.parametrize('business_id',['','   '])
def test_empty_business_id_rejected(business_id):
 with pytest.raises(ValueError,match='business_id'): compose_performance_evidence(trend=trend(),statistical_evidence=stat(),business_id=business_id)

def test_zero_change_is_no_descriptive_change():
 r=compose_performance_evidence(trend=trend(0),statistical_evidence=stat(),business_id='b1')
 assert r.posture is CombinedEvidencePosture.NO_DESCRIPTIVE_CHANGE


def test_result_rejects_duplicate_statistical_lineage():
    from app.domain.performance_evidence_decision_support import (
        DescriptiveDirection,
        InferentialStatus,
        PerformanceEvidenceDecisionSupport,
    )

    with pytest.raises(ValueError, match="statistical_observation_ids must be unique"):
        PerformanceEvidenceDecisionSupport(
            business_id="b1",
            metric_name="profit",
            unit="EGP",
            descriptive_direction=DescriptiveDirection.INCREASED,
            inferential_status=InferentialStatus.STATISTICAL_DIFFERENCE_DETECTED,
            posture=CombinedEvidencePosture.DESCRIPTIVE_CHANGE_WITH_STATISTICAL_DETECTION,
            statistical_observation_ids=("x", "x"),
        )


def test_result_rejects_empty_context():
    from app.domain.performance_evidence_decision_support import (
        DescriptiveDirection,
        InferentialStatus,
        PerformanceEvidenceDecisionSupport,
    )

    with pytest.raises(ValueError, match="business_id cannot be empty"):
        PerformanceEvidenceDecisionSupport(
            business_id="",
            metric_name="profit",
            unit="EGP",
            descriptive_direction=DescriptiveDirection.NO_CHANGE,
            inferential_status=InferentialStatus.UNAVAILABLE,
            posture=CombinedEvidencePosture.INFERENTIAL_EVIDENCE_UNAVAILABLE,
            statistical_observation_ids=(),
        )
