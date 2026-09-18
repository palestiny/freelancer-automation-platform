# Design Gate — Phase 17 Statistical Learning & Inference

**Status:** PROPOSED — design boundary only; no statistical implementation is authorized by this gate.

## Purpose

Define the boundary for the next measurement capability without silently expanding deterministic Phase 16 semantics.

## Problem

Phase 16 can describe historical performance and derive evidence-aware learning signals from deterministic variance rules. It does not determine whether an observed pattern is statistically meaningful, persistent, anomalous, or predictive.

Phase 17 may address that gap only through explicit statistical semantics.

## Proposed V1 Scope

A future implementation may provide provider-independent statistical evidence such as:

- sample-size-aware descriptive statistics
- dispersion measures
- confidence intervals where assumptions are explicit
- hypothesis-test results where a concrete decision use case justifies them
- deterministic eligibility checks for whether a statistical method is applicable
- explicit method/result provenance

## Required Boundaries

Statistical results must remain:

- derived evidence, not facts
- separate from raw observations
- separate from policy decisions
- explicit about assumptions and method
- explicit about insufficient data
- reproducible from identified observations
- scoped to one business and compatible metric/unit context unless a future gate explicitly permits broader scope

## Non-Goals

This gate does not authorize:

- forecasting
- causal inference
- automatic anomaly remediation
- automatic policy mutation
- automatic baseline selection
- provider ranking
- portfolio allocation
- financial execution
- automatic experiment execution
- AI model selection
- persistence or API infrastructure

## Design Questions Before Implementation

1. Which concrete statistical question has product value?
2. What minimum sample sizes and assumptions are required per method?
3. How are non-normal, sparse, zero, or missing observations represented?
4. Which outputs are descriptive versus inferential?
5. How is method/provenance lineage preserved?
6. How do statistical results compose with existing evidence quality and source reliability without replacing them?
7. What explicit handoff consumes a statistical result?

## Decision Gate

No implementation should begin until one concrete statistical use case is selected, its assumptions are documented, and RED tests define insufficient-data and invalid-context behavior.

Phase 16 remains closed and unchanged while this gate is open.


## Statistical Contract Proposal — V1 Mean Uncertainty

### Method boundary

The first statistical implementation should use a **Student's t confidence interval for the population mean** when its applicability conditions are satisfied. This is a bounded descriptive-inference tool for uncertainty around a sample mean; it is not a forecast and does not establish causality.

### Proposed assumptions

V1 requires:

- observations belong to one business, metric, unit, and explicit window
- each contributing observation has a finite numeric actual value
- observations are treated as approximately independent for the interval's interpretation
- the population distribution is treated as approximately normal when the sample is small; for larger samples, the method relies on the usual robustness of the sample mean under appropriate conditions
- confidence level is explicit and fixed by policy; proposed V1 default is **95%**
- sample standard deviation is defined only when at least two observations are available

The implementation must not silently remove invalid observations. Invalid or insufficient input must produce an explicit non-applicable result.

### Minimum sample size

The proposed minimum is **2 observations** because the t interval cannot estimate sample variance from one observation. This is a mathematical applicability floor, not a claim that two observations provide strong evidence.

Evidence-quality and source-reliability policies remain separate gates. A sample can be mathematically applicable while still being weak evidence for downstream decisions.

### Output contract

A statistical result should preserve:

- business_id
- metric_name
- unit
- observation window
- observation_ids
- sample_size
- sample_mean
- sample_standard_deviation
- confidence_level
- interval_lower
- interval_upper
- method identifier
- explicit applicability/result status

The result must be reproducible from the identified observations and explicit method parameters.

### Insufficient / invalid data

The result must explicitly distinguish at least:

- INSUFFICIENT_OBSERVATIONS — fewer than 2 valid observations
- INVALID_CONTEXT — mixed business, metric, unit, or incompatible context
- INVALID_VALUE — non-finite numeric input
- INAPPLICABLE — method assumptions or required conditions are not satisfied

No fallback method is selected automatically in V1.

### Consumer boundary

The statistical result is an evidence artifact. It may later be composed with performance comparison or learning, but V1 must not mutate `PerformanceTrend`, `LearningSignal`, policy, business state, or execution state automatically.

### Implementation gate

Runtime implementation remains blocked until this proposal is reviewed against the repository's existing aggregate/window contracts and RED tests define every invalid/insufficient-data path above. The confidence level, method name, and policy ownership must be explicit in code rather than hidden constants.


## Runtime Status

**Status: APPROVED — V1 first statistical use case implemented.**

The first Phase 17 statistical slice is now implemented as a provider-independent domain evidence artifact for uncertainty around an observed historical mean inside an explicit `PerformanceWindow`.

### Implemented contract

- Student's t confidence interval for a population mean.
- Default confidence level: 95%.
- Mathematical minimum: 2 valid observations.
- Explicit statuses for insufficient observations, invalid context, invalid values, and applicability.
- Observation IDs are preserved as authoritative lineage.
- Business, metric, unit, and explicit time window are preserved.
- Runtime implementation uses the Python standard library; no statistical provider dependency was introduced.

### Assumptions and boundary

The result is an inferential estimate under the method's stated assumptions. The domain does not claim to prove independence or normality from raw observations. Consumers must treat those assumptions as part of applicability context and must not interpret a 95% confidence interval as a probability statement about the fixed population mean.

The implementation does not perform forecasting, causal inference, anomaly detection, automatic policy mutation, learning-policy mutation, portfolio allocation, or external execution.

### Verification

PR #17 was merged after GitHub Actions CI run **277** completed successfully with the full test suite: **206 passed**.
