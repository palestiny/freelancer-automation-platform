# Design Gate — Retry Worker Runtime Invocation Implementation

**Status:** APPROVED — V1 finite single-dispatch invocation.

## Contract

One invocation:
1. Request the next eligible scheduled retry command from the durable store.
2. If none exists, return IDLE.
3. Invoke the existing single-command dispatch boundary exactly once.
4. Map the dispatch result to an explicit runtime outcome.
5. Stop.

Runtime outcomes:
- DISPATCHED — dispatch boundary was invoked.
- IDLE — no eligible scheduled command existed.
- BLOCKED — the selected command could not be claimed because another invocation owns the claim.
- FAILED — the runtime encountered a source/dispatch infrastructure failure.

A stale authorization rejection, provider failure, manual-review transition, or outcome-persistence failure is still DISPATCHED because the runtime successfully invoked the authoritative dispatch boundary; the detailed dispatch result remains available to the caller.

## Safety

- Durable storage is the only source of scheduled work.
- Selection is deterministic: earliest created scheduled command, then command_id.
- The runtime never executes providers directly.
- The runtime never retries or reschedules.
- Authorization revalidation remains inside single-command dispatch.
- Atomic claim remains inside single-command dispatch.
- One invocation consumes at most one command.
- Repeated invocations rely on durable state and claims; no in-memory cursor exists.
- Source and dispatch exceptions are surfaced as FAILED.
- No daemon, queue, lease, heartbeat, worker pool, or graceful-shutdown semantics are introduced.
