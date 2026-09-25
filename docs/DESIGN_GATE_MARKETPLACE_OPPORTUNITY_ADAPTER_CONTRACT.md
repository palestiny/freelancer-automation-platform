# Design Gate — Marketplace Opportunity Adapter Contract

## Status
**APPROVED FOR PROVIDER-NEUTRAL CONTRACT IMPLEMENTATION — real marketplace selection remains open.**

## Purpose
Define the first boundary between the platform and marketplace opportunity discovery without coupling the domain to a marketplace SDK, HTTP client, credential format, or provider response model.

## Scope
V1 is read-only opportunity discovery and normalized opportunity detail.
Flow: External Marketplace → Marketplace Adapter → External Opportunity Observation → Normalization → Opportunity → Opportunity Intelligence.
Proposal submission, bidding, messaging, payment, and automatic execution are outside this gate.

## Ownership
### Marketplace Adapter owns
- provider authentication/authorization mechanics;
- HTTP/SDK transport;
- provider request/response schemas;
- provider pagination and rate-limit handling;
- provider-specific integration retries required to obtain a response safely;
- provider-specific error translation;
- mapping external payloads into the platform observation contract;
- provider metadata and retrieval telemetry.

### Application boundary owns
- selecting enabled providers;
- invoking discovery;
- deciding how incomplete/failed retrieval is surfaced;
- passing normalized observations into normalization/evaluation;
- preserving retrieval metadata and provenance.

### Domain owns
- normalized Opportunity identity and business meaning;
- Opportunity Intelligence policies and evaluation;
- business/economic calculations.
The domain must not import provider SDKs or transport types.

## V1 Adapter Contract
A marketplace adapter exposes a read-only discovery capability conceptually equivalent to discover_opportunities(criteria, page_or_cursor) → OpportunityDiscoveryResult.
The contract must provide provider key, retrieval timestamp, requested criteria or equivalent query identity, normalized external opportunity observations, pagination state when supported, and explicit completeness status.
The contract must not expose raw provider SDK objects to the domain.

## External Opportunity Observation
An observation preserves provider facts before domain normalization.
Minimum semantic fields: provider key; external opportunity identifier; observed-at timestamp; title when available; description/requirements when available; project type when available; budget information when available; source URL when available; required capabilities when available; provider provenance/metadata; raw payload reference only outside the domain boundary.
Missing data is represented explicitly as missing; it is never fabricated during mapping.

## Identity
The canonical external identity is the pair (provider_key, external_opportunity_id).
An external identifier is not globally unique across providers.
A provider-specific identifier change is an identity event, not silently merged with another opportunity.

## Pagination and Freshness
Pagination is an adapter/application concern.
The contract distinguishes complete retrieval, incomplete retrieval with continuation, partial retrieval caused by provider failure, and retrieval where the provider returned no more pages.
The V1 contract does not hide incomplete retrieval behind a successful-looking result.
Freshness is represented by observation timestamps and retrieval metadata. The adapter does not decide whether an opportunity is still actionable.

## Rate Limits
Provider rate-limit behavior remains inside the adapter.
A rate-limited retrieval is distinguishable from authentication failure, provider unavailability, malformed provider response, invalid request, and partial retrieval.
The adapter must not silently switch to another provider.

## Credentials
Only opaque credential references cross the application boundary.
Raw credentials/secrets must not appear in domain objects, opportunity observations, evidence, logs, exception messages, or tests using production secrets.
Credential resolution remains governed by the existing provider credential boundary.

## Failure Semantics
V1 distinguishes at least: AUTHENTICATION_FAILURE, AUTHORIZATION_FAILURE, RATE_LIMITED, PROVIDER_UNAVAILABLE, INVALID_REQUEST, MALFORMED_RESPONSE, PARTIAL_RESULT.
A provider failure is an observation of integration state. It is not automatically a business decision, provider ranking signal, retry command, or fallback instruction.

## Normalization Boundary
Provider payload → provider-specific response.
Adapter mapping → ExternalOpportunityObservation.
Domain normalization → Opportunity.
Evaluation → OpportunityEvaluation.
No layer may skip directly from provider payload to qualification.

## Fake Provider Requirement
Before a real marketplace integration, a deterministic fake adapter must satisfy the same contract and support tests for successful multi-item discovery, stable provider/external identity, missing optional fields, pagination/continuation, partial retrieval, rate limiting, authentication failure, malformed response, provider unavailability, and timezone-aware observation timestamps.
The fake adapter must contain no marketplace-specific semantics.

## Non-goals
- choosing the first real marketplace;
- scraping;
- proposal submission;
- automatic bidding;
- messaging;
- payment;
- credential storage;
- provider ranking/fallback;
- AI provider selection;
- background queues/workers;
- UI.

## Exit Criteria
1. Contract is represented by provider-neutral types/interfaces.
2. Fake adapter passes the contract tests.
3. Provider-specific failures map deterministically to the neutral failure model.
4. Domain tests remain independent of marketplace SDKs.
5. No raw credentials or provider payload types cross into the domain.
6. Pagination/completeness semantics are test-covered.
7. CI passes.
8. Documentation and roadmap are reconciled.
9. Real marketplace selection remains a separate explicit decision.

## Decision Record
This gate intentionally does not choose Upwork, Freelancer.com, or another real marketplace. That choice depends on current external API/access constraints and remains an owner decision under Issue #442.

## Related
- Issue #441 — Design Gate: First Marketplace Adapter
- Issue #442 — Design Gate #441 — Decision Matrix for First Marketplace Adapter
- docs/MARKETPLACE_INTEGRATION_STRATEGY.md
- docs/DESIGN_GATE_OPPORTUNITY_INTELLIGENCE.md
- docs/DESIGN_GATE_PROVIDER_ADAPTER_CONFORMANCE.md
- docs/DESIGN_GATE_PROVIDER_CREDENTIAL_REFERENCE.md