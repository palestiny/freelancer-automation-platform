# Design Gate — Retry Worker Runtime Lifecycle

**Status:** APPROVED — V1 lifecycle semantics implemented and verified; crash/recovery reconciliation remains a separate boundary.

## Purpose

Define the lifecycle semantics required before turning the finite, externally bounded retry-worker batch into a continuously managed runtime.

## Current Boundary

The current runtime can perform a caller-bounded batch of single-command invocations. It has no daemon, queue framework, lease, heartbeat, or worker-pool semantics.

This gate defines those lifecycle semantics. The lifecycle controller, explicit stop/wakeup behavior, and immutable lifecycle observation are implemented. Crash/recovery reconciliation remains intentionally separate.

## V1 Lifecycle

Runtime states:

- STOPPED
- STARTING
- RUNNING
- STOPPING
- STOPPED_WITH_ERROR

Transitions:

- STOPPED → STARTING
- STARTING → RUNNING
- STARTING → STOPPED_WITH_ERROR
- RUNNING → STOPPING
- RUNNING → STOPPED_WITH_ERROR
- STOPPING → STOPPED
- STOPPING → STOPPED_WITH_ERROR
- STOPPED_WITH_ERROR → STARTING only after an explicit restart request

## Control Rules

1. Start is explicit; importing or constructing a worker must not start it.
2. Stop is explicit and must be observable.
3. A stop request prevents new command claims after the current safe boundary.
4. An in-flight provider execution is not forcefully cancelled by the lifecycle controller.
5. Runtime failure must produce an explicit lifecycle observation; it must not silently restart.
6. Restart requires an explicit lifecycle command.
7. The lifecycle controller does not alter retry policy or authorization policy.
8. Command claiming remains atomic and provider-independent.
9. No command may be concurrently claimed by two workers.
10. A worker must revalidate authorization/policy through the existing authoritative boundary before external execution.
11. Shutdown must not fabricate command outcomes for work whose provider result is unknown.
12. Runtime lifecycle and retry eligibility remain separate concerns.

## Scheduling / Waiting

V1 continuous runtime requires a replaceable scheduled-work source and explicit wait semantics.

The lifecycle controller may wait for work or a wake-up signal, but scheduling policy must remain outside the domain retry policy.

No implicit busy-poll loop is permitted.

## Concurrency

V1 supports a single worker process with at most one in-flight provider execution.

Worker pools, distributed leases, multi-process coordination, and horizontal scaling require a separate design gate.

## Recovery

A lifecycle crash must not itself mark a command successful or failed.

Durable command state and immutable attempt history remain authoritative. Commands left in an execution-in-progress state require explicit recovery/reconciliation semantics before any subsequent execution.

## Observability

Each lifecycle run must preserve:
- runtime identity
- lifecycle state transitions
- start/end timestamps
- stop reason or failure code
- invocation/command observations already defined by the finite runtime

Observability remains evidence only and must not trigger automatic restart or retry.

## Explicit Non-Goals

- automatic restart
- distributed worker pools
- queue vendor selection
- provider selection
- automatic retry policy mutation
- payment/capital execution
- metrics backend
- alerting service
- Kubernetes/container orchestration
- cross-business scheduling optimization

## Implementation Gate

Implementation increments completed:
1. lifecycle state semantics and RED tests
2. single-worker runtime controller around the finite invocation
3. explicit stop/wakeup mechanism
4. lifecycle observability
5. integration hardening and CI

Remaining separate boundary:
6. crash/recovery reconciliation for commands left in execution-in-progress state.

No daemon framework or distributed runtime should be introduced implicitly.
