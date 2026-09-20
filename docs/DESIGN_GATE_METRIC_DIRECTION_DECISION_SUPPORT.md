# Design Gate — Metric Direction Interpretation in Evidence Decision Support

**Status:** APPROVED — V1 explicit polarity interpretation consumer.

## Purpose

Connect the existing metric-polarity policy to the existing performance evidence decision-support artifact without changing raw evidence or creating an action recommendation.

## V1 Contract

Input:
- existing PerformanceTrend
- existing StatisticalEvidenceComposition
- explicit MetricDirectionPolicy, or no policy

Output additionally includes:
- metric_direction_interpretation:
  - FAVORABLE
  - UNFAVORABLE
  - NEUTRAL
  - NOT_INTERPRETABLE

Rules:
1. Raw movement remains INCREASED / DECREASED / NO_CHANGE.
2. Favorable/unfavorable is derived only from the explicit metric policy.
3. Missing policy produces NOT_INTERPRETABLE for non-zero movement.
4. DIRECTION_NEUTRAL produces NEUTRAL.
5. Statistical evidence and metric polarity remain separate dimensions.
6. No score, ranking, recommendation, lifecycle mutation, learning mutation, portfolio action, authorization, or execution is introduced.
7. Existing descriptive/inferential posture semantics remain unchanged.
