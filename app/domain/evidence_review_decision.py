from dataclasses import dataclass
from enum import Enum

from .evidence_review_handoff import EvidenceReviewHandoff, ReviewTarget


class ReviewDecisionOutcome(str, Enum):
    ACCEPT = "accept"
    REJECT = "reject"
    REQUEST_MORE_EVIDENCE = "request_more_evidence"


@dataclass(frozen=True)
class EvidenceReviewDecision:
    business_id: str
    metric_name: str
    unit: str
    observation_ids: tuple[str, ...]
    target: ReviewTarget
    outcome: ReviewDecisionOutcome
    reviewer_id: str
    rationale: str
    authorized: bool = False

    def __post_init__(self) -> None:
        for name in ("business_id", "metric_name", "unit", "reviewer_id", "rationale"):
            if not getattr(self, name).strip():
                raise ValueError(f"{name} cannot be empty")
        if not self.observation_ids:
            raise ValueError("observation_ids cannot be empty")
        if len(set(self.observation_ids)) != len(self.observation_ids):
            raise ValueError("observation_ids must be unique")
        if not isinstance(self.target, ReviewTarget):
            raise TypeError("target must be a ReviewTarget")
        if not isinstance(self.outcome, ReviewDecisionOutcome):
            raise TypeError("outcome must be a ReviewDecisionOutcome")
        if self.authorized:
            raise ValueError("review decision cannot authorize execution or policy mutation")


def create_evidence_review_decision(
    *,
    handoff: EvidenceReviewHandoff,
    reviewer_id: str,
    outcome: ReviewDecisionOutcome,
    rationale: str,
) -> EvidenceReviewDecision:
    if not isinstance(handoff, EvidenceReviewHandoff):
        raise TypeError("handoff must be an EvidenceReviewHandoff")
    if not isinstance(outcome, ReviewDecisionOutcome):
        raise TypeError("outcome must be a ReviewDecisionOutcome")
    return EvidenceReviewDecision(
        business_id=handoff.business_id,
        metric_name=handoff.metric_name,
        unit=handoff.unit,
        observation_ids=handoff.observation_ids,
        target=handoff.target,
        outcome=outcome,
        reviewer_id=reviewer_id,
        rationale=rationale,
        authorized=False,
    )
