# Design Gate — Prepared Execution Request Freshness

**Status:** APPROVED — V1 bounded execution safety precondition.

## Purpose

Prevent an authorized execution request from being treated as indefinitely valid after the evidence review and authorization that produced it.

## V1 Contract

An explicit freshness assessment consumes:
- an immutable prepared execution request,
- its explicit preparation timestamp,
- a versionable maximum age policy,
- an explicit `as_of` timestamp.

Result:
- FRESH
- STALE
- MISSING_PREPARED_AT
- FUTURE_PREPARED_AT
- NOT_PREPARED

## Rules

1. Freshness is a safety precondition, not authorization.
2. The evaluator never refreshes, extends, or mutates a request.
3. `as_of` is explicit; no hidden current-clock lookup occurs.
4. Age is calculated from preparation time, not from observation time.
5. Rejected/non-prepared requests cannot become fresh.
6. A future preparation timestamp is rejected explicitly.
7. No automatic re-authorization, retry, rescheduling, or provider call is introduced.
8. The policy is changeable and explicit; no universal default is imposed on existing execution semantics.
9. Evidence lineage and policy identity already carried by the request remain untouched.
