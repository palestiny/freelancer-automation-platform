# Design Gate — Phase 17 Next Statistical Use Case: Historical Mean Comparison

**Status:** APPROVED — V1 design contract committed; runtime implementation follows this gate.

## Purpose

Select a concrete consumer for the existing Student's t mean-uncertainty artifact before adding another statistical method.

## Proposed V1 Question

Given two non-overlapping historical windows for the same business, metric, and unit:

> Is there statistical evidence that the observed means differ?

This is an inferential comparison of historical samples, not a prediction of future performance.

## Committed Method — Welch's Two-Sample t-Test

V1 uses **Welch's two-sample t-test** to compare two historical sample means without assuming equal population variances.

The test is two-sided. V1 significance level is **alpha = 0.05**.

Minimum mathematical sample size is **2 observations in each window**, because each sample requires a variance estimate.

The result is inferential evidence about a difference between the two observed sample means under the method's assumptions. It is not a forecast, causal conclusion, or statement that either period is representative of all future periods.

## Required Context

The future result must preserve:
- business_id
- metric_name
- unit
- both explicit windows
- both observation-ID lineages
- sample sizes
- method identifier
- explicit significance level
- method-specific evidence
- explicit result status

Both windows must be same-business, same metric/unit, non-overlapping, and contain finite numeric actual values. No automatic window selection is permitted.

## Assumption Boundary

The domain must not infer independence, distributional assumptions, or sampling design. Applicability must be explicit and consumer-declared, following the existing Phase 17 boundary.

## Required Statuses

At minimum:
- INSUFFICIENT_OBSERVATIONS
- INVALID_CONTEXT
- INVALID_VALUE
- INAPPLICABLE
- APPLICABLE

## Output Boundary

The result is an evidence artifact only. It must not automatically mutate PerformanceTrend, LearningSignal, policy, business state, choose a baseline, trigger an experiment, execute external actions, allocate capital, or forecast future values.

Observation-level evidence quality and source reliability remain separate evidence dimensions and are not replaced by statistical significance.

## RED Requirements Before Implementation

Tests must define:
1. empty/insufficient windows
2. mixed business/metric/unit context
3. non-finite values
4. overlapping windows
5. explicit applicability failure
6. duplicate observation lineage
7. invalid significance level
8. reproducible method/provenance output
9. a known reference calculation

## Decision Gate

**APPROVED.** The exact method, two-sided alpha of 0.05, minimum sample size of 2 per window, explicit applicability, non-overlap requirement, and result semantics are committed for V1.

Implementation must still follow RED → GREEN and preserve the non-executing evidence boundary.
