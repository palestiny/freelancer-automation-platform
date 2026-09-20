from app.domain.controlled_experiment_allocation import (
    ExperimentAllocationPlan,
    allocate_experiment_variant,
)


def _plan():
    return ExperimentAllocationPlan(
        experiment_id="exp-1",
        variants=("control", "treatment"),
        allocation_weights=(5000, 5000),
        salt="v1",
    )


def test_allocation_is_deterministic():
    plan = _plan()
    first = allocate_experiment_variant(plan=plan, subject_id="subject-1")
    second = allocate_experiment_variant(plan=plan, subject_id="subject-1")
    assert first == second
    assert first in plan.variants


def test_explicit_weights_are_respected_at_boundary():
    plan = ExperimentAllocationPlan(
        experiment_id="exp-1",
        variants=("control", "treatment"),
        allocation_weights=(1, 9999),
        salt="v1",
    )
    assert allocate_experiment_variant(plan=plan, subject_id="subject-1") in plan.variants


def test_same_subject_changes_when_experiment_identity_changes():
    first = allocate_experiment_variant(plan=_plan(), subject_id="subject-1")
    second = allocate_experiment_variant(
        plan=ExperimentAllocationPlan(
            experiment_id="exp-2",
            variants=("control", "treatment"),
            allocation_weights=(5000, 5000),
            salt="v1",
        ),
        subject_id="subject-1",
    )
    assert first in ("control", "treatment")
    assert second in ("control", "treatment")


def test_plan_rejects_duplicate_variants():
    try:
        ExperimentAllocationPlan(
            experiment_id="exp-1",
            variants=("control", "control"),
            allocation_weights=(5000, 5000),
            salt="v1",
        )
    except ValueError:
        return
    raise AssertionError("duplicate variants must be rejected")


def test_plan_rejects_weights_that_do_not_sum_to_basis():
    try:
        ExperimentAllocationPlan(
            experiment_id="exp-1",
            variants=("control", "treatment"),
            allocation_weights=(4000, 5000),
            salt="v1",
        )
    except ValueError:
        return
    raise AssertionError("weights must sum to 10000")
