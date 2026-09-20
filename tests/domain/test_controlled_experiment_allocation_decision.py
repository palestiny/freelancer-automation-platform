from app.domain.controlled_experiment_allocation import (
    ExperimentAllocationDecision,
    ExperimentAllocationPlan,
    allocate_experiment,
    allocate_experiment_variant,
)


def _plan():
    return ExperimentAllocationPlan(
        experiment_id="exp-1",
        variants=("control", "variant"),
        allocation_weights=(5000, 5000),
        salt="salt-1",
    )


def test_allocation_decision_preserves_identity_and_bucket():
    decision = allocate_experiment(plan=_plan(), subject_id="subject-1")

    assert isinstance(decision, ExperimentAllocationDecision)
    assert decision.experiment_id == "exp-1"
    assert decision.subject_id == "subject-1"
    assert decision.variant == allocate_experiment_variant(
        plan=_plan(), subject_id="subject-1"
    )
    assert 0 <= decision.bucket < 10_000


def test_allocation_decision_is_reproducible():
    first = allocate_experiment(plan=_plan(), subject_id="subject-2")
    second = allocate_experiment(plan=_plan(), subject_id="subject-2")

    assert first == second


def test_allocation_variant_compatibility_remains_stable():
    assert allocate_experiment_variant(plan=_plan(), subject_id="subject-3") == allocate_experiment(
        plan=_plan(), subject_id="subject-3"
    ).variant
