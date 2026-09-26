# Design Gate — Marketplace Opportunity Detail Contract for Intelligence

## Status

**APPROVED — semantic boundary accepted; concrete mappings gated by provider-response evidence**

Issue: #448

This document defines the proposed minimum provider-neutral detail contract for V1 Opportunity Intelligence.

## Evidence boundary

Official Freelancer SDK material verifies that the integration can:
- search projects;
- retrieve project details;
- request full descriptions;
- request jobs/qualifications;
- request basic/profile/reputation user details.

The SDK's project-creation example also demonstrates project budget, currency, and jobs as first-class project data. See the official Freelancer SDK repository and its `get_projects.py` and `create_project.py` examples for this capability evidence.

**Important limitation:** this is SDK capability evidence, not evidence of the exact Sandbox response received by our adapter. We do not have a verified live Sandbox payload in CI or in the repository. Therefore no new field should be mapped until its actual response path/type is captured and verified.

## Current adapter boundary

The adapter currently requests full description, jobs, qualifications, and basic user details, but intentionally maps only:

- `provider_key`
- `external_opportunity_id`
- `observed_at`
- `title`
- `description`

This conservative boundary is correct until response evidence is available.

## Proposed V1 observation contract

### 1. Opportunity classification

- `project_type: str | None`
- `status: str | None`

Use only verified provider facts. Do not expose Freelancer SDK enums.

### 2. Economics

- `budget_min: Decimal | None`
- `budget_max: Decimal | None`
- `budget_currency: str | None`
- `pricing_model: str | None`

Rules:
- preserve missing bounds/currency;
- no currency conversion in the marketplace adapter;
- no budget inference from free text;
- no profitability calculation here.

### 3. Required capabilities

- `required_capabilities: tuple[str, ...]`

Only provider-reported job/skill facts.

No AI extraction, synonym expansion, or inference in this gate.

### 4. Source reference

- `source_url: str | None`

Used for provenance/traceability, not qualification.

### 5. Minimal client evidence

Only if verified in the actual provider response:

- `client_external_id: str | None`
- `client_country: str | None`
- reputation fields only after their exact semantics are verified.

Do not introduce a rich Client domain model in this gate.

## Missing-data semantics

Missing is a valid state and must remain distinguishable from a provider-reported empty value.

Examples:
- no budget returned → budget is unavailable;
- no skills field returned → capabilities unavailable;
- explicit empty skills list → provider reported no skills;
- ambiguous provider field → do not map it.

No mapper may fabricate values.

## Provenance

Every mapped field remains part of `ExternalOpportunityObservation` and is associated with:

- provider identity;
- external opportunity identity;
- observation timestamp.

Provider SDK objects remain infrastructure-only.

## Intelligence coverage

| Dimension | Evidence | Missing-data behavior |
|---|---|---|
| Eligibility | verified type/status | INSUFFICIENT_DATA when policy requires it |
| Requirement Fit | description + provider skills | INSUFFICIENT_DATA/partial |
| Estimated Effort | description + capabilities | derived estimate only; never fabricated |
| Economic Fit | budget + currency + pricing model | INSUFFICIENT_DATA |
| Client / Project Risk | verified client/project evidence | INSUFFICIENT_DATA |
| Success Confidence | quality of evidence across dimensions | INSUFFICIENT_DATA / REVIEW_REQUIRED |

No scoring or ranking is introduced by this gate.

## Decision alternatives

### A — Keep title/description only

Smallest implementation, but Economic Fit and provider-reported capability analysis remain structurally unavailable.

### B — Put Freelancer response objects into the domain

Rejected because it couples business meaning to provider SDK schemas.

### C — Evidence-driven provider-neutral expansion

**Recommended:** approve the semantic categories above, but implement only the subset whose exact Sandbox response fields are verified.

## Verification gate before RED

1. Obtain a representative Sandbox project-search response.
2. Obtain a representative project-detail response if search does not contain all required facts.
3. Record exact provider response paths, types, and semantics.
4. Build a field mapping matrix:
   `provider field → observation field → normalization field → intelligence dimension`.
5. Explicitly mark unavailable/ambiguous fields.
6. Write RED tests only for verified mappings.
7. Implement mapping without leaking provider SDK types.
8. Harden missing/ambiguous-field behavior.

## Non-goals

- ranking/scoring;
- AI extraction;
- proposal/bidding;
- payment;
- production access;
- client-domain redesign;
- persistence/UI;
- automatic policy mutation.

## Decision record

Owner decision: **approved** on 2026-09-26.

Approved boundary: evidence-driven provider-neutral expansion covering classification, economics, required capabilities, source provenance, and minimal client evidence. Reputation fields remain deferred until their exact provider semantics are verified.

Approval does not authorize inventing provider fields, implementing unverified mappings, proposal/bidding execution, payment, production dependency, or automatic policy mutation.

The concrete field subset remains conditional on captured/verified Freelancer Sandbox response evidence.

## Decision request

Owner approval is required for the semantic expansion before implementation.

**Current recommendation:** approve the boundary/categories, while making live/fixture response verification a mandatory prerequisite for the concrete field subset.
## Additional SDK-schema evidence (not Sandbox payload evidence)

A direct inspection of the official SDK source adds useful schema-level evidence without changing the implementation boundary:

- The SDK `Project` type is a thin wrapper over the API result dictionary; it does not define a stable typed field schema in the SDK itself.
- The SDK defines `ProjectType.FIXED = 0` and `ProjectType.HOURLY = 1`.
- The SDK request helpers expose project-detail projections for full description, job details, qualification details, and location details.
- The SDK request helpers expose user-detail projections including basic user details, country details, reputation, and employer reputation.
- SDK helper constructors show project budget data with `minimum`, optional `maximum`, and optional `currency_id`; currency data can contain `id`, `code`, `sign`, `name`, and related metadata; job data can contain `id`, `name`, category, and related metadata.
- The official SDK search implementation returns the provider's `result` payload directly; it does not normalize or validate the response shape for us.

This evidence strengthens the candidate mapping categories, but it does **not** prove that a particular Sandbox search/detail response contains every field, with the same path, type, or semantic meaning. Concrete mapping remains blocked on captured provider response evidence.
