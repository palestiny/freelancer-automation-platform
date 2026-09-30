# Success Confidence Criterion Semantics V1

## Status

**APPROVED — semantic boundary accepted on 2026-09-30.**

Issue #482 records the approved high-level direction: **Option B — Evidence Sufficiency**.

This document turns that direction into the concrete provider-independent semantic contract. Owner approval is recorded on Issue #482. TDD/implementation may now proceed only within the boundary defined here.

## Purpose

Success Confidence V1 determines whether the immutable evidence snapshot is sufficient to establish explicit success conditions under a versioned evaluation policy.

The word **confidence** is retained as the criterion name, but V1 does **not** assign a numeric confidence value, probability, model score, or prediction.

Semantic question:

> Does the available evidence establish that the policy-defined success conditions are satisfied?

The answer is categorical:

- `PASS`
- `FAIL`
- `INSUFFICIENT_DATA`
- `NOT_APPLICABLE`

## Semantic Boundary

`External observations → normalized evidence → immutable EvaluationContext → Success Policy → deterministic Success Evaluation → CriterionEvaluation`

Success Confidence consumes evidence already present in `EvaluationContext`.

It does not:
- fetch provider data;
- inspect mutable provider objects;
- calculate effort, economics, risk, or capability compatibility;
- generate hidden evidence;
- invoke an AI model;
- predict future success;
- mutate policy;
- authorize or execute an opportunity.

## Ownership Boundaries

**External adapters** own provider-specific observations and transport semantics.

**Evidence / EvaluationContext** owns:
- evidence identity;
- provenance;
- quality;
- observation time;
- derivation lineage;
- uncertainty.

**Existing specialized criteria** retain their semantic ownership:
- Eligibility owns eligibility constraints.
- Requirement Fit owns exact capability compatibility.
- Estimated Effort owns effort estimates and effort constraints.
- Economic Fit owns economic calculations/constraints.
- Client / Project Risk owns risk constraints.

**Success Confidence** owns only the interpretation of explicit success conditions.

It may consume specialized outputs only when they are represented as explicit evidence under the existing evidence model and explicitly permitted by policy. A criterion outcome itself is never automatically evidence.

## V1 Success-Condition Model

V1 uses explicit success-condition constraints rather than a generalized expression language or numeric scoring system.

Each condition identifies:

- stable `condition_id`;
- explicit semantic scope;
- signal identity;
- expected/allowed state values;
- evidence references.

### Success Condition Scopes

V1 uses explicit scopes to prevent semantic ambiguity:

- `DELIVERY`
- `REQUIREMENT`
- `DEADLINE`
- `DEPENDENCY`
- `ACCEPTANCE`

Historical/experimental evidence is **not** a separate scope. It is an evidence-kind/provenance characteristic that may support a condition when policy explicitly permits it.

### Operator vocabulary

V1 exposes only:

`ALLOWED_VALUES`

Evidence value must be one of the explicitly permitted values.

Numeric thresholds/ranges remain owned by specialized criteria such as Estimated Effort and Economic Fit. Success Confidence consumes an explicit categorical feasibility/state result instead of independently recomputing it.

A generalized boolean/expression language is out of scope.

## Evidence Contract

Success-condition evidence must exist in immutable `EvaluationContext` and preserve:

- stable evidence identity;
- semantic value;
- provenance;
- `EvidenceKind`;
- quality;
- observed/derived time where applicable;
- derivation references;
- uncertainty.

The evaluator must not create hidden evidence.

### Evidence kinds allowed to establish V1 success conditions

The evaluator may use:

- `FACT`
- `OBSERVATION`
- `ESTIMATE`
- `EXPERIMENT_RESULT`

The following do not establish V1 success conditions:

- `ASSUMPTION`
- `HYPOTHESIS`
- `FORECAST`

An AI-generated assertion is not evidence merely because an AI system produced it.

If a future policy permits another evidence kind, that is a new semantic decision and must preserve provenance, quality, lineage, uncertainty, and policy identity.

### Evidence quality

For required evidence:

- `PRESENT_AND_USABLE` may establish a condition;
- `PRESENT_BUT_AMBIGUOUS` → unresolved;
- `PRESENT_BUT_STALE` → unresolved;
- `PRESENT_BUT_LOW_QUALITY` → unresolved;
- `MISSING` → unresolved.

Evidence quality is not itself a success outcome.

## Condition Evaluation Semantics

For each required condition:

1. Resolve only evidence explicitly referenced by the condition.
2. Evidence must match the condition's scope and signal identity.
3. Referenced evidence must exist in the immutable context.
4. Evidence must have an allowed kind.
5. Evidence must be `PRESENT_AND_USABLE`.
6. Evidence value must establish one of the condition's expected values.
7. Multiple incompatible usable values without explicit precedence produce unresolved evidence.

At criterion level:

1. Explicit violation with no unresolved required evidence → **FAIL**.
2. Violation plus unresolved required evidence → **INSUFFICIENT_DATA**.
3. No violation but unresolved required evidence → **INSUFFICIENT_DATA**.
4. All required conditions satisfied → **PASS**.
5. Explicit policy/context non-applicability → **NOT_APPLICABLE**.

Conservative rule:

> Unresolved required evidence never becomes PASS through inference.

Missing evidence is insufficient data, not failure.

## Contradictory Evidence

If multiple usable evidence items for the same condition establish incompatible states and no explicit precedence rule exists:

**→ `INSUFFICIENT_DATA`**

The evaluator must not resolve contradictions using:
- recency alone;
- source popularity;
- implicit provider trust;
- AI confidence;
- hidden heuristics.

V1 has no precedence mechanism.

If precedence is introduced later, it must be explicit and versioned as part of the policy contract.

## Scope / Signal Isolation

Success Confidence must not infer success from unrelated fields.

Examples:

- A populated `Opportunity.required_capabilities` does not prove requirement completion.
- Requirement Fit = `PASS` does not automatically prove delivery success.
- Estimated Effort = `PASS` does not automatically prove deadline success.
- Economic Fit = `PASS` does not prove client acceptance.
- Client / Project Risk = `PASS` does not prove successful completion.

If future policy needs cross-criterion information, it must first be represented as explicit derived evidence with its own identity, derivation references, kind, provenance, quality, uncertainty, and policy permission.

No circular derivation is permitted. Success Confidence cannot consume evidence whose derivation ultimately depends on the Success Confidence result being evaluated.

## Derived Evidence

V1 permits derived evidence when it is explicitly represented in `EvaluationContext` before evaluation.

A derived success-condition signal must:
- have its own evidence identity;
- reference source evidence through `derivation_refs`;
- preserve uncertainty;
- carry explicit evidence kind and quality;
- be permitted by the selected policy.

The evaluator must never manufacture hidden derived evidence.

## Temporal Semantics

`observed_at` is provenance metadata, not an implicit freshness algorithm.

V1 does not infer freshness or validity from timestamps alone.

If evidence is stale, that state must be represented through `EvidenceQuality.PRESENT_BUT_STALE` or an explicitly modeled future evidence policy.

The evaluator must not silently prefer the newest source.

## Deadline and Delivery Semantics

Success Confidence does not calculate deadline feasibility.

For example, a condition may expect:

- `WITHIN_DEADLINE`
- `DELIVERABLE`
- `BLOCKERS_RESOLVED`

Those states must come from explicit evidence.

If a separate component calculates deadline feasibility, that calculation belongs to its own semantic owner. The resulting value can enter `EvaluationContext` as `ESTIMATE` or another explicitly appropriate evidence kind with provenance and lineage.

This avoids duplicating:
- effort calculations;
- calendar calculations;
- scheduling algorithms;
- dependency resolution logic.

## Requirement / Acceptance Semantics

Success Confidence does not duplicate Requirement Fit.

Requirement Fit answers whether required capabilities are compatible/supported.

Success Confidence may evaluate an explicit success condition such as:
- `ACCEPTANCE_CRITERIA_COMPLETE`;
- `REQUIREMENT_ACCEPTANCE_STATE`;

when such evidence exists and is explicitly referenced by policy.

It must not infer acceptance from capability matching.

## Historical / Experiment Evidence

`EXPERIMENT_RESULT` may be accepted when a policy explicitly defines a success condition whose evidence is an experiment result.

A historical result does not automatically become a prediction of current success.

Past evidence may establish the condition only when the condition itself explicitly defines that historical/experimental result as sufficient evidence.

No implicit temporal generalization is allowed.

## AI Evidence Boundary

An AI-generated statement such as “this project will probably succeed” is not a Success Confidence evidence item merely because a model produced it.

If future policy permits AI-derived evidence, it must enter the same evidence model with explicit provenance, kind, quality, derivation lineage, uncertainty, and policy permission.

V1 creates no special AI-confidence pathway.

## NOT_APPLICABLE and Empty Conditions

Success Confidence is `NOT_APPLICABLE` only when policy/context explicitly establishes that the criterion does not apply.

The following are not sufficient:
- no evidence available;
- incomplete opportunity data;
- provider retrieval failure;
- absence of a known success condition.

For consistency with the existing criterion implementations, an empty configured success-condition set is treated as `NOT_APPLICABLE`.

This is a policy-shape convention, not an inference that success is irrelevant. Explicit context `NOT_APPLICABLE` remains authoritative.

## Determinism and Result Preservation

Given the same Opportunity, immutable EvaluationContext, and versioned EvaluationPolicy, evaluation must return the same `CriterionEvaluation`.

No wall-clock lookup, external provider call, AI invocation, random sampling, or mutable state participates in V1.

The result preserves:
- policy identity;
- criterion identity;
- outcome;
- relevant evidence refs;
- missing evidence;
- uncertainty;
- rationale where implemented.

V1 introduces no `score`, numeric confidence, probability, ranking, weight, or calibration value.

## Design Trade-offs

### Option A — Numeric confidence / probability

**Rejected for V1.**

It requires statistical meaning, calibration semantics, population assumptions, uncertainty modeling, and validation strategy outside this deterministic boundary.

### Option B — Evidence Sufficiency

**Selected and owner-approved.**

It gives “Success Confidence” a concrete domain meaning without pretending evidence availability is a calibrated probability. It is deterministic, explainable, and testable.

### Option C — AI-generated confidence

**Rejected for V1.**

Model confidence is not automatically domain evidence and would create an alternative semantic owner outside the versioned evidence/policy model.

## Approved V1 Decisions

The owner approved the following concrete decisions on Issue #482:

1. `condition_id + scope + signal + expected_values + evidence_refs` is the condition contract.
2. Scopes are `DELIVERY`, `REQUIREMENT`, `DEADLINE`, `DEPENDENCY`, and `ACCEPTANCE`.
3. `ALLOWED_VALUES` is the only V1 operator.
4. Allowed evidence kinds are `FACT`, `OBSERVATION`, `ESTIMATE`, and `EXPERIMENT_RESULT`.
5. `ASSUMPTION`, `HYPOTHESIS`, and `FORECAST` do not establish PASS.
6. V1 has no contradiction precedence; conflicting usable values produce `INSUFFICIENT_DATA`.
7. Criterion outcomes are not evidence.
8. Derived evidence is allowed only when explicitly represented with lineage before evaluation.
9. Success Confidence performs no hidden deadline, effort, economic, or risk calculations.
10. Empty condition set produces `NOT_APPLICABLE`, consistent with the existing criterion pattern.
11. V1 introduces no numeric confidence, probability, score, ranking, weighting, prediction, or autonomous execution.

## Proposed TDD Boundary

After owner approval, TDD implements only:

1. `SuccessCondition` domain contract;
2. `EvaluationPolicy.success_confidence_conditions`;
3. deterministic `SuccessConfidenceEvaluator`;
4. EvaluationContext integration;
5. validation for condition identity, scope, evidence references, supported operators, and duplicate IDs;
6. tests for admissible/unadmissible evidence kinds;
7. tests for quality, missing evidence, contradictions, violation/unresolved composition, and explicit non-applicability;
8. tests for context subject mismatch and deterministic repeatability;
9. tests proving no score/confidence/probability fields;
10. documentation reconciliation.

Provider integration, AI integration, statistical modeling, ranking, and execution remain outside the TDD slice.

## Exit Criteria

- Option B remains approved;
- condition identity and scopes are approved;
- operator semantics are explicit;
- evidence-kind rules are explicit;
- quality/contradiction semantics are explicit;
- temporal and derived-evidence boundaries are explicit;
- cross-criterion isolation is explicit;
- empty-condition behavior is explicit;
- no numeric confidence/probability semantics exist;
- owner approval is recorded on Issue #482.
- TDD issue is created as the next implementation slice.

Implementation remains limited to the approved TDD boundary.
