# Design Gate — Baseline Reliability Integration

**Status:** APPROVED — V1 baseline eligibility can incorporate explicit source-reliability policy.

## Purpose

Connect the new source-reliability policy to baseline eligibility without replacing observation evidence quality or changing comparison semantics.

**Performance Aggregate → Evidence Quality + Source Reliability + Freshness → Baseline Eligibility**

## V1 Decisions

### D-097 — Baseline Eligibility May Require Source Reliability

A baseline policy may optionally require a source-reliability policy. Existing baseline policies without one retain their previous behavior.

### D-098 — Source Reliability Is an Additional Gate

Source reliability does not replace minimum observation count, observation-level evidence quality, or freshness checks. All applicable requirements must pass.

### D-099 — Reliability Failures Are Explainable

Baseline eligibility distinguishes insufficient source reliability from missing source-reliability configuration.

### D-100 — Comparison Semantics Remain Stable

The comparison layer continues to consume `BaselineEligibility`; it does not duplicate source-reliability logic.

## Boundary

This gate does not introduce source ranking, calibration, forecasting, causal inference, persistence, provider integrations, automatic policy mutation, or external execution.