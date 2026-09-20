# Design Gate — Controlled Experiment Statistical Comparison

**Status:** APPROVED — V1 concrete statistical consumer of controlled-experiment variant evidence.

## Purpose

Extend the existing controlled-experiment evidence pipeline with one inferential comparison between exactly two declared variants. This is a new statistical use case, not a new generic statistics framework.

## V1 Contract

Input:
- one experiment identity
- exactly two distinct variant identities
- one metric and unit
- ready observations for each variant
- explicit applicability declaration
- explicit alpha

Method:
- two-sided Welch two-sample t-test
- alpha defaults to 0.05
- minimum mathematical sample size: 2 observations per variant

Output preserves:
- experiment_id
- variant identities
- metric/unit
- observation IDs for both groups
- sample sizes
- group means
- mean difference
- t-statistic
- Welch degrees of freedom
- p-value
- alpha
- method
- explicit status

Statuses:
- APPLICABLE
- INSUFFICIENT_OBSERVATIONS
- INVALID_CONTEXT
- INVALID_VALUE
- INAPPLICABLE

## Assumptions

Applicability assumptions remain consumer-declared. The domain does not prove independence, normality, randomization, treatment assignment validity, or causal identification from observations.

## Safety / Boundary

1. This result is an evidence artifact only.
2. No winner selection or ranking is produced.
3. Statistical significance does not establish causality.
4. No experiment lifecycle mutation occurs.
5. No automatic allocation, rollout, budget change, policy mutation, learning mutation, or execution occurs.
6. Evidence quality and source reliability remain separate eligibility gates.
7. Raw experiment observations remain authoritative lineage.
8. No automatic fallback or method selection is introduced.
9. A new statistical method still requires its own dedicated design gate.

## Decision

Welch two-sample comparison is reused as the statistical method because it is already an approved Phase 17 method and does not require equal-variance assumptions. The experiment-specific identity is explicit so historical business-window comparison and controlled-variant comparison remain distinct use cases.
