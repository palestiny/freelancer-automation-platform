# Economic Fit Criterion Semantics V1

## Status

**APPROVED — semantic boundary accepted on 2026-09-28.**

Owner approval is recorded on Issue #473.

## Purpose

Economic Fit determines whether an opportunity satisfies explicit economic requirements under a selected evaluation policy and the available evidence snapshot.

It is a criterion evaluator, not a profitability predictor, financial advisor, ranking engine, or economic calculation engine.

## Ownership Boundary

**Business Economics** owns reusable economic calculations and derived economic estimates.

**Opportunity Intelligence / Economic Fit** owns policy interpretation: whether explicit economic evidence satisfies explicit user/policy constraints.

Economic Fit must not duplicate formulas already owned by Business Economics.

## V1 Economic Evidence

Economic evidence is represented in the immutable `EvaluationContext` and must preserve:

- stable evidence identity;
- economic metric identity;
- value;
- unit;
- currency where applicable;
- `EvidenceKind`;
- provenance;
- quality;
- observation/derivation time where applicable;
- derivation references;
- uncertainty.

Derived economic values remain `EvidenceKind.ESTIMATE`.

An economic value is not treated as established merely because it appears in `Opportunity` fields.

## V1 Metric Boundary

V1 supports explicit policy constraints over these reusable economic metrics when evidence for the metric exists:

- `expected_profit`
- `expected_margin`
- `expected_profit_per_hour`
- `expected_cost`
- `expected_revenue`

No universal economic score is introduced.

### Metric semantics

- **expected_profit**: expected revenue minus expected cost, as produced by Business Economics evidence.
- **expected_margin**: expected profit divided by expected revenue when defined by Business Economics.
- **expected_profit_per_hour**: expected profit divided by expected effort hours.
- **expected_cost**: sum of explicitly modeled expected economic costs.
- **expected_revenue**: expected revenue represented by the economic evidence model.

Economic Fit consumes these values; it does not recompute them.

## Constraint Model

Each Economic Fit constraint has:

- stable `constraint_id`;
- metric identity;
- comparison operator;
- threshold value;
- unit;
- currency where applicable;
- evidence references.

V1 comparison operators are:

- `MINIMUM` — evidence value must be greater than or equal to threshold;
- `MAXIMUM` — evidence value must be less than or equal to threshold.

V1 uses exact unit and currency matching. No silent conversion is permitted.

## Evidence Semantics

For a required constraint:

- usable matching evidence establishes the metric value;
- missing evidence → `INSUFFICIENT_DATA`;
- `PRESENT_BUT_AMBIGUOUS` → `INSUFFICIENT_DATA`;
- `PRESENT_BUT_STALE` → `INSUFFICIENT_DATA`;
- `PRESENT_BUT_LOW_QUALITY` → `INSUFFICIENT_DATA`;
- wrong metric identity → not usable for that constraint;
- wrong unit/currency → not usable and therefore `INSUFFICIENT_DATA`;
- conflicting usable values without explicit policy precedence → `INSUFFICIENT_DATA`.

Evidence quality never directly becomes PASS or FAIL.

## Outcome Composition

For applicable required constraints:

1. Any explicit policy-defined violation established by usable evidence → `FAIL`.
2. No violation, but any required evidence remains unresolved → `INSUFFICIENT_DATA`.
3. All required constraints satisfied → `PASS`.
4. Explicitly established non-applicability → `NOT_APPLICABLE`.

A violation plus unresolved evidence is conservative: `INSUFFICIENT_DATA`, because the complete economic state is not established.

No other criterion outcome is automatically treated as economic evidence.

## Derived Evidence and Lineage

Business Economics outputs may be represented as derived `ESTIMATE` evidence with derivation references to the underlying revenue, cost, effort, and other source evidence.

Economic Fit may consume the derived metric only when its provenance, quality, and lineage are preserved.

AI-generated economic assertions are not evidence merely because an AI system produced them. If future policy explicitly permits them, they must enter the evidence model with provenance, kind, quality, and lineage.

## Cross-Criterion Isolation

Economic Fit does not consume another criterion's outcome as evidence.

For example:

- Requirement Fit = PASS does not prove economic feasibility.
- Estimated Effort = PASS does not itself establish an economic value.
- Success Confidence is not silently injected into economic calculations.

If a future policy needs a cross-criterion-derived economic input, it must be represented as explicit derived evidence with lineage and an explicit semantic decision.

## NOT_APPLICABLE

Economic Fit is `NOT_APPLICABLE` only when policy/context explicitly establishes that the criterion does not apply.

An absence of economic evidence is not sufficient to make the criterion not applicable.

## Non-goals

V1 does not introduce:

- economic scoring;
- weights;
- ranking;
- profitability prediction;
- probability/forecast generation;
- portfolio allocation;
- capital movement;
- payment execution;
- currency conversion;
- AI-generated policy;
- automatic opportunity selection;
- bidding or execution.

## Design Trade-off Decision

**Approved Option C: explicit economic requirements + deterministic evidence-based evaluator.**

This keeps calculation and policy interpretation separate, preserves evidence lineage, and prevents Economic Fit from becoming a hidden scoring or financial decision engine.

## Exit Criteria

- semantic boundary approved;
- metric and comparison semantics explicit;
- evidence quality/conflict semantics explicit;
- Business Economics ownership preserved;
- no scoring/ranking introduced;
- owner approval recorded;
- implementation proceeds only through a separate TDD issue.
