# Design Gate — Provider Execution Status Observation

**Status:** APPROVED — V1 provider-independent status-observation boundary.

## Purpose

Allow an external provider adapter to report the currently observable status of a previously issued execution request after an ambiguous runtime outcome, without authorizing, retrying, or executing anything.

## V1 Contract

The application boundary exposes:
- `ProviderExecutionStatusQuery`
- `ProviderExecutionStatusResult`
- `ProviderExecutionStatusPort`
- `observe_provider_execution_status(...)`

The query preserves:
- request identity
- provider idempotency identity

The result preserves:
- request identity
- idempotency identity
- `ExecutionOutcomeStatus`
- provider outcome code
- observation timestamp
- optional external reference

## Rules

1. Status observation is evidence only.
2. `UNKNOWN` remains unknown.
3. A status observation never authorizes execution.
4. A status observation never schedules or performs a retry.
5. A status observation never mutates retry policy or command state.
6. Request and idempotency identities must match exactly.
7. Observation timestamps must be timezone-aware.
8. Provider credentials and provider-specific behavior remain adapter concerns.
9. No polling loop, queue, daemon, or automatic reconciliation is introduced.
10. Mapping provider-specific responses into `ProviderExecutionStatusResult` occurs at the adapter boundary.

## Next Boundary

A separate design gate is required before status observations can mutate a durable retry-command state or resolve an ambiguous execution. This increment only creates and validates the observation boundary.
