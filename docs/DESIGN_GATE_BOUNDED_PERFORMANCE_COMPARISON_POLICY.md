# Design Gate — Bounded Performance Comparison Policy

**Status:** APPROVED — V1 deterministic comparison-policy foundation.

## Purpose

Turn eligible historical evidence into a controlled descriptive comparison without introducing forecasting or statistical inference.

**Current Evidence + Eligible Baseline → Comparison Policy → Performance Trend / Explicit Rejection**

## V1 Decisions

### D-084 — Comparison Requires an Eligible Baseline

A baseline must first satisfy the explicit baseline eligibility policy. Comparison must not bypass evidence or freshness requirements.

### D-085 — Current Evidence Has Minimum Sufficiency

The current aggregate must contain a configurable minimum observation count and minimum average evidence quality.

### D-086 — Current and Baseline Windows Must Be Temporally Ordered

The current window must start at or after the baseline window end. Overlapping comparison periods are rejected.

### D-087 — Comparison Policy Produces Descriptive Evidence

The policy may produce a PerformanceTrend, but it does not forecast, rank businesses, or choose an action.

## V1 Domain

PerformanceComparisonPolicy:
- minimum current observations
- minimum current evidence quality

assess_performance_comparison(...):
- evaluates baseline eligibility
- validates current sufficiency
- validates business/metric/unit compatibility
- validates temporal ordering
- returns either a descriptive trend or an explicit rejection reason

Reasons:
- BASELINE_NOT_ELIGIBLE
- INSUFFICIENT_CURRENT_OBSERVATIONS
- INSUFFICIENT_CURRENT_EVIDENCE_QUALITY
- INCOMPATIBLE_CONTEXT
- OVERLAPPING_WINDOWS

## Boundary

No forecasting, statistical significance, anomaly detection, seasonality, automatic action, policy mutation, ranking, scoring, or external execution.
