from dataclasses import fields

from app.application.history_aware_execution_coordinator import HistoryAwareExecutionCoordinationResult
from app.domain.execution_outcome import ExecutionOutcome
from app.domain.execution_outcome_policy import ExecutionOutcomeAssessment
from app.domain.execution_recovery import ExecutionRecoveryHandoff


def test_history_aware_result_contract_uses_concrete_domain_types():
    annotations = HistoryAwareExecutionCoordinationResult.__annotations__

    assert annotations["outcome"] is ExecutionOutcome
    assert annotations["policy_assessment"] is ExecutionOutcomeAssessment
    assert annotations["recovery_handoff"] is ExecutionRecoveryHandoff


def test_history_aware_result_contains_only_immutable_coordination_outputs():
    names = tuple(field.name for field in fields(HistoryAwareExecutionCoordinationResult))
    assert names == ("outcome", "history", "policy_assessment", "recovery_handoff")
