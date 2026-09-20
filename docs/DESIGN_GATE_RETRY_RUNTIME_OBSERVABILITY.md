# Design Gate — Retry Runtime Observability

**Status:** APPROVED — V1 invocation observation only.

## Purpose

Make each finite retry-worker invocation auditable without introducing a logging framework, metrics backend, daemon, queue, or lifecycle service.

## V1 Contract

The existing `run_retry_worker_once` remains authoritative for execution behavior.

A separate immutable observation artifact records:
- invocation identity
- start/end timestamps
- runtime outcome
- command identity when a command was selected
- dispatch status when dispatch occurred
- failure code when present

The observation is descriptive evidence only.

## Rules

1. Runtime observation must not change dispatch behavior.
2. The runtime remains finite and externally invoked.
3. Duration is derived from explicit timestamps; no implicit clock inside the domain.
4. Invocation identity is unique and non-empty.
5. Command identity is preserved when selected.
6. Failure information remains explicit.
7. No automatic retry, rescheduling, alerting, health state, or policy mutation is introduced.
8. No metrics provider or logging dependency enters the domain.
9. An observation does not imply provider success; `DISPATCHED` remains an invocation outcome.
10. A future long-running runtime may consume these observations but requires its own lifecycle design gate.
