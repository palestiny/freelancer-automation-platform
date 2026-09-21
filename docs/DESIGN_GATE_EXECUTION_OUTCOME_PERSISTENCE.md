# Design Gate — Execution Outcome Persistence

**Status:** APPROVED — V1 authoritative execution-outcome persistence boundary.

## Purpose

Persist execution outcomes durably after provider execution so recovery assessment and later evidence consumers can reference authoritative outcome records.

## V1 contract

- Domain `ExecutionOutcome` remains immutable and provider-independent.
- Application owns a repository port.
- SQLite is the reference adapter.
- Outcome identity is `request_id + observed_at + idempotency_key` for lookup context, while a single idempotency key may not silently map to conflicting outcomes.
- Exact duplicate persistence is idempotent.
- Conflicting reuse of the same request/idempotency identity is rejected.
- Persistence does not assess recovery, retry, authorize, execute, or mutate request state.
- No distributed transaction/outbox semantics are introduced.

## Read operations

- get by request id
- list by idempotency key

## Safety

Malformed domain values remain rejected by the domain boundary. The repository is an evidence store, not a policy engine.
