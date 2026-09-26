# TDD Plan — Marketplace Opportunity Adapter Contract

## Status

**COMPLETED — PROVIDER-NEUTRAL CONTRACT + FREELANCER SANDBOX V1 MERGED**

The provider-neutral adapter contract, Freelancer.com Sandbox read-only adapter, and observation-to-domain normalization boundary are merged into `main`.

## Verified implementation boundary

- provider-neutral discovery criteria/result types;
- provider/external opportunity identity;
- timezone-aware observation timestamps;
- explicit pagination/completeness;
- neutral provider failure taxonomy;
- domain-independent adapter abstraction;
- Freelancer Sandbox credential-reference boundary;
- provider response mapping;
- pagination mapping;
- malformed payload handling;
- credential-resolution failure mapping;
- provider-unavailability mapping;
- domain isolation from provider SDK types;
- application normalization from `ExternalOpportunityObservation` to `Opportunity`.

## Normalization rules

- provider identity is preserved as `source_platform`;
- external identity is preserved as `source_opportunity_id`;
- verified title/description are preserved;
- missing required domain content is rejected rather than fabricated;
- fields not present in the current observation contract are not inferred.

## Remaining provider-detail expansion

The current observation contract is intentionally minimal. The design gate describes richer optional detail such as project type, budget, required capabilities, source URL, client reference, and provenance metadata.

Those fields require a dedicated design/test slice after verification against the real Freelancer response contract. No provider-specific assumptions are promoted into the domain.

## Current completion state

- Provider-neutral contract: complete.
- Freelancer Sandbox adapter V1: complete and merged.
- Observation → Opportunity normalization: complete and merged.
- Sandbox integration execution remains credential/environment dependent and is not a CI prerequisite.
- Production/Terms validation remains a separate open gate (#445).
- Proposal/bid execution, payment, UI, and production marketplace dependency remain outside scope.

## Next gate

Define the minimum provider-detail contract required to support the committed Opportunity Intelligence dimensions without inventing data or coupling the domain to Freelancer-specific fields.
