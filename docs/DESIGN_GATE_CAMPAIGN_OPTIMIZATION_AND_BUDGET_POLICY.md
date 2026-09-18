# Design Gate — Campaign Optimization & Budget Policy

**Status:** APPROVED — V1 domain direction committed; provider-independent optimization recommendation foundation implemented.

## Purpose

Extend campaign measurement into controlled optimization without conflating observation, policy, recommendation, authorization, and external spend.

Flow: **Campaign → Performance Observation → Optimization Policy → Recommendation → Authorization → External Execution → New Observation**

## Decisions

- **D-052:** Optimization produces recommendations, not silent spend changes.
- **D-053:** Budget limits are hard safety constraints.
- **D-054:** Optimization requires sufficient evidence.
- **D-055:** Optimization policy is changeable.
- **D-056:** Financial spend remains explicitly authorized.

## V1

The policy contains minimum observations, target ROAS, maximum CAC, maximum budget adjustment, and allowed actions. Recommendations support CONTINUE, INCREASE_BUDGET, DECREASE_BUDGET, and PAUSE.

Recommendations never execute external actions. Insufficient evidence cannot produce a budget-changing recommendation. Recommended budgets cannot exceed the campaign budget limit.

## Non-goals

No ad-platform integrations, automatic spend, payment processing, statistical significance testing, attribution engine, multi-campaign allocation, portfolio capital allocation, or provider-specific optimization algorithms.
