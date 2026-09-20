# Design Gate — Retry Worker Crash & Recovery Reconciliation

**Status:** APPROVED — V1 reconciliation boundary.

## Purpose

Define how the platform handles durable retry commands whose execution state may be ambiguous after a worker crash or process termination.

## Problem

A worker can claim a retry command and the process can terminate before the platform receives a durable provider outcome. The platform must not infer success, failure, or permission to retry from process termination alone.

## V1 Contract

Recovery reconciliation consumes explicit durable command state plus immutable execution-attempt history and produces one of:

- REQUIRES_MANUAL_RECONCILIATION
- SAFE_TO_RELEASE_FOR_REVIEW

No outcome is fabricated.

## Rules

1. An unknown provider outcome remains unknown.
2. A lifecycle crash never marks a command successful.
3. A lifecycle crash never marks a command failed merely because the process stopped.
4. Immutable attempt history remains authoritative evidence of what was observed.
5. Recovery reconciliation must preserve request identity and provider idempotency identity.
6. Reconciliation must not automatically re-execute a provider request.
7. Reconciliation must not automatically schedule a retry.
8. Authorization and retry policy remain separate from crash reconciliation.
9. A command with an explicit durable terminal outcome is not reopened by crash reconciliation.
10. Ambiguous in-flight execution requires an explicit review/reconciliation state.
11. The boundary is provider-independent; provider-specific status lookup is a future adapter capability.
12. Cross-worker/distributed recovery, leases, heartbeats, and automatic restart are outside V1.

## Decision Gate

The first implementation increment must use TDD and a provider-independent reconciliation result. It must cover durable in-flight state, no fabricated outcome, preserved identity, already-terminal command, duplicate reconciliation protection, and explicit manual review requirement.

No provider-status polling or automatic retry belongs in this increment.
