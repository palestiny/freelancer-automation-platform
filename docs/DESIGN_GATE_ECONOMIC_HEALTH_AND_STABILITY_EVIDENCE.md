# Design Gate — Economic Health & Stability Evidence

**Status:** APPROVED — V1 descriptive economic health/stability evidence.

## Purpose

Expose a normalized descriptive view of realized economic performance that makes profitability and stability measurable without turning them into a universal business score or automatic posture.

## V1 Metrics

For one business and explicit window:
- outcome count
- profitable outcome count
- loss outcome count
- profitable outcome rate
- average actual profit
- minimum actual profit
- maximum actual profit
- sample standard deviation of actual profit when at least two outcomes exist
- average actual margin when margin observations exist
- average actual profit per effort hour when positive effort is recorded

## Rules

1. Raw EconomicPerformanceOutcome remains authoritative.
2. Estimates and realized outcomes remain separate.
3. Missing margin values remain missing; they are not treated as zero.
4. Stability is descriptive evidence, not a score.
5. No universal economic health score is introduced.
6. No automatic PROTECT/GROW/HARVEST/EXIT posture is derived.
7. No forecast, causal inference, capital allocation, or financial execution.
8. Business isolation and explicit windows remain mandatory.
9. Empty windows remain absent.
10. At least two observations are required to expose profit standard deviation; otherwise it is None.
