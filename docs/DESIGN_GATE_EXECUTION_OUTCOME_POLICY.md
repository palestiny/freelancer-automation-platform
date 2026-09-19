# Design Gate — Execution Outcome Policy

**Status:** APPROVED — V1 non-executing assessment of execution outcomes.

## Purpose

Convert an observed execution outcome into an explicit policy assessment without retrying, compensating, scheduling, or executing anything.

## V1

Policy inputs:
- retryable outcome codes
- maximum retry attempts
- whether unknown outcomes require manual review

Assessment:
- ACCEPTED
- RETRY_ELIGIBLE
- MANUAL_REVIEW_REQUIRED
- TERMINAL_FAILURE

Rules:
1. SUCCEEDED is ACCEPTED.
2. REJECTED is TERMINAL_FAILURE.
3. UNKNOWN is MANUAL_REVIEW_REQUIRED when configured; otherwise TERMINAL_FAILURE is not permitted — UNKNOWN remains explicit review.
4. FAILED is RETRY_ELIGIBLE only when its outcome code is explicitly configured and the current attempt count is below the policy maximum.
5. Otherwise FAILED is TERMINAL_FAILURE.
6. Assessment preserves request identity and idempotency key.
7. Assessment never schedules, retries, compensates, authorizes, mutates policy, or executes.
8. Financial and irreversible action classes remain outside automatic execution in the existing authorization boundary.
