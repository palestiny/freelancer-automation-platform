from datetime import datetime
import pytest

from app.domain.performance_history import PerformanceWindow

from app.domain.evidence_decision_context import (
    EvidenceDecisionContext,
    build_evidence_decision_context,
)
from app.domain.performance_evidence_decision_support import (
    CombinedEvidencePosture,
    DescriptiveDirection,
    InferentialStatus,
    PerformanceEvidenceDecisionSupport,
)


def _support():
    return PerformanceEvidenceDecisionSupport(
        business_id="b1",
        metric_name="profit",
        unit="EGP",
        descriptive_direction=DescriptiveDirection.IMPROVING,
        inferential_status=InferentialStatus.STATISTICAL_DIFFERENCE_DETECTED,
        posture=CombinedEvidencePosture.DESCRIPTIVE_CHANGE_WITH_STATISTICAL_DETECTION,
            statistical_difference_direction=DescriptiveDirection.IMPROVING,
        statistical_observation_ids=("a", "b", "c", "d"),
        statistical_method="welch_two_sample_t_test",
        statistical_first_window=PerformanceWindow(datetime(2026, 1, 25), datetime(2026, 2, 1)),
        statistical_second_window=PerformanceWindow(datetime(2026, 2, 1), datetime(2026, 2, 8)),
        statistical_difference_direction=DescriptiveDirection.IMPROVING,
        current_observation_ids=("c1", "c2"),
        baseline_observation_ids=("b1", "b2"),
    )


def test_context_preserves_support_and_provenance():
    result = build_evidence_decision_context(
        support=_support(),
        source_references=("performance_trend:1", "statistical_evidence:2"),
        current_evidence_quality=80,
        baseline_evidence_quality=75,
    )
    assert isinstance(result, EvidenceDecisionContext)
    assert result.posture is CombinedEvidencePosture.DESCRIPTIVE_CHANGE_WITH_STATISTICAL_DETECTION
    assert result.source_references == ("performance_trend:1", "statistical_evidence:2")
    assert result.statistical_observation_ids == ("a", "b", "c", "d")


def test_missing_source_references_are_rejected():
    with pytest.raises(ValueError):
        build_evidence_decision_context(
            support=_support(),
            source_references=(),
            current_evidence_quality=80,
            baseline_evidence_quality=75,
        )


@pytest.mark.parametrize("value", [-1, 101])
def test_evidence_quality_is_bounded(value):
    with pytest.raises(ValueError):
        build_evidence_decision_context(
            support=_support(),
            source_references=("performance_trend:1",),
            current_evidence_quality=value,
            baseline_evidence_quality=75,
        )
