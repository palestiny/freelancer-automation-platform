from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Callable, Protocol

from app.application.marketplace_opportunity_adapter import (
    ExternalOpportunityObservation,
    MarketplaceOpportunityAdapter,
    OpportunityDiscoveryCriteria,
    OpportunityDiscoveryResult,
    ProviderFailure,
    ProviderFailureCode,
)


class FreelancerCredentialResolver(Protocol):
    def __call__(self, credential_ref: str) -> str:
        """Resolve an opaque credential reference to a short-lived OAuth token."""


class FreelancerProjectSearcher(Protocol):
    def __call__(
        self,
        *,
        token: str,
        query: str,
        limit: int,
        offset: int,
    ) -> Any:
        """Return the provider SDK search result without exposing it to the domain."""


def _sdk_project_searcher(*, token: str, query: str, limit: int, offset: int) -> Any:
    from freelancersdk.resources.projects.projects import search_projects
    from freelancersdk.resources.projects.helpers import (
        create_get_projects_project_details_object,
        create_search_projects_filter,
        create_get_projects_user_details_object,
    )
    from freelancersdk.session import Session

    session = Session(
        oauth_token=token,
        url="https://www.freelancer-sandbox.com",
    )
    return search_projects(
        session,
        query=query,
        search_filter=create_search_projects_filter(),
        project_details=create_get_projects_project_details_object(
            full_description=True,
            jobs=True,
            qualifications=True,
        ),
        user_details=create_get_projects_user_details_object(
            basic=True,
        ),
        limit=limit,
        offset=offset,
    )


class FreelancerSandboxOpportunityAdapter(MarketplaceOpportunityAdapter):
    """Read-only Freelancer.com Sandbox opportunity adapter.

    Provider SDK objects remain inside this infrastructure adapter. The
    application boundary receives only provider-neutral observations.
    """

    provider_key = "freelancer_sandbox"

    def __init__(
        self,
        credential_ref: str,
        credential_resolver: FreelancerCredentialResolver,
        *,
        project_searcher: FreelancerProjectSearcher = _sdk_project_searcher,
        page_size: int = 10,
    ) -> None:
        if not credential_ref.strip():
            raise ValueError("credential_ref cannot be empty")
        if page_size <= 0:
            raise ValueError("page_size must be positive")
        self._credential_ref = credential_ref
        self._credential_resolver = credential_resolver
        self._project_searcher = project_searcher
        self._page_size = page_size

    def discover_opportunities(
        self,
        criteria: OpportunityDiscoveryCriteria,
        cursor: str | None = None,
    ) -> OpportunityDiscoveryResult:
        observed_at = datetime.now(timezone.utc)
        query = criteria.query or ""
        offset = self._parse_cursor(cursor)

        try:
            token = self._credential_resolver(self._credential_ref)
            if not token:
                raise ValueError("credential resolver returned an empty token")
            raw_result = self._project_searcher(
                token=token,
                query=query,
                limit=self._page_size,
                offset=offset,
            )
            return self._map_result(raw_result, observed_at, offset)
        except ValueError as exc:
            return OpportunityDiscoveryResult(
                provider_key=self.provider_key,
                observed_at=observed_at,
                observations=(),
                complete=True,
                failure=ProviderFailure(
                    ProviderFailureCode.AUTHENTICATION_FAILURE,
                    str(exc),
                ),
            )
        except Exception as exc:
            # The provider SDK currently exposes provider search failures as a
            # generic ProjectsNotFoundException. Do not infer finer-grained
            # provider error semantics that the SDK does not expose here.
            return OpportunityDiscoveryResult(
                provider_key=self.provider_key,
                observed_at=observed_at,
                observations=(),
                complete=True,
                failure=ProviderFailure(
                    ProviderFailureCode.PROVIDER_UNAVAILABLE,
                    type(exc).__name__,
                ),
            )

    def _map_result(
        self,
        raw_result: Any,
        observed_at: datetime,
        offset: int,
    ) -> OpportunityDiscoveryResult:
        if not isinstance(raw_result, dict):
            return self._malformed_result(observed_at, "result must be an object")

        projects = raw_result.get("projects")
        total_count = raw_result.get("total_count")
        if not isinstance(projects, list) or not isinstance(total_count, int):
            return self._malformed_result(
                observed_at,
                "result must contain projects and integer total_count",
            )

        observations: list[ExternalOpportunityObservation] = []
        for project in projects:
            if not isinstance(project, dict):
                return self._malformed_result(
                    observed_at,
                    "project entry must be an object",
                )
            project_id = project.get("id")
            if project_id is None:
                return self._malformed_result(
                    observed_at,
                    "project entry is missing id",
                )
            title = project.get("title")
            description = project.get("description")
            if title is not None and not isinstance(title, str):
                return self._malformed_result(
                    observed_at,
                    "project title must be a string or null",
                )
            if description is not None and not isinstance(description, str):
                return self._malformed_result(
                    observed_at,
                    "project description must be a string or null",
                )

            project_type, error = self._extract_project_type(project)
            if error is not None:
                return self._malformed_result(observed_at, error)

            budget_min, budget_max, error = self._extract_budget(project)
            if error is not None:
                return self._malformed_result(observed_at, error)

            required_capabilities, error = self._extract_required_capabilities(project)
            if error is not None:
                return self._malformed_result(observed_at, error)

            observations.append(
                ExternalOpportunityObservation(
                    provider_key=self.provider_key,
                    external_opportunity_id=str(project_id),
                    observed_at=observed_at,
                    title=title,
                    description=description,
                    project_type=project_type,
                    budget_min=budget_min,
                    budget_max=budget_max,
                    required_capabilities=required_capabilities,
                )
            )

        next_offset = offset + len(observations)
        complete = next_offset >= total_count
        next_cursor = None if complete else str(next_offset)
        return OpportunityDiscoveryResult(
            provider_key=self.provider_key,
            observed_at=observed_at,
            observations=tuple(observations),
            next_cursor=next_cursor,
            complete=complete,
        )

    @staticmethod
    def _extract_project_type(project: dict) -> tuple[str | None, str | None]:
        project_type = project.get("type")
        if project_type is None:
            return None, None
        if not isinstance(project_type, str):
            return None, "project type must be a string or null"
        return project_type, None

    @staticmethod
    def _extract_budget(project: dict) -> tuple[float | None, float | None, str | None]:
        budget = project.get("budget")
        if budget is None:
            return None, None, None
        if not isinstance(budget, dict):
            return None, None, "project budget must be an object or null"

        minimum = budget.get("minimum")
        maximum = budget.get("maximum")
        for value in (minimum, maximum):
            if value is not None and not isinstance(value, (int, float)):
                return None, None, "project budget minimum/maximum must be numbers or null"
        return minimum, maximum, None

    @staticmethod
    def _extract_required_capabilities(project: dict) -> tuple[frozenset[str], str | None]:
        jobs = project.get("jobs")
        if jobs is None:
            return frozenset(), None
        if not isinstance(jobs, list):
            return frozenset(), "project jobs must be a list or null"

        capabilities: set[str] = set()
        for job in jobs:
            if not isinstance(job, dict):
                return frozenset(), "project job entry must be an object"
            name = job.get("name")
            if not isinstance(name, str) or not name.strip():
                return frozenset(), "project job entry must have a non-empty name"
            capabilities.add(name)
        return frozenset(capabilities), None

    @staticmethod
    def _parse_cursor(cursor: str | None) -> int:
        if cursor is None:
            return 0
        try:
            offset = int(cursor)
        except (TypeError, ValueError) as exc:
            raise ValueError("cursor must be a non-negative integer") from exc
        if offset < 0:
            raise ValueError("cursor must be a non-negative integer")
        return offset

    def _malformed_result(
        self,
        observed_at: datetime,
        message: str,
    ) -> OpportunityDiscoveryResult:
        return OpportunityDiscoveryResult(
            provider_key=self.provider_key,
            observed_at=observed_at,
            observations=(),
            complete=True,
            failure=ProviderFailure(
                ProviderFailureCode.MALFORMED_RESPONSE,
                message,
            ),
        )
