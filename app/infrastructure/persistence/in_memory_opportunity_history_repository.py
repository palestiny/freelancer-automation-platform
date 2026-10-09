"""In-memory reference adapter for the opportunity history repository contract.

This adapter is for deterministic contract tests and local composition only. It does
not claim crash durability, cross-process linearizability, or distributed locking.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Callable

from app.application.opportunity_decision_pipeline import OpportunityDecisionResult
from app.application.opportunity_history_repository import (
    OpportunityDecisionRecord,
    OpportunityHistoryRepository,
    OpportunityRevisionRecord,
    RecordConflict,
    RecordNotFound,
)
from app.domain.opportunity import Opportunity
from app.domain.opportunity_intelligence import EvaluationPolicy
from app.domain.opportunity_prioritization import PrioritizationPolicy
from app.infrastructure.persistence.opportunity_history_codec import (
    OpportunityHistoryCodecV1,
)


class InMemoryOpportunityHistoryRepository:
    """Small reference adapter implementing single-process immutable semantics."""

    def __init__(
        self,
        *,
        clock: Callable[[], datetime] | None = None,
        codec: OpportunityHistoryCodecV1 | None = None,
    ) -> None:
        self._clock = clock or (lambda: datetime.now(timezone.utc))
        self._codec = codec or OpportunityHistoryCodecV1()
        self._revisions: dict[tuple[str, str], OpportunityRevisionRecord] = {}
        self._decisions: dict[str, OpportunityDecisionRecord] = {}

    @staticmethod
    def _validate_identity(name: str, value: str) -> None:
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{name} must be a non-blank string")

    def _recorded_at(self) -> datetime:
        value = self._clock()
        if not isinstance(value, datetime) or value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("repository clock must return a timezone-aware datetime")
        return value.astimezone(timezone.utc)

    def save_opportunity_revision(
        self, opportunity_id: str, revision_id: str, opportunity: Opportunity
    ) -> OpportunityRevisionRecord:
        self._validate_identity("opportunity_id", opportunity_id)
        self._validate_identity("revision_id", revision_id)
        if not isinstance(opportunity, Opportunity):
            raise TypeError("opportunity must be an Opportunity")
        canonical_opportunity = self._codec.dumps(opportunity)
        key = (opportunity_id, revision_id)
        existing = self._revisions.get(key)
        if existing is not None:
            if self._codec.dumps(existing.opportunity) != canonical_opportunity:
                raise RecordConflict(
                    "revision identity already exists with different canonical content"
                )
            return existing
        record = OpportunityRevisionRecord(
            opportunity_id=opportunity_id,
            revision_id=revision_id,
            opportunity=opportunity,
            recorded_at=self._recorded_at(),
        )
        self._revisions[key] = record
        return record

    def get_opportunity_revision(
        self, opportunity_id: str, revision_id: str
    ) -> OpportunityRevisionRecord:
        self._validate_identity("opportunity_id", opportunity_id)
        self._validate_identity("revision_id", revision_id)
        try:
            return self._revisions[(opportunity_id, revision_id)]
        except KeyError as exc:
            raise RecordNotFound(
                f"opportunity revision not found: {opportunity_id}/{revision_id}"
            ) from exc

    def list_opportunity_revisions(
        self, opportunity_id: str
    ) -> tuple[OpportunityRevisionRecord, ...]:
        self._validate_identity("opportunity_id", opportunity_id)
        records = [
            record for (parent_id, _), record in self._revisions.items()
            if parent_id == opportunity_id
        ]
        return tuple(sorted(records, key=lambda item: (item.recorded_at, item.revision_id)))

    def get_latest_opportunity_revision(
        self, opportunity_id: str
    ) -> OpportunityRevisionRecord:
        history = self.list_opportunity_revisions(opportunity_id)
        if not history:
            raise RecordNotFound(f"opportunity has no recorded revisions: {opportunity_id}")
        return history[-1]

    def save_decision(
        self,
        decision_id: str,
        opportunity_id: str,
        revision_id: str,
        evaluation_policy: EvaluationPolicy,
        prioritization_policy: PrioritizationPolicy,
        result: OpportunityDecisionResult,
    ) -> OpportunityDecisionRecord:
        self._validate_identity("decision_id", decision_id)
        self._validate_identity("opportunity_id", opportunity_id)
        self._validate_identity("revision_id", revision_id)
        if not isinstance(evaluation_policy, EvaluationPolicy):
            raise TypeError("evaluation_policy must be an EvaluationPolicy")
        if not isinstance(prioritization_policy, PrioritizationPolicy):
            raise TypeError("prioritization_policy must be a PrioritizationPolicy")
        if not isinstance(result, OpportunityDecisionResult):
            raise TypeError("result must be an OpportunityDecisionResult")

        decision = result.priority_decision
        if result.opportunity_ref != opportunity_id or decision.opportunity_ref != opportunity_id:
            raise ValueError("decision opportunity lineage does not match opportunity_id")
        if result.evaluation_ref != decision.evaluation_ref:
            raise ValueError("decision evaluation lineage does not match result")
        if (
            result.evaluation.policy_id != evaluation_policy.policy_id
            or result.evaluation.policy_version != evaluation_policy.policy_version
            or decision.evaluation_policy_id != evaluation_policy.policy_id
            or decision.evaluation_policy_version != evaluation_policy.policy_version
        ):
            raise ValueError("evaluation policy identity/version mismatch")
        if (
            decision.prioritization_policy_id != prioritization_policy.policy_id
            or decision.prioritization_policy_version != prioritization_policy.policy_version
        ):
            raise ValueError("prioritization policy identity/version mismatch")

        logical_content = {
            "decision_id": decision_id,
            "opportunity_id": opportunity_id,
            "revision_id": revision_id,
            "evaluation_policy": evaluation_policy,
            "prioritization_policy": prioritization_policy,
            "result": result,
        }
        canonical_content = self._codec.dumps(logical_content)
        existing = self._decisions.get(decision_id)
        if existing is not None:
            existing_content = {
                "decision_id": existing.decision_id,
                "opportunity_id": existing.opportunity_id,
                "revision_id": existing.revision_id,
                "evaluation_policy": existing.evaluation_policy,
                "prioritization_policy": existing.prioritization_policy,
                "result": existing.result,
            }
            if self._codec.dumps(existing_content) != canonical_content:
                raise RecordConflict(
                    "decision identity already exists with different canonical content"
                )
            return existing

        self.get_opportunity_revision(opportunity_id, revision_id)
        record = OpportunityDecisionRecord(
            decision_id=decision_id,
            opportunity_id=opportunity_id,
            revision_id=revision_id,
            evaluation_policy=evaluation_policy,
            prioritization_policy=prioritization_policy,
            result=result,
            recorded_at=self._recorded_at(),
        )
        self._decisions[decision_id] = record
        return record

    def get_decision(self, decision_id: str) -> OpportunityDecisionRecord:
        self._validate_identity("decision_id", decision_id)
        try:
            return self._decisions[decision_id]
        except KeyError as exc:
            raise RecordNotFound(f"decision not found: {decision_id}") from exc

    def list_decisions(
        self, opportunity_id: str
    ) -> tuple[OpportunityDecisionRecord, ...]:
        self._validate_identity("opportunity_id", opportunity_id)
        records = [
            record for record in self._decisions.values()
            if record.opportunity_id == opportunity_id
        ]
        return tuple(sorted(records, key=lambda item: (item.recorded_at, item.decision_id)))
