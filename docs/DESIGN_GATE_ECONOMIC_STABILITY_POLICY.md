# Design Gate — Economic Stability Policy

**Status:** APPROVED — V1 explicit eligibility policy for stable profitability.

## Purpose

Translate descriptive economic-health evidence into an explainable stability eligibility result without creating a universal business score or automatic portfolio posture.

## V1 Inputs

- EconomicHealthEvidence
- minimum observations
- minimum profitable outcome rate
- minimum average actual profit
- maximum allowed profit standard-deviation ratio relative to average profit

## V1 Reasons

- ELIGIBLE
- INSUFFICIENT_OBSERVATIONS
- PROFITABILITY_RATE_BELOW_THRESHOLD
- AVERAGE_PROFIT_BELOW_THRESHOLD
- INSUFFICIENT_VARIABILITY_DATA
- PROFIT_VARIABILITY_ABOVE_THRESHOLD

## Rules

1. Policy thresholds are explicit inputs, not hidden constants.
2. Stable profitability is a policy-derived eligibility result, not an intrinsic business fact.
3. The policy does not rank businesses or produce a universal score.
4. No PROTECT/GROW/HARVEST/EXIT posture is produced.
5. No forecast or causal inference is introduced.
6. No capital allocation, policy mutation, or financial execution.
7. Variability ratio requires positive average profit and at least two observations.
8. Failure reasons are deterministic and explainable.
