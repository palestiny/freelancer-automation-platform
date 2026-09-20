from app.domain.performance_evidence_decision_support import (
    CombinedEvidencePosture,
    DescriptiveDirection,
    InferentialStatus,
    PerformanceEvidenceDecisionSupport,
)
from app.domain.evidence_handoff import (
    EvidenceHandoffStatus,
    create_evidence_handoff,
)


def _support(posture=CombinedEvidencePosture.DESCRIPTIVE_AND_STATISTICAL_ALIGNMENT,
             inferential=InferentialStatus.STATISTICAL_DIFFERENCE_DETECTED):
    return PerformanceEvidenceDecisionSupport(
        business_id="b1",
        metric_name="profit",
        unit="EGP",
        descriptive_direction=DescriptiveDirection.IMPROVING,
        inferential_status=inferential,
        posture=posture,
        statistical_observation_ids=("a", "b"),
    )


def test_ready_handoff_requires_named_consumer():
    result = create_evidence_handoff(
        evidence=_support(),
        consumer_id="portfolio-review",
    )
    assert result.status is EvidenceHandoffStatus.READY
    assert result.consumer_id == "portfolio-review"


def test_unavailable_inferential_evidence_is_not_ready():
    result = create_evidence_handoff(
        evidence=_support(
            posture=CombinedEvidencePosture.INFERENTIAL_EVIDENCE_UNAVAILABLE,
            inferential=InferentialStatus.UNAVAILABLE,
        ),
        consumer_id="portfolio-review",
    )
    assert result.status is EvidenceHandoffStatus.NOT_READY


def test_invalid_context_is_not_ready():
    result = create_evidence_handoff(
        evidence=_support(posture=CombinedEvidencePosture.CONTEXT_INVALID),
        consumer_id="portfolio-review",
    )
    assert result.status is EvidenceHandoffStatus.NOT_READY


def test_empty_consumer_is_rejected():
    try:
        create_evidence_handoff(evidence=_support(), consumer_id=" ")
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError")
