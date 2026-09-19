# Design Gate — Retry Execution Claim & Handoff

**Status:** APPROVED — V1 provider-independent execution claim boundary.

## Purpose

Move a durable retry command from scheduled work into an explicit execution-in-progress handoff without executing a provider action.

## V1 contract

Scheduled RetryCommand → atomic claim → ExecutionHandoff

The handoff preserves command identity, request identity, idempotency key, attempt number, authorization policy identity/version, autonomy bound, and scheduling identity.

The claim is valid only for a command in SCHEDULED state. A lost race returns an explicit claim conflict and does not fabricate execution progress.

## Rules

1. Claiming is not execution.
2. No provider API, queue, worker loop, or external side effect is introduced.
3. Authorization is not silently re-granted; the handoff preserves the authorization context already attached to the command.
4. Duplicate claims must be idempotent or explicitly rejected by the store.
5. Persistence failures do not imply execution occurred.
6. Only SCHEDULED → EXECUTION_IN_PROGRESS is allowed.
7. The handoff is the boundary consumed by a future execution worker/provider adapter.
8. Completion/failure outcome handling remains a separate boundary.
