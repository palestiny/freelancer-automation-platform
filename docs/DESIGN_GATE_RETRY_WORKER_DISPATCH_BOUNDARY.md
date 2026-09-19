# Design Gate — Retry Worker Dispatch Boundary

**Status:** APPROVED — V1 design-only boundary for consuming durable scheduled retry commands.

## Purpose

Define the boundary between durable retry scheduling and future worker/provider execution without introducing a worker loop or external side effect.

## Flow

**Durable Scheduled Command → Claim → Authorization/Policy Revalidation → Prepared Execution Context → Provider Execution Port**

## V1 Contract

A future worker may:
- discover commands in SCHEDULED state;
- atomically claim one command for execution;
- revalidate authorization policy/version/autonomy before external execution;
- transition the command to EXECUTION_IN_PROGRESS only after successful revalidation;
- invoke the existing provider-independent execution boundary;
- record the resulting execution evidence.

## Required Safety

1. Durable command state is authoritative for observed scheduling state.
2. Claiming is atomic; a lost claim must not execute.
3. Authorization/policy context is revalidated immediately before external execution.
4. A stale command must become REJECTED_STALE or an explicit manual-review state; it must not execute.
5. Duplicate worker delivery must be idempotent and must not create a second external retry attempt.
6. Provider execution remains behind the existing ExecutionPort.
7. Unknown provider outcome remains explicit and must not silently create another retry.
8. Worker failures before provider execution must not fabricate execution outcomes.
9. Worker failures after ambiguous provider submission must preserve ambiguity for reconciliation.
10. The worker does not select policy, mutate policy, or automatically escalate autonomy.

## Concurrency

The durable store remains responsible for atomic claim semantics. Worker code must treat a failed claim as a non-executable condition, not as permission to retry the claim blindly.

## Out of Scope

- queue/worker framework selection
- background-process implementation
- distributed lease renewal
- automatic retry loops
- provider selection
- credentials
- payment/financial execution
- automatic policy mutation
- automatic capital movement

## Next Implementation Gate

Implementation requires explicit RED tests for:
- one successful claim among concurrent workers,
- stale authorization rejection,
- duplicate delivery,
- provider success,
- provider failure,
- ambiguous provider result,
- worker failure before provider invocation,
- persistence failure around state transitions.
