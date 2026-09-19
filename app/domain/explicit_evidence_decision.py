from dataclasses import dataclass
from datetime import datetime
from enum import Enum

class DecisionOutcome(str, Enum):
    ACCEPT="accept"
    REJECT="reject"
    DEFER="defer"

@dataclass(frozen=True)
class ExplicitEvidenceDecision:
    decision_id:str
    business_id:str
    outcome:DecisionOutcome
    evidence_context:str
    evidence_observation_ids:tuple[str,...]
    decided_at:datetime
    rationale:str

    def __post_init__(self)->None:
        for name in ("decision_id","business_id","evidence_context","rationale"):
            if not getattr(self,name).strip(): raise ValueError(f"{name} cannot be empty")
        if not self.evidence_observation_ids: raise ValueError("evidence_observation_ids cannot be empty")
        if len(set(self.evidence_observation_ids)) != len(self.evidence_observation_ids): raise ValueError("evidence_observation_ids must be unique")
        if any(not item.strip() for item in self.evidence_observation_ids): raise ValueError("evidence observation ids cannot be empty")
