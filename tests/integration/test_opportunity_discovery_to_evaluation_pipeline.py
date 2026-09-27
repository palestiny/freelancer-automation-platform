"""End-to-end pipeline: Discover -> Normalize -> Evaluate.

This closes the first real slice of the Economic Opportunity OS loop for a
single opportunity, using only existing domain/application contracts (no new
concepts introduced). It wires:

  MarketplaceOpportunityAdapter (infrastructure)
    -> ExternalOpportunityObservation (application boundary)
    -> normalize_opportunity_observation (application)
    -> Opportunity (domain)
    -> OpportunityEvaluator (domain)
    -> OpportunityEvaluation (QUALIFIED / NOT_QUALIFIED / REVIEW_REQUIRED)

A fake project_searcher is injected in place of the real Freelancer SDK call,
mirroring the dependency-injection seam the adapter already exposes for
testing (see FreelancerProjectSearcher protocol). No provider credentials or
network access are required to run this test.
"""

from app.application.marketplace_opportunity_adapter import (
    OpportunityDiscoveryCriteria,
)
from app.application.opportunity_normalization import normalize_opportunity_observation
from app.domain.opportunity_evaluation import (
    EvaluationPolicy,
    OpportunityEvaluator,
    OverallOutcome,
)
from app.infrastructure.freelancer_sandbox_opportunity_adapter import (
    FreelancerSandboxOpportunityAdapter,
)


def _fake_project_searcher(*, token: str, query: str, limit: int, offset: int):
    assert token == "sandbox-token"
    return {
        "total_count": 1,
        "projects": [
            {
                "id": 42,
                "title": "Build a small automation script",
                "description": "Looking for a Python developer to automate a report.",
            }
        ],
    }


def _fake_project_searcher_with_full_fields(*, token: str, query: str, limit: int, offset: int):
    return {
        "total_count": 1,
        "projects": [
            {
                "id": 43,
                "title": "Build a React dashboard",
                "description": "Fixed-price React dashboard for an internal tool.",
                "type": "fixed",
                "budget": {"minimum": 200, "maximum": 800},
                "jobs": [{"id": 1, "name": "React"}, {"id": 2, "name": "CSS"}],
            }
        ],
    }


def _adapter() -> FreelancerSandboxOpportunityAdapter:
    return FreelancerSandboxOpportunityAdapter(
        credential_ref="sandbox-cred",
        credential_resolver=lambda ref: "sandbox-token",
        project_searcher=_fake_project_searcher,
    )


def test_discovered_opportunity_is_normalized_and_evaluated_as_review_required():
    adapter = _adapter()

    discovery = adapter.discover_opportunities(OpportunityDiscoveryCriteria(query="python"))

    assert discovery.failure is None
    assert discovery.complete is True
    assert len(discovery.observations) == 1

    observation = discovery.observations[0]
    assert observation.provider_key == "freelancer_sandbox"
    assert observation.external_opportunity_id == "42"

    opportunity = normalize_opportunity_observation(observation)
    assert opportunity.source_platform == "freelancer_sandbox"
    assert opportunity.source_opportunity_id == "42"
    assert opportunity.title == "Build a small automation script"

    # No project_type was supplied by the provider, and the policy requires
    # one to be known before it can allow/deny -- this is the honest,
    # currently-implemented outcome for real, incomplete marketplace data.
    policy = EvaluationPolicy(allowed_project_types=frozenset({"fixed"}))
    evaluation = OpportunityEvaluator().evaluate(opportunity, policy)

    assert evaluation.overall_outcome is OverallOutcome.REVIEW_REQUIRED
    assert evaluation.criteria["eligibility"].evidence == ("project_type is missing",)


def test_discovered_opportunity_qualifies_under_a_permissive_policy():
    adapter = _adapter()
    discovery = adapter.discover_opportunities(OpportunityDiscoveryCriteria(query="python"))
    opportunity = normalize_opportunity_observation(discovery.observations[0])

    # A policy that only depends on fields the provider actually returned
    # (title/description) should qualify the opportunity end-to-end.
    evaluation = OpportunityEvaluator().evaluate(opportunity, EvaluationPolicy())

    assert evaluation.overall_outcome is OverallOutcome.QUALIFIED


def test_full_provider_data_flows_through_to_a_real_policy_decision():
    """Regression test for the gap found while wiring this pipeline: provider
    project_type/budget/required_capabilities were being silently discarded
    at the observation boundary, so any policy depending on them could never
    receive real data and always fell back to REVIEW_REQUIRED."""
    adapter = FreelancerSandboxOpportunityAdapter(
        credential_ref="sandbox-cred",
        credential_resolver=lambda ref: "sandbox-token",
        project_searcher=_fake_project_searcher_with_full_fields,
    )

    discovery = adapter.discover_opportunities(OpportunityDiscoveryCriteria(query="react"))
    opportunity = normalize_opportunity_observation(discovery.observations[0])

    assert opportunity.project_type == "fixed"
    assert opportunity.budget_min == 200
    assert opportunity.budget_max == 800
    assert opportunity.required_capabilities == frozenset({"React", "CSS"})

    policy = EvaluationPolicy(
        allowed_project_types=frozenset({"fixed"}),
        required_capabilities=frozenset({"React"}),
        minimum_budget=150,
        maximum_budget=1000,
    )
    evaluation = OpportunityEvaluator().evaluate(opportunity, policy)

    assert evaluation.overall_outcome is OverallOutcome.QUALIFIED
