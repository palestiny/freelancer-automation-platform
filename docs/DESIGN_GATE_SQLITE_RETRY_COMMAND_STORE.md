# Design Gate — Durable Retry Command Store

**Status:** APPROVED — V1 SQLite persistence adapter for the existing retry orchestration port.

## Scope

Implement one concrete durable adapter for `RetryCommandStore` using Python's standard-library SQLite driver.

The adapter persists retry command identity and lifecycle state. It does not schedule work, execute providers, authorize actions, or implement retry policy.

## Required Guarantees

1. `(request_id, idempotency_key, attempt_number)` is the durable logical deduplication key.
2. `command_id` remains part of immutable command identity.
3. Duplicate logical commands return the existing command.
4. A duplicate logical command with a different command_id is surfaced to the orchestration boundary as an identity conflict.
5. Claiming is atomic and only one concurrent claimant may transition CREATED → CLAIMED.
6. State transitions are validated through the domain `RetryCommand.transition_to` contract.
7. Time values are stored as timezone-aware ISO-8601 values and reconstructed with timezone information.
8. Scheduler acknowledgements are persisted through the existing command lifecycle.
9. Persistence errors remain infrastructure evidence; they do not mutate retry policy.
10. No scheduler, worker, queue, or provider adapter is introduced.

## SQLite Boundary

The adapter owns:
- connection lifecycle supplied by the caller;
- schema initialization;
- transactional inserts/updates;
- row-to-domain reconstruction.

The domain remains unaware of SQLite.

## Concurrency

Claim uses a transaction and conditional update:
`UPDATE ... WHERE command_id = ? AND state = 'created'`.
Exactly one successful update is required for a successful claim.

SQLite locking behavior is treated as infrastructure behavior; `sqlite3.OperationalError` is not translated into a retry decision.

## Out of Scope

- scheduler implementation
- worker loop
- distributed locking
- queue semantics
- automatic retry
- policy changes
- provider execution
- cross-process orchestration beyond SQLite's transactional guarantees
