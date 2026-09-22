from datetime import datetime
from app.domain.performance_history import PerformanceWindow
from app.domain.performance_trend import PerformanceTrend
from app.domain.statistical_evidence_composition import StatisticalEvidenceComposition, StatisticalEvidenceEligibilityReason, StatisticalEvidenceInterpretation
from app.domain.performance_evidence_decision_support import CombinedEvidencePosture, compose_performance_evidence
from app.domain.performance_reliability import SourceReliabilityAssessment, SourceReliabilityReason
from app.domain.performance_evidence_decision_policy import PerformanceEvidenceState, derive_performance_evidence_state

def trend(change):
    return PerformanceTrend(metric_name="profit", unit="EGP", current_window=PerformanceWindow(datetime(2026,2,1),datetime(2026,2,8)), baseline_window=PerformanceWindow(datetime(2026,1,25),datetime(2026,2,1)), current_average=100+change, baseline_average=100, absolute_change=change, relative_change=change/100, current_observation_ids=("c",), baseline_observation_ids=("b",), current_evidence_quality=80, baseline_evidence_quality=80)

def stat(interpretation, eligible=True):
    reliability = SourceReliabilityAssessment(eligible=True, reason=SourceReliabilityReason.ELIGIBLE, minimum_reliability=80)
    return StatisticalEvidenceComposition(
        business_id="b1", metric_name="profit", unit="EGP",
        method="welch_two_sample_t_test", observation_ids=("b","c"),
        eligible=eligible,
        reason=StatisticalEvidenceEligibilityReason.ELIGIBLE if eligible else StatisticalEvidenceEligibilityReason.INSUFFICIENT_EVIDENCE_QUALITY,
        interpretation=interpretation, alpha=.05,
        first_window=PerformanceWindow(datetime(2026,1,25), datetime(2026,2,1)),
        second_window=PerformanceWindow(datetime(2026,2,1), datetime(2026,2,8)),
        current_evidence_quality=80, baseline_evidence_quality=80,
        current_source_reliability=reliability, baseline_source_reliability=reliability,
        mean_difference=10,
    )

def evidence(change, interpretation, eligible=True):
    return compose_performance_evidence(trend=trend(change), statistical_evidence=stat(interpretation,eligible), business_id="b1")

def test_supports_improvement():
    assert derive_performance_evidence_state(evidence(10, StatisticalEvidenceInterpretation.STATISTICALLY_DETECTED_DIFFERENCE)) is PerformanceEvidenceState.SUPPORTS_IMPROVEMENT

def test_supports_decline():
    assert derive_performance_evidence_state(evidence(-10, StatisticalEvidenceInterpretation.STATISTICALLY_DETECTED_DIFFERENCE)) is PerformanceEvidenceState.SUPPORTS_DECLINE

def test_preserves_change_without_detection():
    assert derive_performance_evidence_state(evidence(10, StatisticalEvidenceInterpretation.NO_STATISTICALLY_DETECTED_DIFFERENCE)) is PerformanceEvidenceState.DESCRIPTIVE_CHANGE_WITHOUT_STATISTICAL_DETECTION

def test_ineligible_inference_not_upgraded():
    assert derive_performance_evidence_state(evidence(10, StatisticalEvidenceInterpretation.STATISTICALLY_DETECTED_DIFFERENCE, False)) is PerformanceEvidenceState.INSUFFICIENT_INFERENTIAL_EVIDENCE

def test_no_change_with_statistical_detection_is_explicitly_preserved():
    result = evidence(0, StatisticalEvidenceInterpretation.STATISTICALLY_DETECTED_DIFFERENCE)
    assert result.posture is CombinedEvidencePosture.NO_DESCRIPTIVE_CHANGE
