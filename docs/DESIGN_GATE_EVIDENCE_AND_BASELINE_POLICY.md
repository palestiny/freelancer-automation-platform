# Design Gate — Evidence & Baseline Policy

**Status:** APPROVED — V1 evidence-aware baseline eligibility foundation.

## Purpose

Prevent weak, sparse, or stale historical aggregates from being treated as usable baselines.

**Performance History → Aggregate → Evidence/Recency Policy → Baseline Eligibility → Trend Analysis**

## V1 Decisions

### D-079 — Baseline Eligibility Is Policy, Not Evidence

A historical aggregate is raw derived evidence. Whether it is suitable as a baseline is a separate policy decision.

### D-080 — Baseline Eligibility Requires Sufficient Observations

A baseline must meet a configurable minimum observation count. The policy must not manufacture confidence from a single or sparse observation.

### D-081 — Baseline Eligibility Requires Evidence Quality

A baseline must meet a configurable minimum average evidence quality. Evidence quality is a bounded property of the contributing observations, not a guarantee of correctness.

### D-082 — Baseline Freshness Is Explicit

A baseline may have a maximum age relative to an explicit `as_of` timestamp. The domain does not infer recency from the current clock.

### D-083 — Ineligibility Must Be Explainable

When a baseline is rejected by policy, the result preserves a deterministic reason. The policy does not silently discard evidence.

## V1 Domain

`PerformanceBaselinePolicy`:
- minimum observations
- minimum average evidence quality
- maximum age

`assess_baseline(aggregate, policy, as_of)` returns a deterministic eligibility result containing:
- eligible / ineligible
- reason

V1 reasons:
- ELIGIBLE
- INSUFFICIENT_OBSERVATIONS
- INSUFFICIENT_EVIDENCE_QUALITY
- STALE_BASELINE

A baseline with an end timestamp after `as_of` is not considered stale; the policy rejects it as **FUTURE_BASELINE** so temporal ordering remains explicit.

## Boundary

This slice does not:
- forecast
- infer statistical significance
- detect seasonality
- detect anomalies
- choose a baseline automatically
- mutate business policy
- rank businesses
- score opportunities
- execute actions

Baseline selection remains an application/policy concern. The domain only evaluates a supplied aggregate against explicit policy.

## Acceptance Criteria

- Policy thresholds are validated.
- Observation count is checked deterministically.
- Evidence quality is checked deterministically.
- Baseline age is checked against explicit `as_of`.
- Future baselines are rejected.
- Reasons are stable and inspectable.
- Raw aggregate provenance remains unchanged.
- No business state or policy is mutated.
