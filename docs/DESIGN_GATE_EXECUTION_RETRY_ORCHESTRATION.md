# Design Gate — Execution Retry Orchestration & Scheduling

**Status:** PROPOSED — design only; no runtime implementation authorized by this gate.

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
