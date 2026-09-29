# Success Confidence Criterion Semantics V1

## Status

**DESIGN COMPLETE — owner approval required before TDD.**

Issue #482 records the approved high-level direction: **Option B — Evidence Sufficiency**.

## Purpose

Success Confidence V1 determines whether available evidence is sufficient to establish explicitly defined success conditions for an opportunity under a selected evaluation policy and immutable evidence snapshot.

Despite its name, V1 does **not** calculate a confidence percentage, probability, score, or prediction.

The semantic pipeline is:

`explicit success conditions → evidence requirements → immutable EvaluationContext → deterministic sufficiency evaluation → CriterionEvaluation`

It answers: “Do we have sufficient admissible evidence to establish the policy-defined success conditions?” It does not answer: “What is the probability that this opportunity will succeed?”

## Ownership Boundary

**Evidence / EvaluationContext** owns normalized evidence identity, provenance, quality, timing, derivation lineage, and uncertainty.

**Success Confidence** owns interpretation of explicit success conditions under a versioned policy.

**Business Economics** owns economic calculations. Success Confidence does not recreate them.

**Experiment / learning domains** own historical experiment observation and statistical analysis. Success Confidence may consume explicitly represented experiment-result evidence but does not perform statistical inference.

**AI providers** may produce evidence through the normal evidence pipeline, but an AI assertion is not evidence merely because AI produced it.

## V1 Success-Condition Model

V1 introduces an explicit policy-side success-condition contract. Each condition identifies:

- stable `condition_id`;
- stable success signal identity;
- deterministic comparison/operator semantics;
- expected/allowed value(s);
- explicit evidence references.

V1 deliberately keeps the operator vocabulary small. The initial operator is:

- `ALLOWED_VALUES` — evidence value must be one of the explicitly permitted values.

Future threshold/range operators require a separate design decision.

## Success Signal Scope

V1 does not define one universal success formula.

A policy may explicitly require evidence for signals such as:

- requirement completion / acceptance state;
- delivery feasibility state;
- deadline feasibility state;
- dependency or blocker resolution state;
- explicit client/project acceptance condition;
- relevant historical or experiment outcome state.

These are admissible semantic examples, not mandatory fields on every opportunity.

## Evidence Contract

Success evidence must already exist in immutable `EvaluationContext` before evaluation and preserve:

- stable evidence identity;
- signal identity and applicable scope in the value contract;
- `EvidenceKind`;
- provenance;
- observed/derived time where applicable;
- quality;
- derivation references;
- uncertainty.

The evaluator must not create hidden evidence.

### Admissible Evidence Kinds

V1 may establish success conditions from:

- `FACT`;
- `OBSERVATION`;
- `ESTIMATE`, only when policy explicitly defines the condition in terms of an estimate/feasibility state;
- `EXPERIMENT_RESULT`, when explicitly represented as evidence relevant to the condition.

These do not establish a V1 success condition by themselves:

- `ASSUMPTION`;
- `HYPOTHESIS`;
- `FORECAST`;
- unsupported AI assertions.

The evaluator must not silently promote one evidence kind into another.

## Evidence Quality

For required evidence:

- `PRESENT_AND_USABLE` may establish a condition;
- `PRESENT_BUT_AMBIGUOUS` → unresolved;
- `PRESENT_BUT_STALE` → unresolved;
- `PRESENT_BUT_LOW_QUALITY` → unresolved;
- `MISSING` → unresolved.

Evidence quality is not itself a success outcome.

## Contradictory Evidence

If multiple usable evidence items referenced by the same condition establish incompatible values and policy defines no explicit precedence:

**→ `INSUFFICIENT_DATA`**

Do not resolve contradictions by source reputation, recency alone, AI confidence, hidden provider preference, or arbitrary ordering.

Any future precedence rule must be explicit and versioned.

## Condition and Criterion Outcomes

For each applicable required condition:

1. Explicit unacceptable/violating evidence with no unresolved required evidence → violated.
2. Any unresolved required evidence → unresolved.
3. All required evidence establishes the expected success state → satisfied.

At criterion level:

- explicit violation with no unresolved required evidence → `FAIL`;
- violation plus unresolved required evidence → `INSUFFICIENT_DATA`;
- no violation but unresolved required evidence → `INSUFFICIENT_DATA`;
- all required conditions satisfied → `PASS`;
- explicit policy/context non-applicability → `NOT_APPLICABLE`.

“Not proven” is not silently treated as “failed”.

### Missing Evidence

Missing required evidence means `INSUFFICIENT_DATA`, not failure.

Example: if policy requires `deadline_feasibility = FEASIBLE` and no such evidence exists, the result is `INSUFFICIENT_DATA`.

### Violation Plus Unresolved Evidence

If one usable evidence item establishes a violation but another required referenced evidence item is unresolved, the result is `INSUFFICIENT_DATA`.

## Cross-Criterion Isolation

A criterion outcome is not automatically evidence for Success Confidence.

- Eligibility = PASS does not prove successful delivery.
- Requirement Fit = PASS does not prove acceptance.
- Estimated Effort = PASS does not prove deadline feasibility.
- Economic Fit = PASS does not prove client acceptance.
- Client / Project Risk = PASS does not prove successful completion.

If future policy needs cross-criterion information, it must first be represented as explicit derived evidence with its own identity, derivation references, kind, provenance, quality, uncertainty, and policy permission.

No circular derivation is permitted. Success Confidence cannot consume evidence whose derivation ultimately depends on the Success Confidence result being evaluated.

## Historical and Experiment Evidence

Historical or experiment evidence may support a success condition only when already represented as explicit evidence with provenance and an applicable `EvidenceKind`.

Success Confidence does not calculate historical success rates, estimate probabilities, perform statistical tests, extrapolate sample results, or generalize a historical result without an explicit evidence contract.

An `EXPERIMENT_RESULT` is an evidence input, not an automatic probability of future success.

## AI Evidence Boundary

An AI-generated statement such as “this project will probably succeed” is not a Success Confidence evidence item merely because a model produced it.

If future policy permits AI-derived evidence, it must enter the same evidence model with explicit provenance, kind, quality, derivation lineage, uncertainty, and policy permission.

V1 creates no special AI-confidence pathway.

## NOT_APPLICABLE

Success Confidence is `NOT_APPLICABLE` only when policy/context explicitly establishes that the criterion does not apply.

The following are not sufficient:

- no evidence available;
- incomplete opportunity data;
- provider retrieval failure;
- absence of a known success condition.

If a policy supplies no success conditions, that absence must be an explicit policy decision; otherwise the policy is invalid or evaluation must reject it rather than infer non-applicability.

## Determinism and Result Preservation

Given the same Opportunity, immutable EvaluationContext, and versioned EvaluationPolicy, evaluation must return the same `CriterionEvaluation`.

No wall-clock lookup, external provider call, AI invocation, random sampling, or mutable state participates in V1.

The result preserves policy identity, criterion identity, outcome, relevant evidence refs, missing evidence, uncertainty, and rationale where implemented.

V1 introduces no `score`, numeric confidence, probability, ranking, weight, or calibration value.

## Trade-offs

### Option A — Numeric confidence / probability

**Rejected for V1.** It requires a statistical/predictive definition, calibration semantics, population assumptions, uncertainty model, and validation strategy outside this deterministic boundary.

### Option B — Evidence Sufficiency

**Selected and owner-approved.** It gives “Success Confidence” a concrete domain meaning without pretending evidence availability is a calibrated probability. It is deterministic, explainable, and testable.

### Option C — AI-generated confidence

**Rejected for V1.** Model confidence is not automatically domain evidence and would create an alternative semantic owner outside the versioned evidence/policy model.

## Non-goals

V1 does not introduce:

- numeric confidence;
- probability of success;
- machine-learning prediction;
- universal success formula;
- scoring or weighting;
- ranking;
- automatic selection/rejection;
- bidding;
- payment;
- execution;
- portfolio decisions;
- automatic policy mutation;
- statistical inference;
- hidden cross-criterion dependencies;
- hidden evidence generation.

## Proposed TDD Boundary

After owner approval, TDD implements only:

1. `SuccessCondition` domain contract;
2. `EvaluationPolicy.success_confidence_conditions`;
3. deterministic `SuccessConfidenceEvaluator`;
4. EvaluationContext integration;
5. validation for condition identity, evidence references, supported operators, and duplicate IDs;
6. tests for admissible/unadmissible evidence kinds;
7. tests for quality, missing evidence, contradictions, violation/unresolved composition, and explicit non-applicability;
8. tests for context subject mismatch and deterministic repeatability;
9. tests proving no score/confidence/probability fields;
10. documentation reconciliation.

Provider integration, AI integration, statistical modeling, ranking, and execution remain outside the TDD slice.

## Exit Criteria

- Option B semantics remain owner-approved;
- success-condition identity/operator semantics are explicit;
- evidence kind/quality/provenance/lineage rules are explicit;
- contradiction/unresolved semantics are explicit;
- historical/experiment evidence boundary is explicit;
- cross-criterion and circular-dependency boundaries are explicit;
- `NOT_APPLICABLE` semantics are explicit;
- deterministic behavior is explicit;
- no score/probability/prediction/ranking is introduced;
- owner approval is recorded on Issue #482;
- implementation begins only through a separate TDD issue.
