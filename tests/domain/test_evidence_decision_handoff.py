from app.domain.performance_evidence_decision_support import CombinedEvidencePosture, DescriptiveDirection, InferentialStatus, PerformanceEvidenceDecisionSupport
from app.domain.evidence_decision_handoff import EvidenceHandoffStatus, handoff_evidence_for_review

def _support(posture, inferential=InferentialStatus.STATISTICAL_DIFFERENCE_DETECTED):
    return PerformanceEvidenceDecisionSupport(business_id='b1', metric_name='profit', unit='EGP', descriptive_direction=DescriptiveDirection.IMPROVING, inferential_status=inferential, posture=posture, statistical_observation_ids=('a','b'))

def test_aligned_evidence_is_ready_for_review():
    assert handoff_evidence_for_review(_support(CombinedEvidencePosture.DESCRIPTIVE_AND_STATISTICAL_ALIGNMENT)).status is EvidenceHandoffStatus.READY_FOR_REVIEW

def test_change_without_statistical_detection_is_reviewable():
    r=handoff_evidence_for_review(_support(CombinedEvidencePosture.DESCRIPTIVE_CHANGE_WITHOUT_STATISTICAL_DETECTION, InferentialStatus.NO_STATISTICAL_DIFFERENCE_DETECTED))
    assert r.status is EvidenceHandoffStatus.READY_FOR_REVIEW

def test_missing_inferential_evidence_is_incomplete():
    r=handoff_evidence_for_review(_support(CombinedEvidencePosture.INFERENTIAL_EVIDENCE_UNAVAILABLE, InferentialStatus.UNAVAILABLE))
    assert r.status is EvidenceHandoffStatus.EVIDENCE_INCOMPLETE

def test_invalid_context_is_explicit():
    assert handoff_evidence_for_review(_support(CombinedEvidencePosture.CONTEXT_INVALID)).status is EvidenceHandoffStatus.CONTEXT_INVALID