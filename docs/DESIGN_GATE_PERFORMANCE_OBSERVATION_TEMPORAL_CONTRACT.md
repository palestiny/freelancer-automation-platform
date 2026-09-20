# Design Gate — Performance Observation Temporal Contract

**Status:** APPROVED — V1 temporal validity hardening for authoritative performance observations.

## Decision

Performance observation timestamps must be timezone-aware datetimes. The domain will reject naive timestamps at construction time.

## Rationale

Performance history, explicit windows, freshness, baseline eligibility, and statistical comparisons perform temporal ordering. Allowing a naive timestamp creates an ambiguous clock basis and can surface as delayed comparison failures when mixed with timezone-aware boundaries.

## Contract

- observed_at must be a datetime.
- observed_at must be timezone-aware.
- No implicit local-time or UTC assumption is made for naive values.
- Persistence adapters preserve the timezone-aware ISO representation.
- This is validation only; no timestamp normalization, clock inference, or current-time lookup is introduced.
