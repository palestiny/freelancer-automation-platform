from datetime import datetime, timezone

from app.application.marketplace_opportunity_adapter import (
    OpportunityDiscoveryCriteria,
    ProviderFailureCode,
)
from app.infrastructure.freelancer_sandbox_opportunity_adapter import (
    FreelancerSandboxOpportunityAdapter,
)


def _adapter(result, resolver=None):
    return FreelancerSandboxOpportunityAdapter(
        credential_ref="credential://freelancer/sandbox",
        credential_resolver=resolver or (lambda _: "opaque-token"),
        project_searcher=lambda **_: result,
        page_size=2,
    )


def test_maps_freelancer_projects_to_provider_neutral_observations():
    result = {
        "projects": [
            {"id": 101, "title": "React dashboard", "description": "Build UI"},
            {"id": 102, "title": "API integration", "description": None},
        ],
        "total_count": 2,
    }

    mapped = _adapter(result).discover_opportunities(
        OpportunityDiscoveryCriteria(query="react")
    )

    assert mapped.provider_key == "freelancer_sandbox"
    assert [item.external_opportunity_id for item in mapped.observations] == [
        "101",
        "102",
    ]
    assert mapped.observations[0].title == "React dashboard"
    assert mapped.complete is True
    assert mapped.next_cursor is None


def test_exposes_next_cursor_when_more_projects_remain():
    result = {
        "projects": [
            {"id": 101, "title": "First", "description": "A"},
            {"id": 102, "title": "Second", "description": "B"},
        ],
        "total_count": 5,
    }

    mapped = _adapter(result).discover_opportunities(
        OpportunityDiscoveryCriteria(query="python")
    )

    assert mapped.complete is False
    assert mapped.next_cursor == "2"


def test_cursor_is_translated_to_provider_offset():
    calls = []

    def searcher(**kwargs):
        calls.append(kwargs)
        return {"projects": [{"id": 103, "title": "Third"}], "total_count": 3}

    adapter = FreelancerSandboxOpportunityAdapter(
        credential_ref="credential://freelancer/sandbox",
        credential_resolver=lambda _: "token",
        project_searcher=searcher,
        page_size=2,
    )

    mapped = adapter.discover_opportunities(
        OpportunityDiscoveryCriteria(query="python"),
        cursor="2",
    )

    assert calls == [{"token": "token", "query": "python", "limit": 2, "offset": 2}]
    assert mapped.complete is True
    assert mapped.observations[0].external_opportunity_id == "103"


def test_malformed_provider_payload_is_neutral_failure():
    mapped = _adapter({"projects": []}).discover_opportunities(
        OpportunityDiscoveryCriteria(query="python")
    )

    assert mapped.failure is not None
    assert mapped.failure.code is ProviderFailureCode.MALFORMED_RESPONSE
    assert mapped.observations == ()


def test_credential_resolution_failure_is_authentication_failure():
    adapter = _adapter(
        {"projects": [], "total_count": 0},
        resolver=lambda _: "",
    )

    mapped = adapter.discover_opportunities(
        OpportunityDiscoveryCriteria(query="python")
    )

    assert mapped.failure is not None
    assert mapped.failure.code is ProviderFailureCode.AUTHENTICATION_FAILURE


def test_provider_exception_does_not_become_retry_or_execution_command():
    def searcher(**_):
        raise RuntimeError("provider outage")

    adapter = FreelancerSandboxOpportunityAdapter(
        credential_ref="credential://freelancer/sandbox",
        credential_resolver=lambda _: "token",
        project_searcher=searcher,
    )

    mapped = adapter.discover_opportunities(
        OpportunityDiscoveryCriteria(query="python")
    )

    assert mapped.failure is not None
    assert mapped.failure.code is ProviderFailureCode.PROVIDER_UNAVAILABLE
    assert "retry" not in mapped.failure.message.lower()


def test_observation_timestamp_is_timezone_aware():
    result = {"projects": [{"id": 101, "title": "A"}], "total_count": 1}

    mapped = _adapter(result).discover_opportunities(
        OpportunityDiscoveryCriteria(query="python")
    )

    assert mapped.observed_at.tzinfo is not None
    assert mapped.observed_at.utcoffset() is not None
    assert isinstance(mapped.observed_at, datetime)
