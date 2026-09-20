# Design Gate — Retry Worker Runtime Loop

**Status:** APPROVED — V1 finite runtime invocation implemented.

## Purpose

Define the smallest runtime boundary required to repeatedly consume durable scheduled retry work without moving scheduling, retry policy, authorization, or provider semantics into the worker loop.

## V1 Contract

The worker runtime may request one eligible scheduled command, invoke the existing single-command worker dispatch boundary, record the dispatch result as an observed runtime outcome, and stop according to an explicit runtime result.

The worker runtime must not invent retry policy, reschedule failed work itself, bypass authorization revalidation, call providers directly, mutate autonomy or authorization policy, perform compensation, run unbounded work without an explicit stop/cancellation boundary, or hide persistence, claim, provider, or outcome errors.

## Runtime Outcomes

V1 runtime iteration reports one explicit outcome:
- DISPATCHED
- IDLE
- BLOCKED
- FAILED

DISPATCHED means the single-command dispatch boundary was invoked; it does not mean provider success.

IDLE means no eligible work was available.

BLOCKED means the dispatch boundary intentionally refused work because an explicit application guard blocked it.

FAILED means the runtime boundary encountered an infrastructure/application error and did not silently retry.

## Lifecycle

A worker invocation is finite and externally controlled:

Start → Attempt One Dispatch → Report Outcome → Stop

A repeated loop, daemon, queue consumer, or background service is not part of V1.

## Safety / Durability Rules

- Durable scheduler/store remains authoritative for work identity and claim semantics.
- Single-command worker dispatch remains authoritative for authorization revalidation and provider dispatch.
- Provider failure remains governed by the existing manual-review boundary.
- Ambiguous persistence/scheduler results remain explicit.
- No in-memory queue becomes an alternative source of truth.
- Runtime repetition cannot create duplicate logical retry commands.

## Decision Gate

This gate approves only a finite worker-runtime invocation contract. A long-running daemon, queue integration, lease/heartbeat, concurrency model, graceful shutdown, health checks, or deployment-specific worker service requires a separate design decision before implementation.


## Implementation Status

The finite invocation and concrete SQLite scheduled-work source are implemented and CI-verified. The implementation consumes at most one scheduled command per invocation and then stops. Continuous looping, daemon lifecycle, queue integration, leases, heartbeats, concurrency pools, and deployment-specific worker services remain outside this gate.
