from datetime import datetime

from .evidence_decision_context import EvidenceDecisionContext
from .evidence_decision_record import (
    DecisionOutcome,
    EvidenceDecisionRecord,
)


def record_evidence_decision(
    *,
    context: EvidenceDecisionContext,
    record_id: str,
    outcome: DecisionOutcome,
    statement: str,
    rationale: str,
    decision_maker_id: str,
    decided_at: datetime,
) -> EvidenceDecisionRecord:
    evidence_ids = _unique_in_order(
        context.source_references
        + context.statistical_observation_ids
        + context.current_observation_ids
        + context.baseline_observation_ids
    )

    return EvidenceDecisionRecord(
        id=record_id,
        business_id=context.business_id,
        outcome=outcome,
        statement=statement,
        rationale=rationale,
        evidence_ids=evidence_ids,
        decided_at=decided_at,
        decision_maker_id=decision_maker_id,
    )


def _unique_in_order(values: tuple[str, ...]) -> tuple[str, ...]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value not in seen:
            seen.add(value)
            result.append(value)
    return tuple(result)
