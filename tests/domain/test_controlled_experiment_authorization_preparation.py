from app.domain.action_authorization import ActionClass, AutonomyLevel
from app.domain.controlled_experiment_authorization_preparation import (
    prepare_experiment_authorization_request,
)
from app.domain.controlled_experiment_hypothesis_policy import HypothesisPolicyOutcome
from app.domain.controlled_experiment_policy_review_decision import (
    ExperimentPolicyReviewDecisionOutcome,
)
from tests.domain.test_controlled_experiment_policy_review_decision import _handoff
from app.domain.controlled_experiment_policy_review_decision import create_experiment_policy_review_decision


def _decision(outcome):
    return create_experiment_policy_review_decision(
        handoff=_handoff(HypothesisPolicyOutcome.SUPPORTS_HYPOTHESIS),
        reviewer_id="reviewer-1",
        outcome=outcome,
        rationale="Reviewed evidence.",
    )


def test_accept_creates_non_authorizing_request():
    result = prepare_experiment_authorization_request(
        decision=_decision(ExperimentPolicyReviewDecisionOutcome.ACCEPT),
        policy_id="experiment-policy",
        policy_version="1",
        action_class=ActionClass.REVERSIBLE_EXTERNAL,
        requested_autonomy=AutonomyLevel.L3_EXECUTE_WITH_APPROVAL,
    )
    assert result.experiment_id == "exp-1"
    assert result.policy_id == "experiment-policy"
    assert result.requested_autonomy is AutonomyLevel.L3_EXECUTE_WITH_APPROVAL
    assert result.observation_ids == ("a", "b")


def test_reject_cannot_create_authorization_request():
    import pytest

    with pytest.raises(ValueError, match="accepted review decision"):
        prepare_experiment_authorization_request(
            decision=_decision(ExperimentPolicyReviewDecisionOutcome.REJECT),
            policy_id="experiment-policy",
            policy_version="1",
            action_class=ActionClass.REVERSIBLE_EXTERNAL,
            requested_autonomy=AutonomyLevel.L3_EXECUTE_WITH_APPROVAL,
        )


def test_more_evidence_cannot_create_authorization_request():
    import pytest

    with pytest.raises(ValueError, match="accepted review decision"):
        prepare_experiment_authorization_request(
            decision=_decision(ExperimentPolicyReviewDecisionOutcome.REQUEST_MORE_EVIDENCE),
            policy_id="experiment-policy",
            policy_version="1",
            action_class=ActionClass.REVERSIBLE_EXTERNAL,
            requested_autonomy=AutonomyLevel.L2_PREPARE,
        )
