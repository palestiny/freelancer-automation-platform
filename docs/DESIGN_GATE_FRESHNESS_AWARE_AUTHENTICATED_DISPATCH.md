# Design Gate — Freshness-Aware Provider-Authenticated Dispatch

**Status:** APPROVED — V1 execution safety composition.

## Purpose

Prevent an authorized prepared execution request from reaching an authenticated provider adapter when the request is stale or otherwise ineligible for freshness.

## V1 Flow

**Capability → Credential Resolution → Authorization Context → Freshness → Authenticated Provider Invocation**

The existing capability and credential boundaries remain unchanged. Freshness is an additional non-mutating safety precondition immediately before provider invocation.

## Contract

The authenticated dispatch boundary receives:
- the authorized execution request,
- an explicit freshness policy,
- an explicit timezone-aware `as_of`.

Provider invocation is permitted only when freshness is `FRESH`.

Rejected freshness reasons remain explicit:
- NOT_PREPARED
- MISSING_PREPARED_AT
- FUTURE_PREPARED_AT
- STALE

## Rules

1. Freshness does not authorize an action.
2. Freshness does not refresh or mutate a request.
3. No automatic re-authorization, retry, rescheduling, or provider fallback.
4. Credential material is still resolved only after capability verification and remains outside domain state.
5. A stale or ineligible request must not invoke the provider adapter.
6. The dispatch boundary must not infer current time.
7. Existing provider execution-result conformance remains authoritative.
8. This gate does not introduce persistence, scheduling, queueing, or retry semantics.
