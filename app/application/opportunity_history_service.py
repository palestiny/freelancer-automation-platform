"""Application use case for evaluating the exact persisted opportunity revision."""

from __future__ import annotations

from datetime import datetime

from app.application.opportunity_decision_pipeline import (
    OpportunityDecisionPipeline,
    OpportunityDecisionResult,
)
from app.application.opportunity_history_repository import (
    OpportunityDecisionRecord,
    OpportunityHistoryRepository,
)
from app.domain.opportunity_intelligence import EvaluationPolicy
from app.domain.opportunity_prioritization import PrioritizationPolicy


class OpportunityHistoryService:
    """Coordinates persisted input lineage, decision creation, and immutable history."""

    def __init__(
        self,
        repository: OpportunityHistoryRepository,
        pipeline: OpportunityDecisionPipeline,
    ) -> None:
        if not callable(getattr(repository, "get_opportunity_revision", None)):
            raise TypeError("repository must provide get_opportunity_revision()")
        if not callable(getattr(repository, "save_decision", None)):
            raise TypeError("repository must provide save_decision()")
        if not callable(getattr(pipeline, "run", None)):
            raise TypeError("pipeline must provide run()")
        self._repository = repository
        self._pipeline = pipeline

    def evaluate_revision(
        self,
        *,
        decision_id: str,
        opportunity_id: str,
        revision_id: str,
        evaluation_ref: str,
        evaluation_policy: EvaluationPolicy,
        prioritization_policy: PrioritizationPolicy,
        evaluated_at: datetime,
    ) -> OpportunityDecisionRecord:
        revision = self._repository.get_opportunity_revision(
            opportunity_id, revision_id
        )
        result = self._pipeline.run(
            opportunity=revision.opportunity,
            evaluation_policy=evaluation_policy,
            prioritization_policy=prioritization_policy,
            opportunity_ref=opportunity_id,
            evaluation_ref=evaluation_ref,
            evaluated_at=evaluated_at,
        )
        if not isinstance(result, OpportunityDecisionResult):
            raise TypeError("pipeline must return an OpportunityDecisionResult")
        return self._repository.save_decision(
            decision_id,
            opportunity_id,
            revision_id,
            evaluation_policy,
            prioritization_policy,
            result,
        )
