# Design Gate — Performance Trend & Baseline Analysis

**Status:** APPROVED — V1 deterministic trend/baseline foundation.

## Purpose

Compare explicit historical performance windows without turning observations into forecasts or policy decisions.

**Historical Observations → Window Aggregates → Baseline Comparison → Trend Evidence**

## V1 Decisions

### D-075 — Trend Analysis Requires Explicit Windows
Trend comparison requires an explicit current window and baseline window. The domain does not infer periods implicitly.

### D-076 — Baselines Are Historical Comparisons
A baseline is a comparison reference derived from observed history. It is not a target, forecast, or guarantee.

### D-077 — Trend Direction Is Descriptive
V1 reports the arithmetic change between comparable aggregates. It does not label the change as good or bad because metric semantics differ.

### D-078 — Missing Data Remains Missing
If either window has no observations, no comparison is produced. No values are invented.

## V1 Boundary

A trend comparison contains:
- metric and unit
- current and baseline windows
- current and baseline averages
- absolute change
- relative change when baseline average is non-zero
- source observation identifiers for both windows
- evidence quality for each side

No forecasting, statistical significance, seasonality, anomaly detection, policy mutation, or automatic action is included.
