from dataclasses import dataclass
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
    budget_min: float | None = None
    budget_max: float | None = None
    opportunity_type: OpportunityType = OpportunityType.FREELANCE
