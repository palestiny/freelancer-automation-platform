# TDD Plan — Marketplace Opportunity Adapter Contract

## Status
READY FOR RED

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
- partial page does not masquerade as complete retrieval.

### Domain isolation tests
- domain imports do not require marketplace SDKs;
- normalized Opportunity contains no provider transport object;
- external identity requires provider plus external id;
- missing optional provider fields remain missing.

## RED Boundary
Create tests against a provider-neutral adapter protocol and deterministic fake adapter before implementing real marketplace integration.

## GREEN Boundary
Implement only the smallest contract required to satisfy the tests. Do not add proposal submission, bidding, provider fallback, queues, credentials storage, or UI.

## HARDEN
Verify invalid inputs, duplicate identities, timezone-naive timestamps, malformed provider mappings, partial retrieval, and secret leakage into errors/logs.

## Completion
All contract tests pass, existing suite remains green, design gate is reconciled, and the real marketplace decision remains explicitly open.