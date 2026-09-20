from app.domain.controlled_experiment_hypothesis_policy import (
    ExperimentHypothesisDirection,
    HypothesisPolicyOutcome,
    ControlledExperimentHypothesisPolicyResult,
)
from app.domain.controlled_experiment_policy_review_handoff import (
    ExperimentPolicyReviewPosture,
    ExperimentPolicyReviewHandoff,
)
from app.domain.controlled_experiment_policy_review_decision import (
    ExperimentPolicyReviewDecisionOutcome,
    create_experiment_policy_review_decision,
)


def _handoff(outcome):
    return ExperimentPolicyReviewHandoff(
        handoff_id="handoff-1",
        experiment_id="exp-1",
        metric_name="revenue",
        direction=ExperimentHypothesisDirection.INCREASES,
        policy_outcome=outcome,
        posture={
            HypothesisPolicyOutcome.SUPPORTS_HYPOTHESIS: ExperimentPolicyReviewPosture.REVIEW_SUPPORTS_HYPOTHESIS,
            HypothesisPolicyOutcome.DOES_NOT_SUPPORT_HYPOTHESIS: ExperimentPolicyReviewPosture.REVIEW_DOES_NOT_SUPPORT_HYPOTHESIS,
            HypothesisPolicyOutcome.INSUFFICIENT_EVIDENCE: ExperimentPolicyReviewPosture.REVIEW_INSUFFICIENT_EVIDENCE,
            HypothesisPolicyOutcome.POLICY_INAPPLICABLE: ExperimentPolicyReviewPosture.REVIEW_POLICY_INAPPLICABLE,
        }[outcome],
        observation_ids=("a", "b"),
    )


def test_accept_is_review_only():
    result = create_experiment_policy_review_decision(
        handoff=_handoff(HypothesisPolicyOutcome.SUPPORTS_HYPOTHESIS),
        reviewer_id="reviewer-1",
        outcome=ExperimentPolicyReviewDecisionOutcome.ACCEPT,
        rationale="Evidence is sufficient for the stated hypothesis review.",
    )
    assert result.outcome is ExperimentPolicyReviewDecisionOutcome.ACCEPT
    assert result.policy_outcome is HypothesisPolicyOutcome.SUPPORTS_HYPOTHESIS
    assert result.authorized is False


def test_reject_is_preserved_without_mutation():
    result = create_experiment_policy_review_decision(
        handoff=_handoff(HypothesisPolicyOutcome.DOES_NOT_SUPPORT_HYPOTHESIS),
        reviewer_id="reviewer-1",
        outcome=ExperimentPolicyReviewDecisionOutcome.REJECT,
        rationale="Observed evidence does not support the stated direction.",
    )
    assert result.outcome is ExperimentPolicyReviewDecisionOutcome.REJECT
    assert result.observation_ids == ("a", "b")


def test_more_evidence_is_explicit():
    result = create_experiment_policy_review_decision(
        handoff=_handoff(HypothesisPolicyOutcome.INSUFFICIENT_EVIDENCE),
        reviewer_id="reviewer-1",
        outcome=ExperimentPolicyReviewDecisionOutcome.REQUEST_MORE_EVIDENCE,
        rationale="More observations are required.",
    )
    assert result.outcome is ExperimentPolicyReviewDecisionOutcome.REQUEST_MORE_EVIDENCE
