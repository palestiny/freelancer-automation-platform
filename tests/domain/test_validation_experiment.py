import pytest

from app.domain.validation_experiment import (
    ExperimentDecision,
    ExperimentOutcome,
    ExperimentResult,
    ExperimentStatus,
    ValidationExperiment,
)


def make_experiment() -> ValidationExperiment:
    return ValidationExperiment(
        id="exp-1",
        hypothesis="Customers will pay for the service.",
        objective="Test willingness to pay.",
        success_criterion="At least 3 paid commitments.",
        variants=("standard_offer", "premium_offer"),
        budget_limit=100.0,
    )


def test_experiment_preserves_hypothesis_and_controlled_variants():
    experiment = make_experiment()
    assert experiment.hypothesis == "Customers will pay for the service."
    assert experiment.variants == ("standard_offer", "premium_offer")


def test_experiment_lifecycle_is_explicit():
    experiment = make_experiment()
    planned = experiment.plan()
    running = planned.start()
    completed = running.complete()
    assert planned.status is ExperimentStatus.PLANNED
    assert running.status is ExperimentStatus.RUNNING
    assert completed.status is ExperimentStatus.COMPLETED


def test_experiment_rejects_empty_core_fields():
    with pytest.raises(ValueError, match="hypothesis"):
        ValidationExperiment(
            id="exp-1", hypothesis=" ", objective="Test", success_criterion="One result"
        )


def test_experiment_rejects_invalid_budget_and_variants():
    with pytest.raises(ValueError, match="budget_limit"):
        ValidationExperiment(
            id="exp-1", hypothesis="H", objective="O", success_criterion="C", budget_limit=-1
        )

    with pytest.raises(ValueError, match="variants"):
        ValidationExperiment(
            id="exp-1", hypothesis="H", objective="O", success_criterion="C", variants=("A", "A")
        )


def test_validated_result_requires_success_criterion():
    result = ExperimentResult(
        experiment_id="exp-1",
        outcome=ExperimentOutcome.VALIDATED,
        observed_measurement="3 paid commitments",
        success_criterion_met=True,
        evidence_statement="Three customers paid.",
        decision=ExperimentDecision.PROMOTE,
    )
    assert result.decision is ExperimentDecision.PROMOTE


def test_invalidated_result_requires_failed_criterion():
    result = ExperimentResult(
        experiment_id="exp-1",
        outcome=ExperimentOutcome.INVALIDATED,
        observed_measurement="0 paid commitments",
        success_criterion_met=False,
        evidence_statement="No customer paid.",
        decision=ExperimentDecision.REJECT,
    )
    assert result.decision is ExperimentDecision.REJECT


def test_inconclusive_result_must_continue_testing():
    result = ExperimentResult(
        experiment_id="exp-1",
        outcome=ExperimentOutcome.INCONCLUSIVE,
        observed_measurement="1 interested customer",
        success_criterion_met=False,
        evidence_statement="Interest was observed but not enough to validate willingness to pay.",
        decision=ExperimentDecision.CONTINUE_TESTING,
    )
    assert result.outcome is ExperimentOutcome.INCONCLUSIVE


def test_inconclusive_cannot_promote_or_reject():
    with pytest.raises(ValueError, match="INCONCLUSIVE"):
        ExperimentResult(
            experiment_id="exp-1",
            outcome=ExperimentOutcome.INCONCLUSIVE,
            observed_measurement="1 interested customer",
            success_criterion_met=False,
            evidence_statement="Insufficient evidence.",
            decision=ExperimentDecision.PROMOTE,
        )
