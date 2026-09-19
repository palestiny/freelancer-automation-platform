# Design Gate — Execution Outcome Contract

**Status:** APPROVED — V1 provider-independent execution outcome artifact.

## Purpose

Define the domain boundary after an authorized execution request reaches an external execution adapter.

The domain records what an adapter reports; it does not call providers, retry, schedule, or execute external actions.

## V1 Contract

An execution outcome references:
- request identity
- idempotency key
- action class
- execution status
- provider-independent outcome code
- optional external reference
- observed timestamp

Statuses:
- SUCCEEDED
- FAILED
- REJECTED
- UNKNOWN

Rules:
1. An outcome must reference a prepared request identity and idempotency key.
2. Provider-specific response formats do not enter the domain.
3. UNKNOWN is explicit and must not be converted to success or failure.
4. An outcome never authorizes a request.
5. Recording an outcome does not trigger retries, compensation, billing, capital movement, or policy mutation.
6. Duplicate idempotency keys are invalid within one outcome stream.
7. External execution remains an adapter responsibility and is outside this domain implementation.
