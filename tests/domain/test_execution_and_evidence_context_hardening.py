import math
import pytest

from app.domain.action_authorization import ActionAuthorization, ActionAuthorizationStatus, ActionClass, AutonomyLevel
from app.domain.authorized_execution_request import AuthorizedExecutionRequest, ExecutionRequestStatus, prepare_execution_request
from app.domain.evidence_decision_context import EvidenceDecisionContext
from app.domain.performance_evidence_decision_support import CombinedEvidencePosture, DescriptiveDirection, InferentialStatus


def _authorization():
    return ActionAuthorization(policy_id="p1", policy_version="1", action_class=ActionClass.REVERSIBLE_EXTERNAL,
                               requested_autonomy=AutonomyLevel.L3_EXECUTE_WITH_APPROVAL,
                               maximum_autonomy=AutonomyLevel.L3_EXECUTE_WITH_APPROVAL,
                               status=ActionAuthorizationStatus.AUTHORIZED, requires_human_approval=False)


@pytest.mark.parametrize("field", ["request_id", "idempotency_key", "policy_id", "policy_version"])
def test_execution_request_rejects_non_string_identity(field):
    values = dict(request_id="r1", idempotency_key="idem", policy_id="p1", policy_version="1",
                  action_class=ActionClass.REVERSIBLE_EXTERNAL, autonomy_level=AutonomyLevel.L3_EXECUTE_WITH_APPROVAL,
                  status=ExecutionRequestStatus.PREPARED)
    values[field] = None
    with pytest.raises(ValueError):
        AuthorizedExecutionRequest(**values)


@pytest.mark.parametrize("value", ["", "   "])
def test_execution_request_rejects_blank_identity(value):
    with pytest.raises(ValueError):
        AuthorizedExecutionRequest(request_id=value, idempotency_key="idem", action_class=ActionClass.REVERSIBLE_EXTERNAL,
                                   autonomy_level=AutonomyLevel.L3_EXECUTE_WITH_APPROVAL, policy_id="p1",
                                   policy_version="1", status=ExecutionRequestStatus.PREPARED)


def _context(**overrides):
    values = dict(
        business_id="b1", metric_name="profit", unit="EGP",
        descriptive_direction=DescriptiveDirection.IMPROVING,
        inferential_status=InferentialStatus.STATISTICAL_DIFFERENCE_DETECTED,
        posture=CombinedEvidencePosture.DESCRIPTIVE_CHANGE_WITH_STATISTICAL_DETECTION,
        statistical_observation_ids=("s1",), current_observation_ids=("c1",),
        baseline_observation_ids=("b1o",), source_references=("trend:1",),
        current_evidence_quality=80.0, baseline_evidence_quality=75.0,
    )
    values.update(overrides)
    return EvidenceDecisionContext(**values)


@pytest.mark.parametrize("field", ["business_id", "metric_name", "unit"])
def test_evidence_context_rejects_non_string_identity(field):
    with pytest.raises(ValueError):
        _context(**{field: None})


@pytest.mark.parametrize("field", ["statistical_observation_ids", "current_observation_ids",
                                   "baseline_observation_ids", "source_references"])
def test_evidence_context_requires_tuple_lineage(field):
    with pytest.raises(TypeError):
        _context(**{field: ["x"]})


@pytest.mark.parametrize("field", ["current_evidence_quality", "baseline_evidence_quality"])
@pytest.mark.parametrize("value", [math.nan, math.inf, -math.inf])
def test_evidence_context_rejects_non_finite_quality(field, value):
    with pytest.raises(ValueError):
        _context(**{field: value})
