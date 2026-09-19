# Design Gate — Execution Retry Orchestration & Scheduling

**Status:** APPROVED — design resolved; runtime implementation remains blocked until the required persistence/scheduler boundary is explicitly introduced.

## Purpose

Define the boundary that turns the existing non-executing recovery handoff into an orchestration concern capable of scheduling a retry or manual-review task without moving provider execution semantics into the domain.

## Current Inputs

- AuthorizedExecutionRequest
- ExecutionOutcome
- immutable ExecutionAttemptHistory
- history-consistent ExecutionPolicyAssessment
- RecoveryHandoff
- provider-independent ExecutionPort

## Proposed V1 Scope

The orchestration layer may:
1. accept only history-consistent recovery handoffs;
2. create an explicit orchestration command for RETRY or MANUAL_REVIEW;
3. persist a durable scheduling/idempotency identity;
4. schedule retry work through a replaceable scheduler port;
5. invoke the existing ExecutionPort when a scheduled retry becomes runnable;
6. record the resulting attempt and re-enter history-aware policy assessment.

## Safety Boundary

The orchestration layer must not:
- bypass authorization;
- change retry policy;
- invent attempt numbers;
- execute an unprepared request;
- execute a retry after a terminal/manual-review outcome;
- create duplicate scheduled retries for the same idempotency identity and attempt;
- mutate domain policy based on runtime outcomes;
- perform compensation automatically;
- move money or perform financial execution;
- select AI/provider strategies implicitly.

## Required Invariants

- Retry commands are idempotent.
- Scheduling identity is durable and explicit.
- Attempt history remains the authoritative execution evidence.
- Scheduler/provider ports are replaceable.
- Domain remains provider- and framework-independent.
- Manual-review outcomes must never be auto-converted into retry commands.
- A scheduled retry must be revalidated against current authorization and policy before external execution.
- External side effects occur only behind explicit application ports.

## Open Design Questions

1. What durable state is required for a scheduled command?
2. When must authorization be revalidated: at scheduling time, execution time, or both?
3. How is a stale scheduled retry invalidated?
4. What happens when the scheduler reports an ambiguous delivery/execution state?
5. How should concurrent workers claim one retry safely?
6. What persistence guarantees are required for idempotency?
7. Which failures belong to scheduler infrastructure versus provider execution evidence?

## Decision Gate

No scheduler, queue, worker, retry loop, persistence model, or provider adapter changes should be implemented until these questions are resolved in a dedicated design review and RED tests define duplicate scheduling, stale authorization, ambiguous scheduler outcomes, concurrent claim, and terminal/manual-review protection.


## Resolved Design Decisions

### Durable State

The orchestration boundary requires a durable command record keyed by:
- request_id
- idempotency_key
- attempt_number
- command identity

The record must preserve command lifecycle, authorization policy identity/version, autonomy bound, creation time, and scheduling state. The domain does not own the storage mechanism.

### Authorization Revalidation

Authorization is checked twice:
1. when the retry command is created;
2. immediately before external execution.

The second check is authoritative. A stale or revoked authorization prevents execution and produces an explicit manual-review outcome.

### Stale Scheduled Retries

A scheduled retry becomes stale when its authorization, policy version, autonomy bound, request identity, or attempt identity no longer matches the current executable context. Stale work is not silently retried; it is rejected and surfaced for explicit review.

### Ambiguous Scheduler Outcomes

If scheduling acknowledgement is ambiguous, the system must not create a second command speculatively. Durable command identity remains the deduplication anchor, and the state is surfaced as infrastructure/manual-review ambiguity until the scheduler state can be reconciled.

### Concurrent Workers

A retry may be claimed by exactly one worker through an atomic durable claim keyed by the durable command identity. A worker must revalidate authorization and execution preconditions after claiming and before the external side effect.

### Idempotency Guarantees

The durable command identity and provider idempotency key are separate but linked identities. Re-delivery of the same command must not create a new attempt number or a second logical retry. Attempt history remains authoritative for observed execution attempts.

### Failure Classification

Scheduler/infrastructure failures remain orchestration evidence. Provider execution failures remain execution outcomes. Neither category silently changes retry policy. The existing outcome-policy boundary remains the source of retry eligibility.

## Implementation Gate

The next implementation increment is intentionally blocked until a persistence and scheduler port design is approved. When implemented, RED tests must cover:
- duplicate scheduling;
- stale authorization;
- stale policy/autonomy context;
- ambiguous scheduler acknowledgement;
- concurrent claim;
- terminal/manual-review protection;
- retry idempotency;
- revalidation immediately before provider execution.

No queue, worker, scheduler implementation, or provider adapter is introduced by this design-only change.
