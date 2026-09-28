# Design Gate: Estimated Effort Criterion Semantics V1

**Status: APPROVED — semantic boundary accepted on 2026-09-28.**

## Purpose

Define a provider-independent semantic contract for the Estimated Effort criterion before implementation.

## V1 semantic boundary

Estimated Effort evaluates **existing effort evidence**. It does not generate an estimate, predict guaranteed delivery, or infer effort from generic heuristics.

The flow is:

`Opportunity → EvaluationContext → Effort Evidence → Estimated Effort Evaluator → CriterionEvaluation`

The evaluator is deterministic and provider-independent.

## Effort evidence

Effort evidence is represented explicitly as `EvidenceKind.ESTIMATE` and remains distinguishable from facts and observations.

An effort estimate must preserve, where applicable:

- stable evidence identity;
- estimate value and explicit unit;
- scope references identifying what the estimate covers;
- provenance;
- evidence quality;
- uncertainty;
- derivation lineage.

V1 does **not** require a universal `min/expected/max` model, confidence percentage, or estimation algorithm.

### Epistemic rules

- `ESTIMATE` remains `ESTIMATE`.
- `ASSUMPTION` remains `ASSUMPTION`.
- No silent conversion of assumptions into facts.
- No invented hours/days from title, description, budget, generic heuristics, or missing scope.
- AI-generated assertions are not evidence merely because an AI produced them. If accepted by policy, they must retain provenance, kind, quality, and lineage.

## Scope and applicability

A usable effort estimate must be connected to an identifiable scope through evidence references.

Examples:

- missing required scope → `INSUFFICIENT_DATA`;
- ambiguous required scope → `INSUFFICIENT_DATA`;
- stale/low-quality required evidence → `INSUFFICIENT_DATA`;
- explicit non-applicability established by policy/context → `NOT_APPLICABLE`.

Evidence quality is not itself a criterion outcome.

## Outcome semantics

### PASS

`PASS` means policy-required effort evidence is sufficiently supported for the defined evaluation boundary and no explicit policy-defined effort constraint is violated.

The policy defines what evidence is required and, where applicable, what effort constraint must be satisfied.

### FAIL

`FAIL` is allowed only when all of the following hold:

1. the policy explicitly defines an effort constraint;
2. the relevant evidence is usable;
3. the evidence establishes an explicit violation.

A large estimate is not inherently a failure.

### INSUFFICIENT_DATA

`INSUFFICIENT_DATA` applies when required effort evidence cannot support a deterministic policy evaluation, including:

- missing evidence;
- ambiguous evidence;
- stale evidence;
- low-quality evidence;
- contradictory usable estimates without explicit precedence;
- uncertainty whose interpretation is required by policy but cannot be established.

The evaluator must not manufacture a resolution.

### NOT_APPLICABLE

`NOT_APPLICABLE` is returned only when policy/context explicitly establishes that effort evaluation does not apply.

## Conflicting estimates

When multiple usable estimates cover the same evaluation scope and conflict, the evaluator does not average, select, or otherwise reconcile them unless the policy explicitly defines the precedence or composition rule.

Without such an explicit rule, the result is `INSUFFICIENT_DATA`, with the relevant evidence references and uncertainty preserved.

## Uncertainty

Uncertainty is preserved as evidence metadata and is separate from the criterion outcome.

V1 does not introduce a universal uncertainty percentage, confidence score, or numeric tolerance.

If a policy requires a particular uncertainty interpretation, that interpretation must be explicit in the policy/evidence contract. Otherwise uncertainty that prevents deterministic evaluation results in `INSUFFICIENT_DATA`.

## Cross-criterion isolation

Estimated Effort does not silently depend on the outcome of another criterion.

In particular:

- `Requirement Fit = PASS` is not itself effort evidence;
- `Economic Fit` does not determine Estimated Effort;
- criterion outcomes do not silently become evidence.

Estimated Effort may consume provider-independent evidence about scope, constraints, requirements, or other facts when those inputs are explicitly present in the immutable `EvaluationContext`.

A later Economic Fit implementation may consume a derived effort evidence artifact through an explicit evidence/lineage contract.

## Determinism and boundaries

The evaluator must:

- operate only on the supplied immutable `EvaluationContext` and `EvaluationPolicy`;
- make no live provider calls;
- import no provider SDK;
- use no hidden user/profile state;
- use no randomness;
- preserve policy identity/version;
- preserve evidence references, missing evidence, uncertainty, and rationale;
- never mutate policy.

## Design options

### A — Simple fixed estimate fields

Rejected for V1 because fixed fields do not adequately preserve scope, provenance, quality, contradiction, and uncertainty semantics.

### B — Generic estimation/rules engine

Rejected as premature abstraction. V1 needs a small explicit semantic contract, not a general-purpose estimation engine.

### C — Explicit policy-defined effort evidence + deterministic evaluator

**Approved for V1.**

This keeps estimation semantics explicit while leaving future estimation algorithms, AI assistance, aggregation strategies, and richer uncertainty models outside the current boundary.

## Non-goals

This gate does not define:

- an estimation algorithm;
- AI-based effort generation;
- scheduling;
- project management;
- time tracking;
- delivery prediction;
- productivity scoring;
- pricing recommendation;
- economic scoring;
- ranking;
- opportunity selection;
- proposal/bid execution;
- payment;
- execution;
- automatic policy mutation.

## Implementation gate

Implementation may proceed only after this semantic boundary is recorded as approved.

The implementation sequence remains:

**RED → GREEN → HARDEN → DOCUMENT → CI → MERGE → reconcile project state.**

## Owner approval

Approved by the project owner on 2026-09-28:

- Option C is approved.
- Estimated Effort evaluates explicit effort evidence; it does not generate estimates.
- Effort evidence retains scope, provenance, quality, uncertainty, and lineage.
- `FAIL` requires an explicit policy-defined effort constraint and usable evidence establishing violation.
- Conflicting usable estimates without explicit policy precedence produce `INSUFFICIENT_DATA`.
- No universal uncertainty score/tolerance, estimation algorithm, ranking, or cross-criterion outcome dependency is introduced in V1.
