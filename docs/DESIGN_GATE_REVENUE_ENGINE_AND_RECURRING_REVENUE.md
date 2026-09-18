# Design Gate — Revenue Engine & Recurring Revenue

**Status:** APPROVED — V1 domain direction committed; revenue-contract foundation implemented.

## Purpose

The platform must distinguish revenue as an actual business outcome from revenue assumptions, forecasts, and pricing hypotheses.

The revenue domain provides a provider-independent contract for recording expected and realized revenue while making recurring economics explicit.

## V1 Boundary

**Business Model → Revenue Contract → Revenue Event → Economic Measurement → Learning**

A revenue contract describes how a business expects to earn money. A revenue event records realized revenue.

V1 distinguishes:

- ONE_TIME
- RECURRING

Recurring revenue requires an explicit recurring period.

## Revenue Contract

A contract contains:

- id
- model identifier
- revenue type
- amount
- currency
- recurring period when applicable
- status

Amounts are nonnegative. Currency is explicit.

## Revenue Event

A realized revenue event contains:

- contract identifier
- amount
- currency
- recognized timestamp

The event is an observation of realized revenue, not a forecast.

## Safety Boundary

V1 does not process payments, move money, issue refunds, reconcile provider statements, or connect to payment processors.

Payment execution remains an external capability behind authorization and policy.

## Recurring Economics

Recurring revenue is a business characteristic that can feed:

- Economic Profile
- profitability analysis
- demand stability
- retention/churn analysis
- capacity planning
- portfolio policy

It does not imply guaranteed retention or passive income.

## Evidence Boundary

Revenue events are observations of actual business outcomes. Expected revenue remains an estimate/forecast until realized.

Learning follows:

**Expected → Actual → Variance → Learning**

No revenue observation silently changes pricing policy, business model, or portfolio posture.

## Non-Goals

- payment processing
- invoicing
- tax accounting
- refunds
- provider reconciliation
- automatic pricing optimization
- customer billing automation
- capital allocation

## Design Decisions

1. Revenue contracts are provider-independent.
2. Recurring revenue is explicit, not inferred from a label.
3. Actual revenue is represented separately from expected revenue.
4. Payment execution remains outside the domain.
5. Revenue observations feed learning but do not silently rewrite policy.

## Design Gate Outcome

Approved for V1 implementation of the provider-independent revenue foundation.
