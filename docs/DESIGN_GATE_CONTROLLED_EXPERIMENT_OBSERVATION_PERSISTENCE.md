# Design Gate — Controlled Experiment Observation Persistence

**Status:** APPROVED — V1 authoritative metric-observation persistence with exposure lineage enforcement.

## Purpose

Persist controlled-experiment metric observations durably while preventing observations from entering the authoritative evidence store without a matching actual exposure context.

## V1 Contract

- Experiment observations remain immutable evidence artifacts.
- An observation must reference an existing assignment identity.
- Before persistence, the application service must resolve the assignment's exposure and validate exposure-compatible lineage.
- Experiment, assignment, subject, and variant identity must match the exposure.
- Observation time must be at or after exposure time.
- Multiple metric observations may belong to one exposure.
- Observation identity is unique.
- The repository is provider-independent; SQLite is the V1 reference adapter.
- Reads preserve experiment identity and chronological observation ordering.

## Boundary

This is persistence and attribution validation only. It does not infer causality, calculate significance, select winners, mutate experiment lifecycle, allocate traffic, schedule exposure, or execute providers.
