from app.application.marketplace_opportunity_adapter import (
    ExternalOpportunityObservation,
)
from app.domain.opportunity import Opportunity
from app.domain.opportunity_type import OpportunityType


def normalize_opportunity_observation(
    observation: ExternalOpportunityObservation,
) -> Opportunity:
    if observation.title is None or observation.description is None:
        raise ValueError(
            "title and description are required to create a domain Opportunity"
        )

    return Opportunity(
        source_platform=observation.provider_key,
        source_opportunity_id=observation.external_opportunity_id,
        title=observation.title,
        description=observation.description,
        project_type=observation.project_type,
        required_capabilities=frozenset(observation.required_capabilities),
        budget_min=observation.budget_min,
        budget_max=observation.budget_max,
        budget_currency=observation.budget_currency,
        pricing_model=observation.pricing_model,
        status=observation.status,
        source_url=observation.source_url,
        client_external_id=observation.client_external_id,
        client_country=observation.client_country,
        opportunity_type=OpportunityType.FREELANCE,
    )
