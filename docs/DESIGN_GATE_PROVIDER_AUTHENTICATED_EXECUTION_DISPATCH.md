# Design Gate — Provider-Authenticated Execution Dispatch

**Status:** APPROVED — V1 application boundary connecting explicit capability checks with explicit credential resolution.

## Purpose

Provide one application-level dispatch boundary that:
1. verifies the requested provider capability,
2. resolves the explicitly referenced credential,
3. verifies provider/reference binding,
4. invokes an authenticated provider adapter contract,
5. returns the existing provider execution result for normal conformance.

## V1 Contract

The authenticated adapter receives:
- the prepared authorized execution request,
- resolved credential material.

Credential material exists only inside the application/integration call path and is never copied into domain execution entities or returned in the result.

Failures:
- unsupported capability: reject before credential resolution,
- credential resolution failure: reject before provider invocation,
- provider/reference binding mismatch: reject,
- invalid credential-resolution result: reject.

## Rules

- Authentication is not authorization.
- Credential resolution does not authorize execution.
- Capability support does not imply credential availability.
- No fallback provider selection.
- No credential fallback.
- No credential caching/rotation/refresh.
- No secret persistence.
- No automatic retry.
- Provider execution remains replaceable.
- Existing execution-result conformance remains authoritative after adapter invocation.
