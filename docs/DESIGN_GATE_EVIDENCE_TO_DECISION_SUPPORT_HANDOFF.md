# Design Gate — Evidence-to-Decision Support Handoff

**Status:** APPROVED — V1 explicit handoff boundary; non-executing.

## Purpose

Define how composed performance evidence becomes a decision-support input without silently becoming a policy or action.

## V1 Contract

Input:
- PerformanceEvidenceDecisionSupport

Output:
- DecisionSupportEvidence containing context, descriptive direction, inferential status, posture, observation lineage, and an explicit `requires_policy_review` flag.

Rules:
1. Evidence is not a decision.
2. The handoff preserves the evidence posture exactly.
3. Any posture other than context-invalid may be handed to policy review; this does not authorize an action.
4. Context-invalid evidence cannot be handed off.
5. No score, ranking, recommendation, lifecycle transition, portfolio action, or execution is created.
6. Policy review remains a separate consumer and must explicitly decide whether an action is permitted.
7. Lineage is preserved.
