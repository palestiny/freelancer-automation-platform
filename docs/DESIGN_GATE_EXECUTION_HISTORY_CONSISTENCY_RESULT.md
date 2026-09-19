# Design Gate — Execution History Consistency Result Contract

**Status:** APPROVED — V1 value-object hardening.

## Purpose

Make the execution-history consistency result internally self-consistent so manually constructed artifacts cannot represent impossible combinations of status and observed attempt count.

## V1 Contract

- CONSISTENT requires at least one observed attempt.
- EMPTY_HISTORY requires zero observed attempts.
- IDENTITY_MISMATCH and LATEST_ATTEMPT_MISMATCH require a nonnegative observed history count.
- Request and idempotency identity remain mandatory.
- This hardening does not change how consistency is assessed from actual history.
- It does not infer missing attempts or require contiguous attempt numbers.

## Boundary

No retry, scheduling, execution, authorization, compensation, persistence, or policy mutation.
