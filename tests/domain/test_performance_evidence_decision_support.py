from datetime import datetime
import pytest
from app.domain.performance_history import PerformanceWindow
from app.domain.performance_trend import PerformanceTrend
from app.domain.statistical_evidence_composition import StatisticalEvidenceComposition, StatisticalEvidenceEligibilityReason, StatisticalEvidenceInterpretation
from app.domain.performance_evidence_decision_support import CombinedEvidencePosture, compose_performance_evidence

def trend(change=10.0):
 return PerformanceTrend(metric_name='profit',unit='EGP',current_window=PerformanceWindow(datetime(2026,2,1),datetime(2026,2,8)),baseline_window=PerformanceWindow(datetime(2026,1,25),datetime(2026,2,1)),current_average=100+change,baseline_average=100,absolute_change=change,relative_change=change/100,current_observation_ids=('c1',),baseline_observation_ids=('b1',),current_evidence_quality=80,baseline_evidence_quality=80)

def stat():
 return StatisticalEvidenceComposition(business_id='b1',metric_name='profit',unit='EGP',method='welch_two_sample_t_test',observation_ids=('b1','b2','c1','c2'),eligible=True,reason=StatisticalEvidenceEligibilityReason.ELIGIBLE,interpretation=StatisticalEvidenceInterpretation.STATISTICALLY_DETECTED_DIFFERENCE,alpha=.05)

def test_identity_and_lineage_are_preserved():
 r=compose_performance_evidence(trend=trend(),statistical_evidence=stat(),business_id='b1')
 assert r.business_id=='b1'
 assert r.statistical_observation_ids==('b1','b2','c1','c2')

@pytest.mark.parametrize('business_id',['','   '])
def test_empty_business_id_rejected(business_id):
 with pytest.raises(ValueError,match='business_id'): compose_performance_evidence(trend=trend(),statistical_evidence=stat(),business_id=business_id)

def test_zero_change_is_no_descriptive_change():
 r=compose_performance_evidence(trend=trend(0),statistical_evidence=stat(),business_id='b1')
 assert r.posture is CombinedEvidencePosture.NO_DESCRIPTIVE_CHANGE
