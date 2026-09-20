# Design Gate — Controlled Experiment Exposure Evidence

**Status:** APPROVED — V1 non-executing exposure confirmation boundary.

## Purpose

Separate deterministic assignment from evidence that a subject was actually exposed to the assigned variant.

## V1 contract

- An exposure record references an existing assignment identity.
- Exposure identity is immutable and caller-provided.
- One assignment may have at most one exposure record in V1.
- Exposure timestamp is timezone-aware.
- The persisted variant and subject must match the referenced assignment.
- Recording exposure is evidence capture only; it does not schedule, invoke providers, deliver content, mutate experiment lifecycle, reallocate subjects, or optimize allocation.
- Assignment remains the authoritative allocation identity; exposure is a separate observation of delivery/exposure.

## Boundary

The application service validates assignment context and writes through a replaceable repository port. SQLite is the V1 reference adapter. Production delivery/exposure integrations remain outside the boundary.
