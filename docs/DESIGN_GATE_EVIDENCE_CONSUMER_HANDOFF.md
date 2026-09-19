# Design Gate — Evidence Consumer Handoff

**Status:** APPROVED — V1 non-executing handoff from evidence composition to explicit decision-support review.

## Purpose

Create a stable boundary where downstream policy/decision logic can consume composed performance evidence without statistical code becoming a policy owner.

## V1 Contract

Input:
- PerformanceEvidenceDecisionSupport

Output:
- EvidenceReviewItem containing business/metric/unit, descriptive direction, inferential status, combined posture, observation lineage, and review state.

Review states:
- READY_FOR_REVIEW
- EVIDENCE_UNAVAILABLE
- CONTEXT_INVALID

Rules:
1. The handoff never executes an action.
2. It never creates a recommendation.
3. It never changes evidence, policy, learning, lifecycle, portfolio, or financial state.
4. READY_FOR_REVIEW means evidence is structurally usable, not that an action is justified.
5. Evidence lineage remains preserved.
