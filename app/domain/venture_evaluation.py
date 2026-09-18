from dataclasses import dataclass
from enum import Enum

from app.domain.evidence import Evidence


class VentureCriterion(Enum):
    MARKET_DEMAND = "MARKET_DEMAND"
    MARKET_SIZE = "MARKET_SIZE"
    COMPETITION = "COMPETITION"
    CAPITAL_REQUIREMENT = "CAPITAL_REQUIREMENT"
    TIME_TO_REVENUE = "TIME_TO_REVENUE"
    RECURRING_REVENUE_POTENTIAL = "RECURRING_REVENUE_POTENTIAL"
    AUTOMATION_POTENTIAL = "AUTOMATION_POTENTIAL"
    SCALABILITY = "SCALABILITY"
    RISK = "RISK"
    EVIDENCE_QUALITY = "EVIDENCE_QUALITY"
    STRATEGIC_FIT = "STRATEGIC_FIT"
    EXIT_EXPANSION_POTENTIAL = "EXIT_EXPANSION_POTENTIAL"


class VentureCriterionOutcome(Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    INSUFFICIENT_DATA = "INSUFFICIENT_DATA"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class VentureOverallOutcome(Enum):
    QUALIFIED = "QUALIFIED"
    NOT_QUALIFIED = "NOT_QUALIFIED"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"


@dataclass(frozen=True)
class VentureCriterionEvaluation:
    outcome: VentureCriterionOutcome
    evidence: tuple[Evidence, ...] = ()


@dataclass(frozen=True)
class VentureEvaluation:
    criteria: dict[VentureCriterion, VentureCriterionEvaluation]

    @property
    def overall_outcome(self) -> VentureOverallOutcome:
        if not self.criteria:
            return VentureOverallOutcome.REVIEW_REQUIRED

        outcomes = [criterion.outcome for criterion in self.criteria.values()]

        if VentureCriterionOutcome.FAIL in outcomes:
            return VentureOverallOutcome.NOT_QUALIFIED

        if VentureCriterionOutcome.INSUFFICIENT_DATA in outcomes:
            return VentureOverallOutcome.REVIEW_REQUIRED

        return VentureOverallOutcome.QUALIFIED
