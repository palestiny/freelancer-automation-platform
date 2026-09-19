# Design Gate — Evidence Decision Context

**Status:** APPROVED — V1 explicit context for downstream evidence interpretation.

## Purpose

Preserve why a composed performance-evidence result exists and which evidence artifacts support it, without turning evidence into an automatic business decision.

## V1 Contract

Create an immutable context containing:
- business identity
- metric/unit
- descriptive direction
- inferential status
- combined evidence posture
- statistical observation lineage
- explicit source references
- evidence-quality values used by the statistical composition

Rules:
1. Source references are provenance only.
2. Context must preserve, not recompute, prior evidence semantics.
3. No score/rank/recommendation.
4. No policy, learning, lifecycle, portfolio, or execution mutation.
5. Missing provenance is explicit and invalid.
