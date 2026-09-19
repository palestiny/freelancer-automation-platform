# Design Gate — Retry Execution Outcome Handoff

**Status:** APPROVED — V1 provider-independent retry outcome boundary.

## Purpose

Consume an already-observed ExecutionOutcome for a claimed retry execution and close the retry command state without scheduling another retry.

## V1 mapping

- SUCCEEDED → COMPLETED
- FAILED → REQUIRES_MANUAL_REVIEW
- REJECTED → REQUIRES_MANUAL_REVIEW
- UNKNOWN → REQUIRES_MANUAL_REVIEW

The mapping is intentionally terminal for this boundary. Retry decisions remain outside it.

## Rules

1. The outcome must match request identity and idempotency key.
2. The command must be EXECUTION_IN_PROGRESS.
3. Outcome timestamps are preserved by the supplied ExecutionOutcome.
4. Persistence failure does not imply completion.
5. Duplicate completion is rejected rather than silently replayed.
6. No retry, scheduling, compensation, authorization change, or provider call occurs.
7. A non-success outcome is handed to manual review; it is not automatically retried.
