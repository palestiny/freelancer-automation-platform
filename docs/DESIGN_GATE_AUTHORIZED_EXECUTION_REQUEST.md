# Design Gate — Authorized Execution Request Boundary

**Status:** APPROVED — V1 non-executing execution-request artifact.

## Purpose

Create the explicit boundary between action authorization and an eventual execution adapter. The domain may prepare an authorized request, but it must not perform or imply an external side effect.

## V1 Contract

Input:
- ActionAuthorization
- explicit action/request identity
- idempotency key

Output:
- PREPARED execution request when authorization is valid
- REJECTED request when authorization is not valid

The artifact preserves authorization policy identity/version, action class, autonomy level, request identity, and idempotency key.

## Safety Rules

1. Only AUTHORIZED actions can produce a PREPARED request.
2. HUMAN_APPROVAL_REQUIRED, NOT_AUTHORIZED, and SAFETY_BLOCKED actions are rejected.
3. Idempotency key is mandatory and non-empty.
4. The same request identity must not be represented with different idempotency keys inside one request artifact.
5. No provider credentials, provider SDK, queue, scheduler, worker, HTTP call, payment call, marketplace submission, campaign spend, or communication is performed.
6. Preparation is not execution.
7. Execution result/state belongs to a future provider-facing boundary.
