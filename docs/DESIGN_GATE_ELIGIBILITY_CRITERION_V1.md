# Design Gate: Eligibility Criterion Semantics V1

## Status

**APPROVED — semantic boundary accepted on 2026-09-28.**

Owner approval is recorded on Issue #461. This document is the durable design record for the first concrete Opportunity Intelligence criterion.

## Decision

Eligibility uses **explicit policy-defined constraints evaluated against an immutable EvaluationContext evidence snapshot**.

The evaluator is deterministic, provider-independent, and categorical.

### Constraint model

Each eligibility constraint declares:

- a stable constraint identity;
- one or more evidence references;
- the allowed values that satisfy the constraint.

The evaluator interprets each applicable constraint as:

- **SATISFIED** — usable evidence establishes an allowed value;
- **VIOLATED** — usable evidence establishes a value outside the allowed set;
- **UNDETERMINED** — required evidence is missing, ambiguous, stale, low-quality, non-string, or contradictory.

Criterion composition:

- any violation → **FAIL**;
- otherwise any undetermined constraint → **INSUFFICIENT_DATA**;
- all constraints satisfied → **PASS**;
- no applicable eligibility constraints → **NOT_APPLICABLE**.

## Evidence rules

Evidence quality is not itself a criterion outcome.

- PRESENT_AND_USABLE may establish a constraint result.
- PRESENT_BUT_AMBIGUOUS is insufficient unless an explicit policy later defines an unambiguous interpretation.
- PRESENT_BUT_STALE is insufficient for a current eligibility condition.
- PRESENT_BUT_LOW_QUALITY is insufficient unless explicitly permitted.
- MISSING is insufficient.

Contradictory usable evidence without an explicit precedence rule produces INSUFFICIENT_DATA. The evaluator preserves the involved evidence references.

## Explicit non-inference boundary

Eligibility must not be inferred from:

- title wording;
- budget/pricing;
- client reputation;
- missing fields;
- unstated user preferences;
- unproven AI assertions.

A country, status, type, or other constraint only applies when the selected policy explicitly defines it and the required evidence is available.

## Determinism

The result is deterministic for the same:

- policy identity/version;
- opportunity;
- evaluation-context evidence snapshot;
- evaluation time.

The evaluator performs no live provider calls, mutable profile reads, hidden state access, or randomization.

## Cross-criterion isolation

Eligibility does not consume outcomes from Requirement Fit, Economic Fit, Client/Project Risk, or Success Confidence.

Any future cross-criterion dependency must be represented as explicit derived evidence with lineage and separately approved semantics.

## Trade-off decision

### A — Hard-coded eligibility rules

Rejected for V1 because product policy would become embedded in evaluator code.

### B — Generic rules engine

Rejected for V1 because it introduces unnecessary abstraction before the concrete semantic surface is proven.

### C — Explicit policy-defined constraints + small deterministic evaluator

**Approved.**

This preserves policy/evaluator separation, provider independence, auditability, deterministic testing, and future extensibility without creating a premature rules-engine subsystem.

## Non-goals

- numeric scores;
- weighting;
- ranking;
- automatic opportunity selection;
- bidding/proposals;
- execution;
- policy mutation;
- marketplace-specific provider heuristics.

## Implementation boundary

Implemented in Issue #461 / PR #462:

- EligibilityConstraint domain contract;
- EvaluationPolicy.eligibility_constraints;
- EligibilityEvaluator;
- RED/GREEN/hardening tests;
- evidence lineage in criterion results.

The generic Opportunity Intelligence orchestration contract remains unchanged in this slice. Integration of context-aware concrete evaluators into broader orchestration is a separate boundary and must not be introduced implicitly.
