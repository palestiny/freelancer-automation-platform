# Design Gate — Execution Attempt History

**Status:** APPROVED — V1 provider-independent execution-attempt evidence.

## Purpose

Preserve each provider execution attempt as immutable evidence so retries and recovery remain auditable without moving retry scheduling or execution orchestration into the domain.

## V1 Contract

An execution attempt records:
- request_id
- idempotency_key
- attempt_number
- outcome status
- outcome code
- observed_at
- optional external reference

An execution attempt history:
- belongs to exactly one request and idempotency key
- contains unique positive attempt numbers
- exposes chronological ordering
- preserves every attempt as evidence

## Rules

1. Recording an attempt does not authorize, schedule, retry, or execute anything.
2. Attempt number is explicit input; the history does not invent retry policy.
3. Request identity and idempotency identity must remain consistent.
4. Attempt evidence is immutable.
5. Missing attempts are allowed; the domain does not infer continuity.
6. Outcome timestamps must be timezone-aware.
7. This history does not replace ExecutionOutcome; it preserves repeated execution observations.
8. Cross-request aggregation and persistence remain outside this domain slice.
