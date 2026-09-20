# Design Gate — Retry Status Reconciliation Coordination

**Status:** APPROVED — V1 application orchestration boundary.

## Purpose

Coordinate the existing provider status observation, non-mutating reconciliation assessment, and atomic durable-state application into one explicit recovery operation.

## V1 Contract

Input:
- retry command identity
- provider status port
- durable retry command store
- explicit expected state

Flow:
**Load Command → Observe Provider Status → Assess → Apply Assessment**

Output:
- unchanged command for terminal/non-reconcilable/ambiguous status
- atomically resolved command for confirmed completion/failure
- explicit conflict/error when durable state changed or provider observation fails

## Safety Rules

1. This boundary does not execute the original provider action.
2. It performs at most one provider status observation per invocation.
3. It does not poll, sleep, schedule, retry, or restart.
4. Request/idempotency identity must match throughout.
5. Assessment remains non-mutating until the explicit state-application boundary.
6. State application uses expected-state compare-and-set.
7. Ambiguous outcomes remain ambiguous.
8. Confirmed failure becomes manual review, never automatic retry.
9. Terminal commands are never reopened.
10. Provider observation failure is surfaced; durable state is not fabricated or changed.

## TDD Scope

Cover:
- confirmed success → COMPLETED
- confirmed failure → REQUIRES_MANUAL_REVIEW
- unknown → unchanged
- terminal command → no provider status observation
- identity preservation
- provider observation failure → no mutation
- concurrent durable-state conflict
