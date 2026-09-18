from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class DecisionOutcome(str, Enum):
    ACCEPT = "accept"
    REJECT = "reject"
    DEFER = "defer"


@dataclass(frozen=True)
class EvidenceDecisionRecord:
    id: str
    business_id: str
    outcome: DecisionOutcome
    statement: str
    rationale: str
    evidence_ids: tuple[str, ...]
    decided_at: datetime
    decision_maker_id: str

    def __post_init__(self) -> None:
        for name in (
            "id",
            "business_id",
            "statement",
            "rationale",
            "decision_maker_id",
        ):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} cannot be empty")

        if not isinstance(self.outcome, DecisionOutcome):
            raise TypeError("outcome must be a DecisionOutcome")

        if not self.evidence_ids:
            raise ValueError("evidence_ids cannot be empty")
        if any(not isinstance(value, str) or not value.strip() for value in self.evidence_ids):
            raise ValueError("evidence_ids must contain non-empty strings")
        if len(set(self.evidence_ids)) != len(self.evidence_ids):
            raise ValueError("evidence_ids must be unique")
