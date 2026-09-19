# Design Gate — Execution Recovery Handoff

**Status:** APPROVED — V1 non-executing recovery handoff from execution-outcome policy assessment.

## Purpose

Create an explicit artifact for downstream orchestration when an execution outcome is retry-eligible or requires manual review, without performing or scheduling recovery.

## V1 Contract

Input:
- ExecutionOutcomeAssessment

Output:
- request identity
- idempotency key
- recovery mode
- attempt count
- explicit reason
- source assessment status

Recovery modes:
- RETRY
- MANUAL_REVIEW
- NONE

Rules:
1. Only RETRY_ELIGIBLE maps to RETRY.
2. MANUAL_REVIEW_REQUIRED maps to MANUAL_REVIEW.
3. ACCEPTED and TERMINAL_FAILURE map to NONE.
4. A recovery handoff never authorizes or performs a retry.
5. It never schedules, queues, compensates, or calls a provider.
6. Idempotency and request identity are preserved.
7. No policy, lifecycle, portfolio, learning, or financial state is mutated.
8. Unknown outcomes remain manual review; they must never be converted into retry.
