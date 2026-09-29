# Client / Project Risk Criterion Semantics V1

## Status

**APPROVED — semantic boundary accepted on 2026-09-29.**

Owner approval is recorded on Issue #478.

## Purpose

Client / Project Risk determines whether an opportunity satisfies explicit risk-related requirements under a selected evaluation policy and immutable evidence snapshot.

It is a deterministic criterion evaluator, not a universal risk model, reputation engine, probability predictor, ranking engine, or automatic rejection mechanism.

## Semantic Boundary

`External observations → normalized evidence → immutable EvaluationContext → Risk Policy → deterministic Risk Evaluation → CriterionEvaluation`

Risk evaluation consumes evidence already present in `EvaluationContext`. It does not directly inspect provider objects or mutable opportunity state.

## Ownership Boundary

**External adapters** own provider-specific observations and transport semantics.

**Evidence / EvaluationContext** owns normalized evidence identity, provenance, quality, timing, derivation lineage, and uncertainty.

**Client / Project Risk** owns interpretation of explicit risk constraints under policy.

The Risk evaluator must not become a generic evidence-generation or provider-ranking engine.

## V1 Risk Scopes

Client Risk and Project Risk are distinct semantic scopes.

### Client Risk

Client-risk evidence may describe explicit counterparty or relationship conditions, including:

- contractual/payment-condition signals when explicitly evidenced;
- communication or workflow obligations;
- acceptance and revision conditions attributable to the client relationship;
- other explicitly modeled client-related constraints.

### Project Risk

Project-risk evidence may describe explicit work or delivery conditions, including:

- requirement clarity;
- scope stability or explicitness;
- deadline/time constraints;
- dependencies and blockers;
- project lifecycle/status;
- delivery or acceptance conditions.

The criterion may evaluate both scopes in one policy, but their evidence and constraint identities must preserve scope.

V1 does not collapse Client Risk and Project Risk into a numeric or composite risk score.

## Evidence Contract

Risk evidence must be represented in immutable `EvaluationContext` and preserve:

- stable evidence identity;
- risk signal identity;
- risk scope;
- value/state where applicable;
- unit where applicable;
- `EvidenceKind`;
- provenance;
- observed/derived time where applicable;
- quality;
- derivation references;
- uncertainty.

Evidence quality is not itself a risk outcome.

Required evidence that is:

- missing;
- ambiguous;
- stale;
- low quality;

cannot establish a satisfied risk constraint.

## Policy / Constraint Model

V1 uses explicit policy-defined constraints.

A risk constraint must identify at least:

- stable `constraint_id`;
- risk scope;
- signal identity;
- comparison/operator semantics;
- expected or allowed value(s);
- evidence references.

The V1 operator vocabulary should remain intentionally small and deterministic. A generalized risk expression language is out of scope.

The policy, not the evaluator, defines which risk conditions matter.

## Subjective and Reputation Signals

A provider-supplied reputation, sentiment, trust, or similar signal is not automatically risk evidence merely because it exists.

Such a signal may participate only when its evidence contract explicitly provides:

- stable identity;
- provenance;
- applicable evidence kind;
- quality;
- uncertainty where applicable;
- policy permission.

AI-generated risk assertions are not evidence merely because an AI system produced them.

If a future policy explicitly permits such evidence, it must enter the same evidence model with provenance, quality, kind, and lineage.

## Contradictory Evidence

If multiple usable evidence items establish incompatible values or states and the selected policy provides no explicit precedence rule:

**→ `INSUFFICIENT_DATA`**

The evaluator must not resolve contradictions using:

- implicit source trust;
- recency alone;
- AI confidence;
- hidden provider preferences;
- undocumented heuristics.

If a future policy defines precedence, that precedence must be explicit and versioned as part of the policy contract.

## Derived Risk Evidence

V1 permits derived risk evidence only when it is explicitly represented as evidence before criterion evaluation.

A derived risk signal must:

- have its own stable evidence identity;
- identify derivation references;
- preserve source evidence lineage;
- preserve uncertainty;
- carry explicit evidence kind and quality;
- be allowed by policy.

The Risk evaluator must not recursively manufacture hidden derived evidence as a side effect of evaluation.

## Outcome Semantics

For applicable required constraints:

1. Any explicit policy-defined violation established by usable evidence → `FAIL`.
2. A violation exists but required evidence remains unresolved → `INSUFFICIENT_DATA`.
3. Required evidence is unresolved without an established violation → `INSUFFICIENT_DATA`.
4. All required constraints are satisfied → `PASS`.
5. Policy/context explicitly establishes non-applicability → `NOT_APPLICABLE`.

For mixed evidence, unresolved required evidence must not silently become `PASS`.

The evaluator preserves evidence references, provenance/quality, uncertainty, and policy identity in the resulting criterion evaluation.

## Cross-Criterion Isolation

A criterion outcome is not automatically evidence for Client / Project Risk.

For example:

- Eligibility = PASS does not prove low client risk.
- Requirement Fit = PASS does not prove low project risk.
- Estimated Effort = PASS does not prove a safe deadline.
- Economic Fit = PASS does not prove contractual or delivery safety.

Any future cross-criterion-derived risk input must be represented as explicit derived evidence with lineage and an explicit semantic decision.

## NOT_APPLICABLE

Client / Project Risk is `NOT_APPLICABLE` only when policy/context explicitly establishes that the criterion does not apply.

Absence of risk evidence is not sufficient to establish non-applicability.

## Non-goals

V1 does not introduce:

- risk scoring;
- reputation scoring;
- probability or risk prediction;
- universal risk formulas;
- ranking;
- automatic opportunity rejection;
- portfolio decisions;
- bidding;
- payment;
- execution;
- AI-generated policy;
- automatic policy mutation.

## Design Trade-off Decision

**Approved Option C: explicit risk constraints + deterministic categorical evaluator.**

The approved boundary also preserves separate Client Risk and Project Risk evidence scopes while using one provider-independent criterion contract.

This keeps risk interpretation explainable, prevents hidden scoring, and allows future risk signals to be added through explicit policy/evidence contracts without turning V1 into a generalized risk engine.

## Exit Criteria

- semantic boundary approved;
- Client Risk and Project Risk scopes explicit;
- constraint semantics explicit;
- evidence quality and contradiction semantics explicit;
- derived evidence and lineage rules explicit;
- no scoring/ranking/prediction introduced;
- owner approval recorded;
- implementation proceeds only through a separate TDD issue.
