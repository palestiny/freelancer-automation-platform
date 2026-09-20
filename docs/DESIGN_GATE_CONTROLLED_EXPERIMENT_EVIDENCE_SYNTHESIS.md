# Design Gate — Controlled Experiment Evidence Synthesis

**Status:** APPROVED — V1 provider-independent synthesis of descriptive and inferential two-variant experiment evidence.

## Purpose

Provide one evidence artifact that preserves descriptive movement and Welch inferential evidence for exactly two declared variants without selecting a winner.

## V1 Contract

Inputs:
- ExperimentVariantComparison
- ExperimentStatisticalComparisonResult

Outputs:
- experiment and metric identity
- variant identities
- descriptive difference
- inferential status
- inferential direction
- explicit synthesis status
- complete observation lineage from both artifacts

Synthesis statuses:
- DESCRIPTIVE_AND_STATISTICAL_ALIGNMENT
- DESCRIPTIVE_CHANGE_WITHOUT_STATISTICAL_DETECTION
- STATISTICAL_AND_DESCRIPTIVE_DIRECTION_CONFLICT
- NO_DETECTED_DIFFERENCE
- STATISTICAL_EVIDENCE_UNAVAILABLE
- CONTEXT_INVALID

## Rules

1. No winner selection, ranking, recommendation, experiment lifecycle mutation, allocation change, or execution.
2. Descriptive movement remains neutral: the first-to-second variant difference is not favorable/unfavorable.
3. Statistical detection is copied from the existing Welch artifact; p-values are not reinterpreted.
4. Direction is descriptive only and is preserved separately from significance.
5. The two artifacts must match experiment, metric, variant identities, and observation lineage.
6. Statistical applicability remains distinct from descriptive comparison applicability.
7. Raw observation IDs remain authoritative provenance.
