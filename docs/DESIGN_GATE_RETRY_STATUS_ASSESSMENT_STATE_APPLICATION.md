# Design Gate — Retry Status Assessment State Application

**Status:** APPROVED — V1 durable application of a non-mutating retry recovery assessment.

## Purpose

Apply an already-created retry status reconciliation assessment to durable retry-command state without re-running providers, scheduling work, or changing immutable command identity.

## V1 Contract

Input:
- durable retry command identity
- expected current state
- non-mutating RetryRecoveryAssessment

Output:
- updated RetryCommand when the expected state transition is applied
- explicit no-op for assessments that require no reconciliation or remain ambiguous
- explicit conflict when durable state changed before application

## Safety Rules

1. Assessment and state mutation remain separate operations.
2. Only assessments with a concrete target state may mutate state.
3. The durable command must still be in the expected pre-transition state.
4. The transition must be atomic at the persistence boundary.
5. Immutable request/idempotency/attempt/command identity cannot change.
6. Terminal commands are never reopened.
7. Ambiguous outcomes never mutate durable state.
8. No provider call, retry scheduling, authorization, or execution occurs here.
9. A concurrent state change produces an explicit conflict, not an overwrite.
10. Applying a confirmed failure produces manual review, not automatic retry.

## Decision Gate

TDD must cover successful completion application, confirmed failure → manual review, ambiguous/no-op behavior, terminal no-op, identity preservation, and concurrent-state conflict. SQLite must enforce the expected-state compare-and-set atomically.
