# Design Gate — Bounded Retry Worker Batch Invocation

**Status:** APPROVED — V1 externally bounded repeated invocation.

## Purpose

Extend the existing single-command retry worker invocation into a finite batch boundary without introducing a daemon, queue framework, lease system, heartbeat, or worker pool.

## V1 Contract

A batch invocation accepts an explicit positive maximum invocation count and repeatedly delegates to the authoritative `run_retry_worker_once` boundary.

It stops at the first terminal runtime outcome:
- IDLE
- BLOCKED
- FAILED

It also stops when the explicit invocation limit is reached.

DISPATCHED means one command was attempted and the batch may continue.

## Result

The batch reports:
- total invocation attempts
- dispatched invocation count
- terminal stop reason
- ordered immutable per-invocation runtime results

## Safety

1. The batch never selects work itself.
2. Durable scheduled storage remains authoritative.
3. Single-command dispatch remains authoritative for claims, authorization, provider execution, and outcomes.
4. The batch never retries a failed command itself.
5. No sleeping, polling interval, queue, lease, heartbeat, concurrency, or background lifecycle is introduced.
6. The explicit maximum is mandatory; unbounded execution is rejected.
7. A BLOCKED or FAILED result stops the batch rather than spinning.
8. An IDLE result stops the batch because no work is currently available.

## Trade-off

A bounded batch improves operational efficiency for externally scheduled invocations while preserving deterministic termination. It intentionally does not solve continuous worker lifecycle or concurrency; those remain deployment-specific future boundaries.
