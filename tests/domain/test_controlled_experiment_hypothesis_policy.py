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


def _synthesis(*, direction: str, detected: bool, eligible: bool = True) -> ExperimentEvidenceSynthesis:
    difference = 1.0 if direction == "increased" else -1.0
    return ExperimentEvidenceSynthesis(
        experiment_id="exp1",
        metric_name="conversion",
        first_variant="control",
        second_variant="treatment",
        descriptive_difference=difference,
        statistical_difference=difference if eligible else None,
        statistical_detected=detected if eligible else None,
        status=(
            ExperimentEvidenceSynthesisStatus.DESCRIPTIVE_AND_STATISTICAL_ALIGNMENT
            if eligible and detected
            else ExperimentEvidenceSynthesisStatus.DESCRIPTIVE_CHANGE_WITHOUT_STATISTICAL_DETECTION
            if eligible
            else ExperimentEvidenceSynthesisStatus.STATISTICAL_EVIDENCE_UNAVAILABLE
        ),
        observation_ids=("a", "b", "c", "d"),
    )


def _policy(direction: ExperimentHypothesisDirection):
    return ControlledExperimentHypothesisPolicy(
        experiment_id="exp1",
        metric_name="conversion",
        direction=direction,
    )


def test_supports_increase_hypothesis_when_evidence_aligns():
    result = evaluate_experiment_hypothesis(
        synthesis=_synthesis(direction="increased", detected=True),
        policy=_policy(ExperimentHypothesisDirection.INCREASES),
    )
    assert result.outcome is HypothesisPolicyOutcome.SUPPORTS_HYPOTHESIS


def test_opposite_direction_does_not_support_hypothesis():
    result = evaluate_experiment_hypothesis(
        synthesis=_synthesis(direction="decreased", detected=True),
        policy=_policy(ExperimentHypothesisDirection.INCREASES),
    )
    assert result.outcome is HypothesisPolicyOutcome.DOES_NOT_SUPPORT_HYPOTHESIS


def test_ineligible_evidence_is_insufficient():
    result = evaluate_experiment_hypothesis(
        synthesis=_synthesis(direction="increased", detected=True, eligible=False),
        policy=_policy(ExperimentHypothesisDirection.INCREASES),
    )
    assert result.outcome is HypothesisPolicyOutcome.INSUFFICIENT_EVIDENCE
