# TDD Plan — Marketplace Opportunity Adapter Contract

## Status
**GREEN/HARDENED FOR PROVIDER-NEUTRAL CONTRACT — REAL MARKETPLACE INTEGRATION STILL OPEN**

## Completed RED → GREEN boundary
The provider-neutral adapter contract has been implemented and merged to `main`. The implementation establishes:
- provider-neutral discovery criteria and result types;
- provider/external opportunity identity;
- timezone-aware observation timestamps;
- explicit pagination/completeness;
- neutral provider failure taxonomy;
- domain-independent adapter abstraction;
- deterministic contract and invariant coverage.

This closes the contract-level RED/GREEN slice. It does **not** select or implement a real marketplace.

## Test Layers
### Contract tests
- accepts a valid provider key and discovery criteria;
- returns provider-neutral opportunity observations;
- preserves provider/external identity;
- preserves timezone-aware observation time;
- exposes completeness and continuation explicitly;
- never exposes raw provider SDK objects.

### Failure mapping tests
- authentication failure maps to AUTHENTICATION_FAILURE;
- authorization failure maps to AUTHORIZATION_FAILURE;
- rate limit maps to RATE_LIMITED;
- provider outage maps to PROVIDER_UNAVAILABLE;
- invalid request maps to INVALID_REQUEST;
- malformed provider payload maps to MALFORMED_RESPONSE;
- mixed success/failure retrieval maps to PARTIAL_RESULT when applicable.

### Pagination tests
- first page exposes continuation;
- subsequent page preserves provider identity;
- end-of-results is explicit;
- a complete result cannot also expose a continuation cursor.

### Domain isolation tests
- domain imports do not require marketplace SDKs;
- normalized Opportunity contains no provider transport object;
- external identity requires provider plus external id;
- missing optional provider fields remain missing.

## HARDENED invariants
The merged contract rejects:
- timezone-naive observation/result timestamps;
- empty provider keys or external opportunity identifiers;
- provider identity mismatch between result and observations;
- non-tuple observation collections;
- complete results that contain a continuation cursor;
- invalid failure codes/messages.

## Remaining RED boundary
The next RED slice begins only after the first real marketplace is explicitly selected.

That slice must cover:
- provider-specific request/response mapping;
- provider authentication boundary using opaque credential references;
- provider pagination semantics;
- provider rate-limit/error translation;
- missing-field preservation;
- provenance;
- provider conformance against the existing neutral contract.

## GREEN Boundary for real adapter
Implement only the smallest read-only discovery + normalized detail capability required by the selected provider. Do not add proposal submission, bidding, provider fallback, queues, credential storage, or UI.

## HARDEN for real adapter
Verify:
- malformed provider payloads;
- partial retrieval;
- pagination continuation/end-of-results;
- authentication/authorization failures;
- rate limiting;
- provider outage;
- secret leakage into errors/logs;
- domain isolation from provider SDK/transport types;
- deterministic mapping of provider observations into the neutral contract.

## Completion
The provider-neutral contract slice is complete after implementation, tests, CI, and documentation reconciliation.

The real marketplace adapter remains a separate design/implementation slice and requires an explicit owner decision under Issue #442 before provider-specific code is introduced.
