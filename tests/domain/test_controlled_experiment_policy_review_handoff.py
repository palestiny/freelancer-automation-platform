from app.domain.controlled_experiment_hypothesis_policy import (
    ControlledExperimentHypothesisPolicyResult,
    ExperimentHypothesisDirection,
    HypothesisPolicyOutcome,
)
from app.domain.controlled_experiment_policy_review_handoff import (
    ExperimentPolicyReviewPosture,
    create_experiment_policy_review_handoff,
)


def _result(outcome):
    return ControlledExperimentHypothesisPolicyResult(
        experiment_id="exp-1",
        metric_name="revenue",
        direction=ExperimentHypothesisDirection.INCREASES,
        outcome=outcome,
        observation_ids=("a", "b", "c"),
    )


def test_supporting_policy_result_becomes_review_evidence_only():
    result = create_experiment_policy_review_handoff(
        handoff_id="handoff-1", policy_result=_result(HypothesisPolicyOutcome.SUPPORTS_HYPOTHESIS)
    )
    assert result.posture is ExperimentPolicyReviewPosture.REVIEW_SUPPORTS_HYPOTHESIS
    assert result.observation_ids == ("a", "b", "c")
    assert result.policy_outcome is HypothesisPolicyOutcome.SUPPORTS_HYPOTHESIS


def test_non_support_is_preserved():
    result = create_experiment_policy_review_handoff(
        handoff_id="handoff-2", policy_result=_result(HypothesisPolicyOutcome.DOES_NOT_SUPPORT_HYPOTHESIS)
    )
    assert result.posture is ExperimentPolicyReviewPosture.REVIEW_DOES_NOT_SUPPORT_HYPOTHESIS


def test_insufficient_evidence_is_distinct():
    result = create_experiment_policy_review_handoff(
        handoff_id="handoff-3", policy_result=_result(HypothesisPolicyOutcome.INSUFFICIENT_EVIDENCE)
    )
    assert result.posture is ExperimentPolicyReviewPosture.REVIEW_INSUFFICIENT_EVIDENCE


def test_policy_inapplicable_is_distinct():
    result = create_experiment_policy_review_handoff(
        handoff_id="handoff-4", policy_result=_result(HypothesisPolicyOutcome.POLICY_INAPPLICABLE)
    )
    assert result.posture is ExperimentPolicyReviewPosture.REVIEW_POLICY_INAPPLICABLE
