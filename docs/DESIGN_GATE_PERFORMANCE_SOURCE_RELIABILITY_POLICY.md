# Design Gate — Performance Source Reliability Policy

**Status:** APPROVED — V1 provider-independent source-reliability policy foundation.

## Purpose

Make source reliability an explicit policy concern without conflating it with observation-level evidence quality.

**Source Provenance → Reliability Policy → Reliability Assessment → Evidence Eligibility**

## V1 Decisions

### D-092 — Source Reliability Is Policy-Derived

Source reliability is not stored as an immutable fact on a performance observation. A policy assigns reliability values to known source types and evaluates whether the current evidence context satisfies a required minimum.

### D-093 — Observation Evidence Quality Remains Separate

`evidence_quality` describes the quality of a specific normalized observation. Source reliability describes the policy-assigned suitability of a source type. One must not silently replace the other.

### D-094 — Mixed-Source Evidence Uses the Weakest Configured Source

When an aggregate contains multiple source types, V1 uses the minimum configured reliability among represented sources. This is conservative, deterministic, and avoids inventing weights between heterogeneous evidence domains.

### D-095 — Missing Reliability Configuration Blocks Eligibility

A source type without an explicit reliability configuration cannot be assumed reliable. The assessment returns an explainable missing-policy result.

### D-096 — Reliability Does Not Rank or Execute

The V1 reliability assessment is an eligibility input only. It does not rank providers, infer causal correctness, mutate source observations, execute actions, or change business policy.

## V1 Domain

`PerformanceSourceReliabilityPolicy` contains:

- minimum required reliability
- explicit reliability value for each configured `PerformanceSourceType`

`SourceReliabilityAssessment` contains:

- eligibility
- deterministic reason
- minimum reliability represented by the aggregate when available

## Boundary

This gate does not introduce:

- provider-specific trust algorithms
- causal attribution
- statistical inference
- forecasting
- automatic policy mutation
- external execution
- persistence
- source ranking
- universal reliability values outside explicit policy

Future work may define how reliability policies are versioned, evidenced, calibrated, or combined with observation-level evidence quality.
