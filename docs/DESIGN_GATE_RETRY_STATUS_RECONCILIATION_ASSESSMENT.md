# Design Gate — Retry Status Reconciliation Assessment

**Status:** APPROVED — V1 non-mutating reconciliation assessment.

## Purpose

Translate an explicit provider status observation into a deterministic recovery assessment for an ambiguous retry command.

## V1 Outcomes

- CONFIRMED_COMPLETED
- CONFIRMED_FAILURE_REQUIRES_REVIEW
- REMAINS_AMBIGUOUS
- NO_RECONCILIATION_REQUIRED
- IDENTITY_MISMATCH

## Rules

1. The assessment consumes a durable RetryCommand and one provider status observation.
2. It does not persist or mutate the command.
3. Terminal retry commands remain terminal and produce NO_RECONCILIATION_REQUIRED.
4. A matching SUCCEEDED observation for EXECUTION_IN_PROGRESS produces CONFIRMED_COMPLETED.
5. A matching FAILED or REJECTED observation produces CONFIRMED_FAILURE_REQUIRES_REVIEW; it does not schedule or execute a retry.
6. UNKNOWN remains REMAINS_AMBIGUOUS.
7. Request and idempotency identity mismatches are explicit failures.
8. No provider polling loop is introduced.
9. No automatic state transition, retry scheduling, authorization, compensation, or execution is introduced.
10. Applying an assessment to durable command state requires a separate design gate.
