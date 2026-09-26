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
        opportunity_type=OpportunityType.FREELANCE,
    )
