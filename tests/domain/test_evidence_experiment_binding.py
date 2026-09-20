import pytest

from app.domain.evidence_learning_handoff import (
    EvidenceHandoffType,
    EvidenceLearningHandoff,
)
from app.domain.validation_experiment import ValidationExperiment
from app.domain.evidence_experiment_binding import bind_evidence_to_experiment


def _handoff(*, handoff_type=EvidenceHandoffType.EXPERIMENT, target="exp-1"):
    return EvidenceLearningHandoff(
        handoff_id="handoff-1",
        business_id="b1",
        metric_name="profit",
        unit="EGP",
        handoff_type=handoff_type,
        target=target,
        statement="Observed evidence supports testing the hypothesis.",
        observation_ids=("o1", "o2"),
    )


def test_binding_requires_matching_experiment_target():
    binding = bind_evidence_to_experiment(
        handoff=_handoff(),
        experiment=ValidationExperiment(
            id="exp-1",
            hypothesis="Test pricing",
            objective="Validate demand",
            success_criterion="At least 3 conversions",
        ),
    )
    assert binding.handoff_id == "handoff-1"
    assert binding.experiment_id == "exp-1"
    assert binding.observation_ids == ("o1", "o2")


def test_binding_rejects_policy_review_handoff():
    with pytest.raises(ValueError, match="EXPERIMENT"):
        bind_evidence_to_experiment(
            handoff=_handoff(handoff_type=EvidenceHandoffType.POLICY_REVIEW),
            experiment=ValidationExperiment(
                id="exp-1",
                hypothesis="Test pricing",
                objective="Validate demand",
                success_criterion="At least 3 conversions",
            ),
        )


def test_binding_rejects_target_identity_mismatch():
    with pytest.raises(ValueError, match="target"):
        bind_evidence_to_experiment(
            handoff=_handoff(target="different-experiment"),
            experiment=ValidationExperiment(
                id="exp-1",
                hypothesis="Test pricing",
                objective="Validate demand",
                success_criterion="At least 3 conversions",
            ),
        )


def test_binding_does_not_change_experiment_lifecycle():
    experiment = ValidationExperiment(
        id="exp-1",
        hypothesis="Test pricing",
        objective="Validate demand",
        success_criterion="At least 3 conversions",
    )
    bind_evidence_to_experiment(handoff=_handoff(), experiment=experiment)
    assert experiment.status.value == "DRAFT"
