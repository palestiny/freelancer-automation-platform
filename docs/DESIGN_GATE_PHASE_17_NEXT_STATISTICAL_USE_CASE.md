# Design Gate — Phase 17 Next Statistical Use Case: Historical Mean Comparison

**Status:** PROPOSED — design only; no runtime implementation authorized.

## Purpose

Select a concrete consumer for the existing Student's t mean-uncertainty artifact before adding another statistical method.

## Proposed V1 Question

Given two non-overlapping historical windows for the same business, metric, and unit:

> Is there statistical evidence that the observed means differ?

This is an inferential comparison of historical samples, not a prediction of future performance.

## Candidate Method

A two-sample comparison of means is the candidate method. The implementation must not be selected until the assumptions and exact test contract are approved.

The design review must explicitly decide between:
- Welch's two-sample t-test, which does not require equal population variances; or
- another justified method if the evidence/use case requires it.

No method is authorized by this document alone.

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

Implementation is blocked until the exact statistical method, assumptions, sample-size floor, significance level, and result semantics are explicitly approved and recorded in the decision log.
