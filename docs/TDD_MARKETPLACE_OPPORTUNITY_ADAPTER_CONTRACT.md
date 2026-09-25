# TDD Plan — Marketplace Opportunity Adapter Contract

## Status
**IMPLEMENTED — FREELANCER SANDBOX V1 GREEN/HARDEN PENDING CI**

## Completed RED → GREEN boundary
The provider-neutral adapter contract is implemented on `main`. The current branch adds the first real provider adapter boundary for Freelancer.com Sandbox. The implementation establishes:
- provider-neutral discovery criteria and result types;
- provider/external opportunity identity;
- timezone-aware observation timestamps;
- explicit pagination/completeness;
- neutral provider failure taxonomy;
- domain-independent adapter abstraction;
- deterministic contract and invariant coverage.

This closes the provider-neutral contract slice and enters the provider-specific RED → GREEN implementation slice.

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

## Provider-specific RED → GREEN slice
The selected provider is Freelancer.com Sandbox. The implementation covers:
- provider-specific request/response mapping;
- provider authentication boundary using opaque credential references;
- provider pagination semantics;
- provider rate-limit/error translation;
- missing-field preservation;
- provenance;
- provider conformance against the existing neutral contract.

## GREEN Boundary for real adapter
Implemented the smallest read-only discovery + normalized detail capability using the official Python SDK and Sandbox URL. OAuth credentials enter only through an opaque credential reference resolver. No proposal submission, bidding, provider fallback, queues, credential storage, or UI were added.

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

## Current completion state
Provider-specific code and deterministic tests are implemented on the feature branch. CI is the remaining completion gate, followed by final documentation reconciliation and merge.

Provider-specific error classification is intentionally conservative because the official SDK exposes project-search failures through a generic `ProjectsNotFoundException`; the adapter does not invent unsupported rate-limit or authorization semantics.
