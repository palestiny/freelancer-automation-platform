# Design Gate — Evidence Policy Review

**Status:** APPROVED — V1 explicit policy-evaluation boundary; non-executing.

## Purpose

Define the first policy-review consumer of an evidence handoff. Policy review may determine whether supplied evidence satisfies an explicitly configured policy condition, but it must not authorize or execute an action.

## V1 Contract

Input:
- EvidenceDecisionHandoff
- explicit PolicyReviewPolicy

Policy inputs:
- allowed descriptive directions
- whether statistical detection is required
- minimum evidence completeness requirement

Output:
- policy evaluation status
- deterministic reason
- preserved evidence context and lineage

Statuses:
- POLICY_SATISFIED
- POLICY_NOT_SATISFIED
- REVIEW_REQUIRED

Reasons:
- SATISFIED
- DIRECTION_NOT_ALLOWED
- STATISTICAL_DETECTION_REQUIRED
- EVIDENCE_INCOMPLETE
- INVALID_CONTEXT
- POLICY_REVIEW_NOT_AVAILABLE

## Rules

1. Policy evaluation is distinct from action authorization.
2. No recommendation, ranking, score, lifecycle mutation, portfolio action, or execution is produced.
3. Context-invalid evidence cannot satisfy policy.
4. Incomplete evidence cannot satisfy a policy requiring complete evidence.
5. A policy may explicitly require statistical detection; absence of statistical detection is then a deterministic mismatch.
6. Policy configuration is explicit and immutable.
7. Evidence lineage is preserved.
8. No default policy is inferred.
9. No automatic policy selection or optimization is introduced.
10. External financial/payment execution remains outside this boundary.
