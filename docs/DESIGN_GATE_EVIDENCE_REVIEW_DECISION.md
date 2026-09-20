# Design Gate — Evidence Review Decision Artifact

**Status:** APPROVED — V1 explicit non-executing review outcome.

## Purpose

Represent the result of a human or policy-review step after an evidence review handoff, without silently turning review into authorization or execution.

## V1 Contract

Input:
- an EvidenceReviewHandoff
- reviewer identity
- explicit review outcome
- decision rationale

Outcomes:
- ACCEPT
- REJECT
- REQUEST_MORE_EVIDENCE

Output:
- immutable EvidenceReviewDecision
- preserved handoff identity, target, evidence lineage, and posture
- reviewer identity and rationale
- explicit outcome

## Rules

1. A review decision is an explicit decision artifact, not execution authorization.
2. ACCEPT does not authorize provider execution, payment, capital movement, or policy mutation.
3. REQUEST_MORE_EVIDENCE does not fabricate missing evidence.
4. REJECT does not mutate source evidence.
5. Reviewer identity and rationale are mandatory.
6. The decision preserves the original evidence lineage and review target.
7. No persistence, notification, scheduling, or external side effect is introduced.
