# Design Gate — Economic Performance Aggregation

**Status:** APPROVED — V1 deterministic historical aggregation for realized economic outcomes.

## Purpose

Provide a bounded historical view over realized economic outcomes so profitability and actual-vs-expected behavior can be measured without mutating estimates or making business decisions.

## V1 Metrics

For one business and explicit time window:
- actual revenue average
- actual cost average
- actual profit average
- actual effort average
- profit variance average
- revenue variance average
- cost variance average
- effort variance average
- actual outcome count
- source outcome IDs

## Rules

1. Raw economic outcomes remain authoritative evidence.
2. Aggregates are derived views and never rewrite EconomicEstimate.
3. The window is explicit and start-inclusive/end-exclusive.
4. Business identity is mandatory and cannot be mixed.
5. Empty windows return no aggregate rather than zero-filled economics.
6. Averages are arithmetic means over selected outcomes.
7. No universal economic score, forecast, ranking, capital allocation, portfolio action, or execution is introduced.
8. This slice does not decide whether a business is healthy, stable, scalable, or worth protecting.
