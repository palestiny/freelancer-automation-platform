from app.domain.evidence import Evidence, EvidenceKind
from app.domain.venture_evaluation import (
    VentureCriterion,
    VentureCriterionEvaluation,
    VentureCriterionOutcome,
    VentureEvaluation,
    VentureOverallOutcome,
)


def test_venture_evaluation_requires_review_when_evidence_is_insufficient():
    evaluation = VentureEvaluation(
        criteria={
            VentureCriterion.MARKET_DEMAND: VentureCriterionEvaluation(
                VentureCriterionOutcome.PASS,
                (
                    Evidence(EvidenceKind.OBSERVATION, "Observed demand"),
                ),
            ),
            VentureCriterion.EVIDENCE_QUALITY: VentureCriterionEvaluation(
                VentureCriterionOutcome.INSUFFICIENT_DATA,
            ),
        }
    )

    assert evaluation.overall_outcome is VentureOverallOutcome.REVIEW_REQUIRED


def test_failed_venture_criterion_blocks_qualification():
    evaluation = VentureEvaluation(
        criteria={
            VentureCriterion.MARKET_DEMAND: VentureCriterionEvaluation(
                VentureCriterionOutcome.PASS
            ),
            VentureCriterion.CAPITAL_REQUIREMENT: VentureCriterionEvaluation(
                VentureCriterionOutcome.FAIL
            ),
        }
    )

    assert evaluation.overall_outcome is VentureOverallOutcome.NOT_QUALIFIED


def test_all_passing_venture_criteria_qualify():
    evaluation = VentureEvaluation(
        criteria={
            VentureCriterion.MARKET_DEMAND: VentureCriterionEvaluation(
                VentureCriterionOutcome.PASS
            ),
            VentureCriterion.AUTOMATION_POTENTIAL: VentureCriterionEvaluation(
                VentureCriterionOutcome.PASS
            ),
        }
    )

    assert evaluation.overall_outcome is VentureOverallOutcome.QUALIFIED
