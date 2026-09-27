from datetime import datetime, timezone

import pytest

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


def test_normalizes_project_type_budget_and_required_capabilities():
    observation = ExternalOpportunityObservation(
        provider_key="freelancer_sandbox",
        external_opportunity_id="789",
        observed_at=datetime(2026, 9, 25, 10, 0, tzinfo=timezone.utc),
        title="Build a React dashboard",
        description="Create a responsive dashboard.",
        project_type="fixed",
        budget_min=100,
        budget_max=500,
        required_capabilities=frozenset({"React", "CSS"}),
    )

    result = normalize_opportunity_observation(observation)

    assert result.project_type == "fixed"
    assert result.budget_min == 100
    assert result.budget_max == 500
    assert result.required_capabilities == frozenset({"React", "CSS"})


def test_normalization_rejects_missing_required_domain_content():
    observation = ExternalOpportunityObservation(
        provider_key="freelancer_sandbox",
        external_opportunity_id="456",
        observed_at=datetime(2026, 9, 25, 10, 0, tzinfo=timezone.utc),
        title=None,
        description=None,
    )

    with pytest.raises(ValueError, match="title and description"):
        normalize_opportunity_observation(observation)
