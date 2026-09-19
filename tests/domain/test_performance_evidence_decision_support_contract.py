from app.domain.performance_evidence_decision_support import CombinedEvidencePosture, DescriptiveDirection, InferentialStatus, PerformanceEvidenceDecisionSupport
import pytest

def make():
    return dict(business_id='b1', metric_name='profit', unit='EGP', descriptive_direction=DescriptiveDirection.IMPROVING, inferential_status=InferentialStatus.UNAVAILABLE, posture=CombinedEvidencePosture.INFERENTIAL_EVIDENCE_UNAVAILABLE, statistical_observation_ids=('a',))

def test_rejects_empty_identity():
    with pytest.raises(ValueError): PerformanceEvidenceDecisionSupport(**{**make(), 'business_id': ''})

def test_rejects_duplicate_lineage():
    with pytest.raises(ValueError): PerformanceEvidenceDecisionSupport(**{**make(), 'statistical_observation_ids': ('a','a')})

def test_rejects_empty_lineage():
    with pytest.raises(ValueError): PerformanceEvidenceDecisionSupport(**{**make(), 'statistical_observation_ids': ()})
