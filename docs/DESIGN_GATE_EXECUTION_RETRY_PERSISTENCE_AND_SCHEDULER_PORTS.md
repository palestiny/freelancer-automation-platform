# Design Gate — Execution Retry Persistence & Scheduler Ports

**Status:** APPROVED — V1 infrastructure boundary resolved; concrete adapters remain out of scope.

## Purpose

Define the replaceable application ports required before runtime retry orchestration can safely schedule and execute recovery handoffs.

## Durable Command

A retry orchestration command has immutable identity: command_id, request_id, idempotency_key, attempt_number.

It also preserves action type (RETRY or MANUAL_REVIEW), authorization policy identity/version, autonomy bound, created_at, lifecycle state, scheduling identity, and last infrastructure observation. The command identity is the deduplication anchor.

## Command Lifecycle

CREATED -> SCHEDULED -> CLAIMED -> REVALIDATION_REQUIRED -> EXECUTION_IN_PROGRESS -> COMPLETED

Explicit terminal/non-success states: REJECTED_STALE, REQUIRES_MANUAL_REVIEW, SCHEDULING_AMBIGUOUS, CLAIM_CONFLICT.

A lifecycle state is orchestration evidence, not a replacement for provider execution outcome.

## Persistence Port

The application boundary requires a replaceable durable store with operations equivalent to: create-or-get by command identity; get by command_id; atomically transition state with expected current state; atomically claim a runnable command; record scheduling acknowledgement; record infrastructure/manual-review observation.

Persistence must enforce command identity uniqueness and atomic claim semantics.

## Scheduler Port

The scheduler boundary accepts a durable command reference and explicit scheduling identity. It may return only ACCEPTED, REJECTED, or AMBIGUOUS. An ambiguous acknowledgement must never cause speculative duplicate scheduling.

The scheduler does not own authorization, retry policy, attempt numbering, or provider execution.

## Revalidation

Before external execution, the coordinator must revalidate prepared request identity, authorization identity/version, autonomy bound, retry policy eligibility, immutable attempt history consistency, and command identity/idempotency identity. A failed revalidation transitions to explicit stale/manual-review state and produces no external side effect.

## Claiming

Only one worker may claim a command through an atomic compare-and-set operation. A lost race returns CLAIM_CONFLICT; it does not create a new command or attempt.

## Ambiguity

Scheduler ambiguity is durable orchestration evidence. The system must retain the original command identity and reconcile that identity before creating any new schedule request.

## Failure Boundary

Persistence failures = infrastructure evidence. Scheduler failures = orchestration evidence. Provider failures = ExecutionOutcome. Retry eligibility = existing execution policy. Authorization = existing authorization boundary. No failure category silently changes another category's policy.

## Explicit Non-Goals

No concrete database, concrete queue/scheduler, background workers, provider credentials, automatic retry loops, financial execution, compensation, or AI/provider selection.

## Implementation Gate

The next implementation increment may define provider-independent command value objects and ports with RED tests for identity uniqueness, lifecycle transitions, atomic claim semantics, scheduler acknowledgement mapping, and stale-state representation. Concrete persistence/scheduler adapters require their own integration design.
