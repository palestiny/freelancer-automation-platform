# Design Gate — Metric Direction Policy

**Status:** APPROVED — V1 explicit metric-polarity interpretation policy.

Interpret neutral performance movement (`INCREASED`, `DECREASED`, `NO_CHANGE`) only according to an explicit metric policy.

Metric polarity: HIGHER_IS_FAVORABLE, LOWER_IS_FAVORABLE, DIRECTION_NEUTRAL.

Interpretation: FAVORABLE, UNFAVORABLE, NEUTRAL, NOT_INTERPRETABLE.

Rules:
1. Raw evidence remains neutral and unchanged.
2. Favorable/unfavorable interpretation requires explicit policy.
3. Missing policy yields NOT_INTERPRETABLE; no inference from metric names.
4. A neutral metric always yields NEUTRAL.
5. Policy is provider-independent and versionable by its consumer.
6. No score, ranking, lifecycle mutation, learning mutation, portfolio action, or execution.
