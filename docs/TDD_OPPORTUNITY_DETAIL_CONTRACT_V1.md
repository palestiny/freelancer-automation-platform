# TDD — Opportunity Detail Contract V1

## Status

**IN PROGRESS — provider-neutral contract implementation**

## Scope

Implement the owner-approved semantic boundary for opportunity detail without claiming that any field is verified against a live Freelancer Sandbox payload.

The implementation currently establishes:
- provider-neutral observation fields for classification, economics, capabilities, provenance, and minimal client evidence;
- normalized domain representation for those fields;
- explicit missing/optional semantics;
- synthetic contract fixtures only.

## Evidence rule

The fixture under `tests/fixtures/` is explicitly synthetic and provider-neutral. It is **not** Freelancer response evidence.

No Freelancer-specific response path is encoded in the domain/application contract.

Actual Freelancer mappings remain a separate provider-validation task and require a captured response before adapter mapping tests are added.

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
