# TDD: Economic Fit Criterion V1

**Status: IMPLEMENTATION MERGED — CI verification in progress.**

## Approved boundary

Economic Fit evaluates explicit economic evidence against explicit policy constraints. It does not calculate economics, generate forecasts, rank opportunities, or execute actions.

Business Economics remains the owner of reusable economic calculations. Economic Fit interprets those evidence artifacts inside an immutable `EvaluationContext`.

## RED

PR #476 introduced the implementation-first TDD surface for:

- all five V1 economic metrics;
- MINIMUM and MAXIMUM constraints;
- explicit policy violations;
- missing, ambiguous, stale, low-quality, and missing referenced evidence;
- wrong metric identity;
- unit and currency mismatch without conversion;
- conflicting usable evidence without precedence;
- conservative violation + unresolved evidence handling;
- uncertainty preservation;
- explicit NOT_APPLICABLE;
- no inference from Opportunity fields;
- policy/context identity;
- duplicate constraint/reference validation;
- supported metric/operator validation;
- finite threshold validation;
- no recomputation from revenue/cost components.

The RED suite was intentionally created before the implementation. GitHub did not surface a workflow run for the intermediate RED commit through the available connector.

## GREEN

Implemented:

- `app.domain.economic_fit.EconomicMetric`
- `app.domain.economic_fit.EconomicComparisonOperator`
- `app.domain.economic_fit.EconomicConstraint`
- `EvaluationPolicy.economic_fit_constraints`
- `app.application.economic_fit.EconomicFitEvaluator`

The evaluator:

- consumes only `EvaluationContext`;
- requires `EvidenceKind.ESTIMATE` for V1 expected-economic values;
- matches metric, unit, and currency exactly;
- never performs currency/unit conversion;
- detects conflicting usable values without precedence;
- applies only explicit MINIMUM/MAXIMUM comparisons;
- returns PASS, FAIL, INSUFFICIENT_DATA, or NOT_APPLICABLE according to the approved semantics;
- preserves evidence references and uncertainty;
- does not calculate Business Economics metrics.

## HARDEN

Validation coverage includes:

- immutable/frozen constraint semantics;
- supported metric and operator identity;
- finite numeric thresholds;
- unique constraint identities;
- unique evidence references;
- context subject identity;
- evidence quality;
- explicit applicability;
- conservative handling of violation plus unresolved evidence;
- no score/confidence fields;
- no inference from opportunity text/fields;
- no duplicate economics calculation.

## Merge

PR #476 was merged squash into `main` as:

`cbadd00e216cbf7bbfa2447b19e69bd17b38b45b`

The available GitHub connector reported no workflow run for that merge commit. This verification branch intentionally contains only this documentation reconciliation so the repository CI workflow can validate the current `main` implementation without changing runtime behavior.

## Completion gate

The implementation slice is code-complete and merged. Completion remains pending until this verification CI run is observed successfully and project state is reconciled.

No scoring, ranking, forecasting, portfolio allocation, payment/capital movement, automatic selection, bidding, or execution was introduced.
