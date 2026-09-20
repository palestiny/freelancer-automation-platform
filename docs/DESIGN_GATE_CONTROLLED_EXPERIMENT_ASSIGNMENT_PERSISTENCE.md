# Design Gate — Controlled Experiment Assignment Persistence

**Status:** APPROVED — V1 authoritative assignment persistence boundary.

## Purpose

Persist the authoritative experiment assignment created from an explicit deterministic allocation decision so later observations can reference stable assignment identity.

## V1 contract

- An assignment is created only from an explicit allocation decision.
- Assignment identity is caller-provided and immutable.
- `experiment_id + subject_id` is unique in the reference store.
- The persisted variant must equal the allocation decision variant.
- Assignment persistence does not expose/execute the subject, schedule work, mutate experiment lifecycle, reallocate, optimize weights, or invoke providers.
- Existing observations remain authoritative evidence and must reference an assignment identity.
- Re-saving the same assignment identity is rejected; conflicting assignment for the same experiment/subject is rejected explicitly.

## Boundary

Persistence is an infrastructure concern behind an application repository port. SQLite is the V1 reference adapter only and does not commit a production database choice.
