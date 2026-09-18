# Design Gate — Performance Evidence Decision Support

**Status:** APPROVED — V1 provider-independent evidence composition across descriptive and inferential evidence.

## Purpose

Give downstream consumers one explicit evidence artifact that keeps deterministic performance trend evidence separate from statistical evidence.

## V1

Inputs:
- an existing PerformanceTrend
- an existing StatisticalEvidenceComposition

Outputs:
- descriptive direction
- inferential status
- combined evidence posture
- preserved business/metric/unit context and source lineage

Descriptive direction:
- IMPROVING
- DECLINING
- NO_CHANGE
- UNAVAILABLE

Inferential status:
- STATISTICAL_DIFFERENCE_DETECTED
- NO_STATISTICAL_DIFFERENCE_DETECTED
- UNAVAILABLE

Combined posture:
- DESCRIPTIVE_CHANGE_WITH_STATISTICAL_DETECTION
- DESCRIPTIVE_CHANGE_WITHOUT_STATISTICAL_DETECTION
- NO_DESCRIPTIVE_CHANGE
- INFERENTIAL_EVIDENCE_UNAVAILABLE
- CONTEXT_INVALID

## Rules

1. This is evidence composition, not business decision-making.
2. No universal score, ranking, recommendation, policy mutation, learning mutation, portfolio action, or execution.
3. Descriptive direction is derived only from the supplied trend absolute change.
4. Inferential status is copied from the existing statistical evidence artifact; p-values are not reinterpreted.
5. Statistical evidence eligibility remains distinct from statistical interpretation.
6. Context must match on business, metric, and unit.
7. Source observation lineage is preserved from the statistical evidence artifact.
8. A statistically detected difference does not establish directional agreement with the descriptive trend. A nonzero descriptive change plus statistical detection is represented as evidence of change, not directional alignment.
