from dataclasses import dataclass
from enum import Enum

from app.domain.business_model import BusinessModelHypothesis
from app.domain.opportunity_type import OpportunityType


class VentureStage(Enum):
    DISCOVERED = "DISCOVERED"
    RESEARCHING = "RESEARCHING"
    THESIS_CREATED = "THESIS_CREATED"
    ECONOMICALLY_EVALUATED = "ECONOMICALLY_EVALUATED"
    VALIDATION_REQUIRED = "VALIDATION_REQUIRED"
    MVP = "MVP"
    EARLY_REVENUE = "EARLY_REVENUE"
    PROVEN = "PROVEN"
    SCALE = "SCALE"
    KILLED = "KILLED"


_ALLOWED_TRANSITIONS: dict[VentureStage, frozenset[VentureStage]] = {
    VentureStage.DISCOVERED: frozenset({VentureStage.RESEARCHING, VentureStage.KILLED}),
    VentureStage.RESEARCHING: frozenset({VentureStage.THESIS_CREATED, VentureStage.KILLED}),
    VentureStage.THESIS_CREATED: frozenset(
        {VentureStage.ECONOMICALLY_EVALUATED, VentureStage.KILLED}
    ),
    VentureStage.ECONOMICALLY_EVALUATED: frozenset(
        {VentureStage.VALIDATION_REQUIRED, VentureStage.KILLED}
    ),
    VentureStage.VALIDATION_REQUIRED: frozenset({VentureStage.MVP, VentureStage.KILLED}),
    VentureStage.MVP: frozenset({VentureStage.EARLY_REVENUE, VentureStage.KILLED}),
    VentureStage.EARLY_REVENUE: frozenset({VentureStage.PROVEN, VentureStage.KILLED}),
    VentureStage.PROVEN: frozenset({VentureStage.SCALE, VentureStage.KILLED}),
    VentureStage.SCALE: frozenset(),
    VentureStage.KILLED: frozenset(),
}


@dataclass
class Venture:
    id: str
    name: str
    opportunity_type: OpportunityType
    stage: VentureStage = VentureStage.DISCOVERED
    business_models: tuple[BusinessModelHypothesis, ...] = ()

    def advance_to(self, target: VentureStage) -> None:
        if target not in _ALLOWED_TRANSITIONS[self.stage]:
            raise ValueError(
                f"Invalid venture transition: {self.stage.value} -> {target.value}"
            )

        self.stage = target
