# Design Gate: Requirement Fit Criterion Semantics V1

## Status

**PROPOSED — semantic boundary prepared for owner approval.**

This document defines the proposed V1 semantic boundary for the Requirement Fit criterion. It does not authorize implementation until the semantic decisions below are explicitly approved.

## Decision Target

Requirement Fit evaluates whether the immutable evaluation evidence establishes that an opportunity's **mandatory capability requirements** are satisfied by the subject's declared capability evidence.

The criterion is deterministic, provider-independent, categorical, and evidence-traceable.

It does not produce a percentage, score, ranking, recommendation, or probability.

## Core Semantic Model

V1 separates three concepts:

1. **Requirement** — a policy-defined capability demand of the opportunity.
2. **Capability Evidence** — evidence about a capability possessed or supported by the subject.
3. **Matching Relation** — the explicit relation permitted by policy between a requirement and capability evidence.

A requirement must have a stable identity and an explicit capability identity.

Proposed V1 requirement fields:

- `requirement_id`
- `capability_id`
- `evidence_refs`
- `required: true`
- optional applicability controlled explicitly by policy/context

V1 intentionally treats requirements as atomic capability requirements. Compound natural-language interpretation is outside this evaluator.

## Capability Identity

V1 uses **exact normalized capability identity** as the only matching relation.

Example:

- requirement: `react`
- capability evidence: `react`
- result: satisfied when the evidence is usable.

The following are **not** inferred in V1:

- aliases;
- synonyms;
- semantic similarity;
- version compatibility;
- substitute technologies;
- compatible variants;
- implied capabilities from related technologies.

Those relations require an explicit future capability ontology/compatibility contract and evidence-backed semantics.

This prevents a hidden ontology from silently changing qualification results.

## Requirement Interpretation

For each applicable mandatory requirement:

### SATISFIED

A usable capability evidence item establishes the exact required capability identity.

### VIOLATED

V1 permits FAIL only when explicit usable evidence establishes an incompatibility or an explicit policy-defined negative capability condition.

Absence of evidence is **not** a violation.

### UNDETERMINED

The required capability cannot be established because evidence is:

- missing;
- ambiguous;
- stale;
- low quality;
- contradictory without an approved precedence rule;
- non-usable under the selected policy.

Criterion composition:

- any explicit violation → **FAIL**;
- otherwise any undetermined mandatory requirement → **INSUFFICIENT_DATA**;
- all applicable mandatory requirements satisfied → **PASS**;
- no applicable requirements → **NOT_APPLICABLE**.

## Evidence Rules

Requirement Fit reuses the approved `EvaluationContext` evidence semantics.

Evidence quality is not itself an outcome:

- `PRESENT_AND_USABLE` may establish a match;
- `PRESENT_BUT_AMBIGUOUS` → insufficient;
- `PRESENT_BUT_STALE` → insufficient unless the policy explicitly defines the evidence as temporally valid;
- `PRESENT_BUT_LOW_QUALITY` → insufficient unless explicitly permitted;
- `MISSING` → insufficient.

Contradictory usable evidence without explicit policy precedence produces `INSUFFICIENT_DATA` and preserves all relevant evidence references.

## Partial Matching

Partial matching is not converted into a score or percentage.

For mandatory requirements:

- all satisfied → PASS;
- one or more unresolved → INSUFFICIENT_DATA;
- one or more explicit violations → FAIL.

Optional requirements are **not part of the V1 criterion result**. Introducing optional-requirement contribution without a score/ranking semantic would create an unresolved policy surface, so optional requirements should be deferred until explicitly designed.

## Applicability

`NOT_APPLICABLE` is returned only when policy/context explicitly establishes that Requirement Fit does not apply.

Unknown applicability is not equivalent to NOT_APPLICABLE.

If applicability is required but unresolved, the result is `INSUFFICIENT_DATA`.

## AI-Derived Evidence

AI may assist upstream extraction or normalization, but generation alone does not make an assertion usable evidence.

An AI-derived capability assertion may be considered by the evaluator only when it is represented in the approved evidence model with:

- stable evidence identity;
- provenance;
- epistemic kind;
- quality;
- derivation lineage where applicable;
- explicit policy permission for that evidence kind.

V1 should not silently upgrade `ASSUMPTION`, `HYPOTHESIS`, or unsupported generated claims into usable capability facts.

## Cross-Criterion Isolation

Requirement Fit does not consume outcomes from:

- Eligibility;
- Estimated Effort;
- Economic Fit;
- Client / Project Risk;
- Success Confidence.

A future dependency must be represented as explicit derived evidence with lineage and receive separate semantic approval.

## Determinism and Boundary

The evaluator is deterministic for the same:

- policy identity/version;
- opportunity;
- immutable EvaluationContext;
- evaluation time.

It performs no live provider calls, mutable profile reads, hidden state access, ranking, or randomization.

Provider SDKs and marketplace-specific semantics remain outside the domain/application criterion evaluator.

## Trade-off Decision

### A — String/set matching

Rejected as the complete semantic contract because raw strings cannot safely represent requirement identity, evidence quality, provenance, contradictions, or future explicit compatibility rules.

### B — Generic capability/rules engine

Rejected for V1 because it introduces a generalized ontology/rules subsystem before the concrete semantic surface is proven.

### C — Explicit capability requirements + small deterministic evaluator

**Proposed.**

This preserves the approved architecture: policy defines meaning, immutable context supplies evidence, evaluator deterministically interprets evidence, and results retain traceability.

## Non-goals

- capability scoring or percentage matching;
- ranking opportunities;
- semantic similarity;
- automatic alias/synonym inference;
- version compatibility inference;
- AI-owned qualification;
- provider-specific capability heuristics;
- proposal/bidding;
- execution;
- policy mutation;
- autonomous selection.

## Open Owner Decisions

1. Approve **exact normalized capability identity only** for V1.
2. Approve **mandatory requirements only** for V1; defer optional requirements.
3. Approve explicit incompatibility as the only V1 path to `FAIL`; missing capability evidence remains `INSUFFICIENT_DATA`.
4. Approve contradictory usable evidence without explicit precedence as `INSUFFICIENT_DATA`.
5. Approve AI-derived evidence as non-authoritative unless represented with provenance/quality/lineage and explicitly permitted by policy.

## Exit Criteria

The design gate can move to implementation only after:

- owner approval of the semantic boundary;
- design document reconciled to APPROVED;
- implementation issue/branch created;
- RED tests written before implementation;
- GREEN implementation;
- hardening/refactoring;
- documentation reconciliation;
- passing CI;
- merge and verified project state.
