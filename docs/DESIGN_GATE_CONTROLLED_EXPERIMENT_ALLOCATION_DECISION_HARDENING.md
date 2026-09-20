# Design Gate — Controlled Experiment Allocation Decision Hardening

**Status:** APPROVED — V1 auditability hardening for deterministic allocation.

## Decision

The allocator must expose an immutable allocation decision artifact rather than only a variant string. The artifact preserves experiment identity, subject identity, selected variant, and deterministic bucket.

## Rules

1. Allocation remains deterministic and provider-independent.
2. The decision artifact is evidence of the allocation decision, not experiment exposure evidence.
3. No assignment persistence, scheduling, provider execution, lifecycle mutation, reallocation, or optimization is introduced.
4. Existing variant allocation behavior remains unchanged.
5. The deterministic bucket is preserved for auditability and reproducibility.
