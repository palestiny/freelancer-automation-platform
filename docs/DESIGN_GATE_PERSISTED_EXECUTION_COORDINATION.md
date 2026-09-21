# Design Gate — Persisted Execution Coordination

**Status:** APPROVED — V1 application boundary integrating authoritative execution-outcome persistence.

## Problem

Execution outcome persistence exists as a durable evidence boundary, while the current execution coordinator returns provider outcomes directly. Without an explicit integration boundary, callers can execute and assess recovery without first durably recording the authoritative outcome.

## V1 contract

**Authorized Request → Provider Execution → Durable Outcome Persistence → Outcome Policy Assessment → Recovery Handoff**

The persisted coordinator:
- executes exactly once through the supplied ExecutionPort;
- persists the returned ExecutionOutcome before policy/recovery assessment;
- returns an explicit persistence failure instead of fabricating recovery state;
- preserves provider outcome identity and evidence;
- remains provider-independent at the domain boundary.

## Failure semantics

- Provider failure produces no fabricated outcome.
- Outcome persistence failure produces no policy assessment or recovery handoff.
- Exact duplicate outcome persistence remains idempotent at the repository boundary.
- Persistence does not authorize, retry, or execute anything itself.

## Boundary

This gate does not add background workers, distributed transactions, outbox semantics, automatic retries, or provider-specific behavior.
