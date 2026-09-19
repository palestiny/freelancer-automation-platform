# Design Gate — Performance Evidence Decision Policy

**Status:** APPROVED — V1 consumer-facing interpretation boundary.

## Purpose

Translate the existing descriptive/inferential evidence composition into explicit evidence states for downstream policy consumers, without creating a recommendation or executing a policy.

## V1 Evidence States

- SUPPORTS_IMPROVEMENT
- SUPPORTS_DECLINE
- DESCRIPTIVE_CHANGE_WITHOUT_STATISTICAL_DETECTION
- NO_MATERIAL_DESCRIPTIVE_CHANGE
- INSUFFICIENT_INFERENTIAL_EVIDENCE
- CONTEXT_INVALID

## Rules

1. The state is evidence, not a business decision.
2. A detected statistical difference is never sufficient by itself to label improvement or decline; direction must come from descriptive trend evidence.
3. If descriptive and inferential evidence disagree, preserve the disagreement as DESCRIPTIVE_CHANGE_WITHOUT_STATISTICAL_DETECTION.
4. Ineligible statistical evidence cannot be upgraded by descriptive evidence.
5. No score, rank, recommendation, lifecycle mutation, learning mutation, portfolio action, capital allocation, or execution.
6. No automatic thresholds beyond the explicit evidence artifact semantics.
7. Preserve source observation lineage.
