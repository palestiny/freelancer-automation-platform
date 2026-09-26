# Design Gate — Marketplace Opportunity Detail Contract for Intelligence

## Status

**PROPOSED — awaiting owner decision**

Issue: #448

This document proposes the minimum provider-neutral detail contract required to begin V1 Opportunity Intelligence without inventing provider data.

## Evidence boundary

The official Freelancer Python SDK documents project search and project-detail retrieval and exposes request options for full description, jobs, qualifications, and user details. Its examples also demonstrate project budget/currency/jobs as first-class project data. The current adapter already requests full description, jobs, qualifications, and basic user details.

However, the current adapter deliberately maps only title/description into `ExternalOpportunityObservation`. We should not add domain fields merely because the SDK can request them: the exact response-field mapping must be verified against the real Sandbox response before implementation.

## Proposed V1 observation contract

Keep the existing required identity/timestamp fields:

- `provider_key`
- `external_opportunity_id`
- `observed_at`

Keep the existing content fields:

- `title: str | None`
- `description: str | None`

Add only these provider-neutral semantic groups after provider-response verification:

### 1. Opportunity classification

- `project_type: str | None`
- `status: str | None`

Purpose: support Eligibility and distinguish incompatible/closed opportunity types without embedding Freelancer enums in the domain.

### 2. Economics

A provider-neutral budget value:

- `budget_min: Decimal | None`
- `budget_max: Decimal | None`
- `budget_currency: str | None`
- `pricing_model: str | None`

Rules:
- preserve missing bounds as missing;
- preserve missing currency as missing;
- do not convert currencies in the marketplace adapter;
- do not infer a budget from description text;
- do not calculate profitability here.

Economic Fit can therefore return INSUFFICIENT_DATA when the required budget facts are absent.

### 3. Required capabilities

- `required_capabilities: tuple[str, ...]`

These represent provider-reported job/skill facts only.

Rules:
- no AI extraction in this gate;
- no synonym expansion;
- no capability inference from title/description;
- preserve an empty collection only when the provider explicitly reports no required capabilities; otherwise distinguish unavailable data from an explicit empty set.

### 4. Source reference

- `source_url: str | None`

This is provider evidence for traceability/navigation, not a decision signal.

### 5. Client evidence

Do not create a rich Client domain model in this gate.

Use a minimal provider-neutral observation group only if the verified response contains it:

- `client_external_id: str | None`
- `client_country: str | None`
- `client_reputation: ... | None` only after exact response semantics are verified

The client group is evidence for Client / Project Risk. Missing client evidence must remain missing and produce INSUFFICIENT_DATA where required.

## Provenance

Every newly mapped field is still part of the External Opportunity Observation and inherits:

- provider identity;
- external opportunity identity;
- observation timestamp.

The normalization step converts verified observations into the existing Opportunity fields. Provider SDK objects and raw provider response models remain infrastructure-only.

For fields whose provider meaning is ambiguous, the mapping must remain absent rather than guessing.

## Intelligence coverage

| Intelligence dimension | Minimum useful evidence | If absent |
|---|---|---|
| Eligibility | verified project type/status | INSUFFICIENT_DATA where policy requires it |
| Requirement Fit | description + provider-reported capabilities | partial/INSUFFICIENT_DATA |
| Estimated Effort | description + capabilities; estimate remains derived | do not invent effort |
| Economic Fit | budget + currency + pricing model | INSUFFICIENT_DATA |
| Client / Project Risk | verified client/project evidence | INSUFFICIENT_DATA |
| Success Confidence | evidence from the other dimensions + data quality | INSUFFICIENT_DATA / REVIEW_REQUIRED |

This does not introduce scoring or ranking.

## Alternatives considered

### A. Expand only title/description

Pros: minimal code.

Cons: Economic Fit and capability-based Requirement Fit remain structurally unavailable.

### B. Add the full Freelancer response model to the domain

Rejected.

It couples the domain to provider terminology and SDK evolution.

### C. Add a broad provider-neutral contract now

Not recommended.

It creates fields whose semantics have not yet been verified against the real provider response.

### Proposed decision

Use a **small, evidence-driven expansion**: budget/economics, project classification, required capabilities, source URL, and minimal client evidence, but implement only fields whose exact Freelancer response semantics are verified first.

## Required verification before RED

1. Capture a representative Freelancer Sandbox project-search response.
2. Verify exact response paths/types for each proposed field.
3. Record provider field → neutral field mappings.
4. Mark unavailable/ambiguous fields explicitly.
5. Then write RED tests for the agreed subset.
6. Keep provider SDK types outside application/domain code.

## Non-goals

- ranking or scoring;
- AI extraction;
- proposal/bidding;
- payment;
- production access;
- client-domain redesign;
- persistence/UI;
- automatic policy mutation.

## Decision request

Owner approval is required for the proposed semantic expansion before implementation.

Recommended path: approve the **field categories and boundary**, while requiring exact provider-response verification to determine the concrete mapped subset.
