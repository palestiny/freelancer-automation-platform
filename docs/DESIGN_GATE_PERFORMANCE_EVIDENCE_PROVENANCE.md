# Design Gate — Performance Evidence Provenance

**Status:** APPROVED — V1 provenance-preserving aggregation foundation.

## Purpose

Prevent derived performance evidence from losing the source context needed to interpret, compare, and audit it.

**Source Observations → Provenance-Preserving Aggregate → Context-Safe Comparison / Learning**

## V1 Decisions

### D-088 — Derived Aggregates Preserve Source-Type Provenance

A performance aggregate must preserve the distinct `PerformanceSourceType` values represented by its source observations. Observation identifiers alone are not sufficient as a directly inspectable provenance summary.

### D-089 — Aggregation Does Not Invent Provenance

Source types are copied from normalized observations. The aggregate must not infer, rename, or otherwise manufacture source provenance.

### D-090 — Comparison Requires Compatible Provenance Context

A descriptive comparison is valid only when current and baseline aggregates have the same source-type provenance. This prevents a metric with identical name/unit from being compared across different evidence domains without an explicit future policy.

### D-091 — Raw Observation Lineage Remains Authoritative

Aggregates remain derived views. Source observation identifiers are preserved, and the raw observations remain the authoritative evidence.

## V1 Domain

`PerformanceAggregate` now preserves:

- `observation_ids`
- `source_types`
- business identity
- metric/unit
- explicit time window
- actual/expected summaries
- evidence quality

`PerformanceComparisonPolicy` additionally validates source-type compatibility before producing a trend.

## Boundary

This gate does not introduce:

- source reliability scoring
- causal attribution
- statistical inference
- forecasting
- automatic policy mutation
- persistence
- provider integrations
- external execution
- source-type ranking

Those concerns require separate policy/design decisions.