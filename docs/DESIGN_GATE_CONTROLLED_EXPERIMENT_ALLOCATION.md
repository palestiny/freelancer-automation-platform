# Design Gate — Controlled Experiment Allocation

**Status:** APPROVED — V1 provider-independent deterministic allocation foundation.

## Purpose

Turn an approved experiment allocation policy into a reproducible variant assignment decision without persistence, scheduling, provider execution, or lifecycle mutation.

## V1 Contract

An immutable allocation plan contains:
- experiment identity
- ordered variant names
- explicit integer allocation weights in basis points
- a non-empty allocation salt

Weights must be positive and sum to 10,000 basis points.

Allocation uses SHA-256 over the explicit experiment identity, subject identity, and salt. The resulting deterministic bucket maps to exactly one declared variant according to cumulative weights.

## Decisions

- Allocation is deterministic and reproducible.
- Allocation weights are explicit policy input; no automatic optimization is performed.
- Variant order is part of the plan contract and is therefore immutable.
- The allocator produces an assignment decision only; it does not persist an assignment or call a provider.
- Reallocation, scheduling, experimentation lifecycle, exposure enforcement, and statistical analysis remain separate boundaries.
- A changed plan/salt is a different allocation context; existing assignments are not rewritten.

## Safety

The allocator rejects duplicate/empty variants, invalid weights, invalid identity, and empty salt. It never silently falls back to another variant.
