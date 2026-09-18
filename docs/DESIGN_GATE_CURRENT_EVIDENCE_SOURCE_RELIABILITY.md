# Design Gate — Current Evidence Source Reliability

**Status:** APPROVED — V1 comparison policy may explicitly require source reliability for current evidence.

## Purpose

Ensure the current evidence window is subject to the same explicit source-reliability discipline already available for eligible baselines, without duplicating baseline logic.

**Current Aggregate → Current Evidence Policy → Comparison Eligibility → Descriptive Trend**

## V1 Decisions

### D-101 — Current Evidence Reliability Is Optional Policy

`PerformanceComparisonPolicy` may include a source-reliability policy. Existing comparison policies without one retain their previous behavior.

### D-102 — Current Reliability Is an Additional Gate

Current source reliability does not replace current observation-count or evidence-quality requirements. All configured requirements must pass.

### D-103 — Reliability Rejections Remain Explicit

Insufficient reliability and missing source configuration have separate rejection reasons.

### D-104 — Comparison Does Not Duplicate Baseline Reliability

Baseline reliability remains owned by `PerformanceBaselinePolicy`. Current reliability remains owned by `PerformanceComparisonPolicy`. The comparison service composes the two eligibility boundaries.

## Boundary

No provider ranking, reliability calibration, forecasting, causal inference, automatic policy mutation, persistence, or external execution is introduced.
