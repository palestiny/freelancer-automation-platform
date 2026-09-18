# Project State

## Current Phase

**Phase 0 — Product & Architecture — Business Economics & Growth approved; Domain TDD in progress**

## Product Direction

The platform is now explicitly a **Business Automation OS**, initially validated through the freelance-work market.

Freelancing remains the first concrete market, not the permanent architectural boundary.

## Completed

- Repository created and verified.
- Shared engineering working rules established.
- Modular-monolith direction established.
- Marketplace-independent architecture established.
- Opportunity Intelligence gate approved.
- Six Opportunity Evaluation dimensions committed.
- Economic/growth direction approved.
- Business Economics domain foundation implemented.

## Committed Opportunity Evaluation Dimensions

1. Eligibility
2. Requirement Fit
3. Estimated Effort
4. Economic Fit
5. Client / Project Risk
6. Success Confidence

Criterion-level evidence and uncertainty remain mandatory.

Overall outcomes:

- QUALIFIED
- NOT_QUALIFIED
- REVIEW_REQUIRED

Numeric scoring is not required for the first domain slice.

## Committed Economic Model

The first economic slice models:

- expected revenue
- expected effort
- platform fee
- capability cost
- operating cost
- revision allowance
- success confidence
- expected cost
- expected profit
- expected margin
- expected profit per hour
- risk-adjusted profit

Economic estimates are derived data and do not mutate Opportunity identity.

## Current Implementation Progress

Opportunity Intelligence contains:

- Opportunity identity representation
- Evaluation policy representation
- Eligibility criterion evaluation
- PASS / FAIL / INSUFFICIENT_DATA criterion outcomes
- QUALIFIED / NOT_QUALIFIED / REVIEW_REQUIRED overall outcomes
- Criterion-level evidence
- Evaluation without mutating Opportunity identity
- Re-evaluation of the same Opportunity under different policies
- Budget eligibility boundaries

Business Economics now contains:

- immutable EconomicEstimate
- explicit cost components
- expected cost calculation
- expected profit calculation
- expected margin calculation
- expected profit/hour calculation
- risk-adjusted profit calculation
- validation of invalid economic inputs

## Current Boundary

The active implementation boundary is domain behavior only.

Allowed now:

- domain models
- domain services
- domain value objects
- domain tests

Still outside the current slice:

- marketplace SDKs
- real marketplace credentials
- persistence
- HTTP/API
- UI
- AI provider dependencies

## Next Step

Complete the remaining Opportunity Intelligence domain behaviors, then continue Business Economics with a dedicated Resource Economics / Capacity Design Gate.

The next economic gate should define:

- resource identity
- resource cost
- capacity
- availability
- opportunity cost
- actual-vs-expected economics
- portfolio constraints

## Long-Term Learning Loop

**Expected → Actual → Variance → Learning Signal → Controlled Policy/Experiment Improvement**

Learning must not silently rewrite policy.

## Project Health Rule

A meaningful increment is done only after applicable design, RED/GREEN TDD, review, refactoring, documentation, passing tests, commit/push, and project-state update.
