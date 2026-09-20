from app.domain.controlled_experiment_evidence_synthesis import (
    ExperimentEvidenceSynthesis,
    ExperimentEvidenceSynthesisStatus,
)
from app.domain.controlled_experiment_hypothesis_policy import (
    ControlledExperimentHypothesisPolicy,
    ExperimentHypothesisDirection,
    HypothesisPolicyOutcome,
    evaluate_experiment_hypothesis,
)


def test_supports_increase_hypothesis_when_evidence_aligns():
    synthesis = {
        "experiment_id": "exp1",
        "metric_name": "conversion",
        "control_variant_id": "control",
        "treatment_variant_id": "treatment",
        "descriptive_direction": "increased",
        "statistical_difference_detected": True,
        "evidence_eligible": True,
        "observation_ids": ("a", "b", "c", "d"),
    }
    result = evaluate_experiment_hypothesis(
        synthesis=synthesis,
        policy=ControlledExperimentHypothesisPolicy(
            experiment_id="exp1",
            metric_name="conversion",
            direction=ExperimentHypothesisDirection.INCREASES,
        ),
    )
    assert result.outcome is HypothesisPolicyOutcome.SUPPORTS_HYPOTHESIS


def test_opposite_direction_does_not_support_hypothesis():
    synthesis = {
        "experiment_id": "exp1",
        "metric_name": "conversion",
        "control_variant_id": "control",
        "treatment_variant_id": "treatment",
        "descriptive_direction": "decreased",
        "statistical_difference_detected": True,
        "evidence_eligible": True,
        "observation_ids": ("a", "b", "c", "d"),
    }
    result = evaluate_experiment_hypothesis(
        synthesis=synthesis,
        policy=ControlledExperimentHypothesisPolicy(
            experiment_id="exp1",
            metric_name="conversion",
            direction=ExperimentHypothesisDirection.INCREASES,
        ),
    )
    assert result.outcome is HypothesisPolicyOutcome.DOES_NOT_SUPPORT_HYPOTHESIS


def test_ineligible_evidence_is_insufficient():
    synthesis = {
        "experiment_id": "exp1",
        "metric_name": "conversion",
        "control_variant_id": "control",
        "treatment_variant_id": "treatment",
        "descriptive_direction": "increased",
        "statistical_difference_detected": True,
        "evidence_eligible": False,
        "observation_ids": ("a", "b", "c", "d"),
    }
    result = evaluate_experiment_hypothesis(
        synthesis=synthesis,
        policy=ControlledExperimentHypothesisPolicy(
            experiment_id="exp1",
            metric_name="conversion",
            direction=ExperimentHypothesisDirection.INCREASES,
        ),
    )
    assert result.outcome is HypothesisPolicyOutcome.INSUFFICIENT_EVIDENCE
