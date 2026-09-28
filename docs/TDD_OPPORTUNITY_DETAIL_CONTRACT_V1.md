# TDD — Opportunity Detail Contract V1

## Status

**COMPLETED — provider-neutral contract implementation merged**

## Scope

The owner-approved provider-neutral semantic boundary for opportunity detail is implemented and merged without claiming that any field is verified against a live Freelancer Sandbox payload.

The implementation currently establishes:
- provider-neutral observation fields for classification, economics, capabilities, provenance, and minimal client evidence;
- normalized domain representation for those fields;
- explicit missing/optional semantics;
- synthetic contract fixtures only.

## Evidence rule

The fixture under `tests/fixtures/` is explicitly synthetic and provider-neutral. It is **not** Freelancer response evidence.

No Freelancer-specific response path is encoded in the domain/application contract.

Actual Freelancer mappings remain a separate provider-validation task and require a captured response before adapter mapping tests are added.

## Completion evidence

- PR #452 merged by squash into `main`.
- CI passed on head SHA `516cbae4a195b62f028b7fc05a84c3138a6b13d4` before merge.
- Synthetic fixture remains explicitly non-provider evidence.
- Concrete Freelancer mapping remains deferred until verified Sandbox response evidence is available.

## TDD boundary

### RED

Tests must prove:
1. rich provider-neutral observations can be represented;
2. normalization preserves verified-neutral values;
3. optional fields remain absent when unavailable;
4. invalid types/empty capability entries are rejected.

### GREEN

Implement the minimum contract needed by those tests.

### HARDEN

Verify:
- Decimal budget precision;
- immutable observation/domain objects;
- no provider SDK imports in domain/application;
- no fabricated defaults;
- no automatic scoring/ranking;
- no provider-specific enum leakage.

## Non-goals

- real Freelancer payload mapping;
- AI extraction;
- scoring/ranking;
- proposal/bidding;
- payment;
- production access;
- automatic policy mutation.
