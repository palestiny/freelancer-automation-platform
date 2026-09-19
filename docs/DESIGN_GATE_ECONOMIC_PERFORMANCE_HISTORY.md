# Design Gate — Economic Performance History

**Status:** APPROVED — V1 actual-vs-expected economic evidence foundation.

## Purpose

Preserve realized economic outcomes against an explicit economic estimate so profitability and stability can be measured over time without rewriting the original estimate.

## V1 Model

Each economic outcome belongs to one business and records estimate identity, observed time, actual revenue, actual cost, and actual effort hours.

Derived: actual profit, actual margin when revenue is non-zero, revenue/cost/profit/effort variance versus the estimate.

## Rules

1. The original estimate remains immutable evidence of what was expected.
2. Actual outcomes are separate evidence.
3. Missing/zero revenue does not invent a margin.
4. Negative actual revenue/cost/effort is invalid; zero effort is allowed only when explicitly representing an outcome with no recorded effort.
5. Business identity is mandatory and history cannot mix businesses.
6. Variance is actual minus expected.
7. This slice does not score, rank, forecast, allocate capital, mutate policy, or execute financial actions.
8. Historical aggregation and statistical inference remain separate consumers.
