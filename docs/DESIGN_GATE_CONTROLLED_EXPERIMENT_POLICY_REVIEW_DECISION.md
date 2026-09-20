# Design Gate — Controlled Experiment Policy Review Decision

**Status:** APPROVED — V1 explicit human/policy review decision after experiment hypothesis-policy evaluation.

## Purpose

Represent a review decision about an experiment policy result without confusing review with authorization, experiment lifecycle mutation, allocation, or execution.

## V1 Contract

Input:
- ExperimentPolicyReviewHandoff
- reviewer identity
- explicit outcome: ACCEPT, REJECT, REQUEST_MORE_EVIDENCE
- rationale

Output:
- immutable review decision preserving experiment, metric, hypothesis direction, exact policy outcome, handoff identity, reviewer, rationale, and observation lineage.

## Rules

1. ACCEPT is a review decision, not authorization.
2. REJECT does not mutate experiment lifecycle.
3. REQUEST_MORE_EVIDENCE does not automatically launch another experiment.
4. The exact policy outcome from the handoff is preserved.
5. Observation lineage is immutable.
6. No allocation, scheduling, execution, provider call, payment, portfolio action, or automatic policy mutation occurs.
7. Authorization remains a separate boundary.
