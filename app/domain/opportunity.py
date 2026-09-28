from dataclasses import dataclass
from decimal import Decimal
from typing import FrozenSet

from app.domain.opportunity_type import OpportunityType


@dataclass(frozen=True)
class Opportunity:
    source_platform: str
    source_opportunity_id: str
    title: str
    description: str
    project_type: str | None = None
    required_capabilities: FrozenSet[str] = frozenset()
    budget_min: Decimal | None = None
    budget_max: Decimal | None = None
    budget_currency: str | None = None
    pricing_model: str | None = None
    status: str | None = None
    source_url: str | None = None
    client_external_id: str | None = None
    client_country: str | None = None
    opportunity_type: OpportunityType = OpportunityType.FREELANCE
