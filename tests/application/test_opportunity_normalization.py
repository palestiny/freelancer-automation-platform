from datetime import datetime, timezone

from app.application.marketplace_opportunity_adapter import (
    ExternalOpportunityObservation,
)
from app.application.opportunity_normalization import (
    normalize_opportunity_observation,
)
from app.domain.opportunity import Opportunity
from app.domain.opportunity_type import OpportunityType


def test_normalizes_provider_observation_into_domain_opportunity():
    observed_at = datetime(2026, 9, 25, 10, 0, tzinfo=timezone.utc)
    observation = ExternalOpportunityObservation(
        provider_key="freelancer_sandbox",
        external_opportunity_id="123",
        observed_at=observed_at,
        title="Build a React dashboard",
        description="Create a responsive dashboard.",
    )

    result = normalize_opportunity_observation(observation)

    assert result == Opportunity(
        source_platform="freelancer_sandbox",
        source_opportunity_id="123",
        title="Build a React dashboard",
        description="Create a responsive dashboard.",
        opportunity_type=OpportunityType.FREELANCE,
    )


def test_normalization_does_not_invent_missing_provider_fields():
    observation = ExternalOpportunityObservation(
        provider_key="freelancer_sandbox",
        external_opportunity_id="456",
        observed_at=datetime(2026, 9, 25, 10, 0, tzinfo=timezone.utc),
        title=None,
        description=None,
    )

    result = normalize_opportunity_observation(observation)

    assert result.title == ""
    assert result.description == ""
    assert result.project_type is None
    assert result.required_capabilities == frozenset()
    assert result.budget_min is None
    assert result.budget_max is None
