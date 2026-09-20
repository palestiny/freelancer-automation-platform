# Design Gate — Evidence Review Handoff

**Status:** APPROVED — V1 explicit handoff from composed evidence to human/policy review.

## Purpose

Close the gap between evidence composition and policy review without turning evidence into automatic policy.

## V1 Contract

Input:
- a PerformanceEvidenceDecisionSupport artifact
- an explicit review reason
- a review target

Output:
- immutable EvidenceReviewHandoff
- business/metric/unit identity
- descriptive direction
- inferential status
- combined posture
- observation lineage
- review target and reason

Review targets:
- POLICY_REVIEW
- HUMAN_REVIEW

## Rules

1. The handoff is non-executing.
2. It does not approve, reject, mutate, or authorize policy.
3. It preserves the evidence composition exactly; no new statistical interpretation is performed.
4. Evidence lineage is preserved.
5. Empty review reasons/targets are invalid.
6. This boundary does not schedule work, notify users, or persist externally.
