from datetime import datetime, timezone
from decimal import Decimal
import json
from pathlib import Path

import pytest

from app.application.marketplace_opportunity_adapter import ExternalOpportunityObservation
from app.application.opportunity_normalization import normalize_opportunity_observation


def _synthetic_observation() -> ExternalOpportunityObservation:
    fixture_path = Path(__file__).parents[1] / "fixtures" / "synthetic_opportunity_detail.json"
    payload = json.loads(fixture_path.read_text(encoding="utf-8"))["observation"]
    return ExternalOpportunityObservation(
        provider_key=payload["provider_key"],
        external_opportunity_id=payload["external_opportunity_id"],
        observed_at=datetime(2026, 9, 26, 10, 0, tzinfo=timezone.utc),
        title=payload["title"],
        description=payload["description"],
        project_type=payload["project_type"],
        status=payload["status"],
        budget_min=Decimal(payload["budget_min"]),
        budget_max=Decimal(payload["budget_max"]),
        budget_currency=payload["budget_currency"],
        pricing_model=payload["pricing_model"],
        required_capabilities=tuple(payload["required_capabilities"]),
        source_url=payload["source_url"],
        client_external_id=payload["client_external_id"],
        client_country=payload["client_country"],
    )


def test_normalizes_synthetic_provider_neutral_detail_contract():
    result = normalize_opportunity_observation(_synthetic_observation())

    assert result.project_type == "FIXED"
    assert result.status == "OPEN"
    assert result.budget_min == Decimal("100.00")
    assert result.budget_max == Decimal("250.00")
    assert result.budget_currency == "USD"
    assert result.pricing_model == "FIXED"
    assert result.required_capabilities == frozenset({"react", "javascript"})
    assert result.source_url == "https://example.test/opportunities/synthetic-001"
    assert result.client_external_id == "client-synthetic-001"
    assert result.client_country == "EG"


def test_optional_detail_fields_remain_unavailable_when_not_observed():
    observation = ExternalOpportunityObservation(
        provider_key="example_marketplace",
        external_opportunity_id="synthetic-002",
        observed_at=datetime(2026, 9, 26, 10, 0, tzinfo=timezone.utc),
        title="Minimal opportunity",
        description="Description",
    )

    result = normalize_opportunity_observation(observation)

    assert result.project_type is None
    assert result.budget_min is None
    assert result.budget_max is None
    assert result.budget_currency is None
    assert result.required_capabilities == frozenset()
    assert result.source_url is None


def test_observation_rejects_non_decimal_budget():
    with pytest.raises(TypeError, match="budget_min"):
        ExternalOpportunityObservation(
            provider_key="example_marketplace",
            external_opportunity_id="synthetic-003",
            observed_at=datetime(2026, 9, 26, 10, 0, tzinfo=timezone.utc),
            title="Opportunity",
            description="Description",
            budget_min=100.0,
        )


def test_observation_rejects_empty_capability():
    with pytest.raises(ValueError, match="required_capabilities"):
        ExternalOpportunityObservation(
            provider_key="example_marketplace",
            external_opportunity_id="synthetic-004",
            observed_at=datetime(2026, 9, 26, 10, 0, tzinfo=timezone.utc),
            title="Opportunity",
            description="Description",
            required_capabilities=("react", ""),
        )
