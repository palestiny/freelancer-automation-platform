"""Provider-neutral repository port for immutable opportunity history."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Protocol

from app.application.opportunity_decision_pipeline import OpportunityDecisionResult
from app.domain.opportunity import Opportunity
from app.domain.opportunity_intelligence import EvaluationPolicy
from app.domain.opportunity_prioritization import PrioritizationPolicy


class RecordConflict(ValueError):
    """An existing caller-owned identity was reused for different content."""


class RecordNotFound(LookupError):
    """A requested immutable history record does not exist."""


@dataclass(frozen=True)
class OpportunityRevisionRecord:
    opportunity_id: str
    revision_id: str
    opportunity: Opportunity
    recorded_at: datetime


@dataclass(frozen=True)
class OpportunityDecisionRecord:
    decision_id: str
    opportunity_id: str
    revision_id: str
    evaluation_policy: EvaluationPolicy
    prioritization_policy: PrioritizationPolicy
    result: OpportunityDecisionResult
    recorded_at: datetime


class OpportunityHistoryRepository(Protocol):
    """Single-record immutable persistence contract; no transaction claim."""

    def save_opportunity_revision(
        self, opportunity_id: str, revision_id: str, opportunity: Opportunity
    ) -> OpportunityRevisionRecord: ...

    def get_opportunity_revision(
        self, opportunity_id: str, revision_id: str
    ) -> OpportunityRevisionRecord: ...

    def list_opportunity_revisions(
        self, opportunity_id: str
    ) -> tuple[OpportunityRevisionRecord, ...]: ...

    def get_latest_opportunity_revision(
        self, opportunity_id: str
    ) -> OpportunityRevisionRecord: ...

    def save_decision(
        self,
        decision_id: str,
        opportunity_id: str,
        revision_id: str,
        evaluation_policy: EvaluationPolicy,
        prioritization_policy: PrioritizationPolicy,
        result: OpportunityDecisionResult,
    ) -> OpportunityDecisionRecord: ...

    def get_decision(self, decision_id: str) -> OpportunityDecisionRecord: ...

    def list_decisions(
        self, opportunity_id: str
    ) -> tuple[OpportunityDecisionRecord, ...]: ...
