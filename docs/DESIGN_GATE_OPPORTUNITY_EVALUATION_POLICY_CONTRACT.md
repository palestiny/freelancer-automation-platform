# Design Gate: Opportunity Evaluation Policy Contract V1

**Status:** PROPOSED — OWNER DECISION REQUIRED

## Purpose

Define the provider-independent policy contract that turns the six approved Opportunity Intelligence dimensions into deterministic criterion outcomes without introducing marketplace-specific heuristics, universal scoring, or hidden policy decisions.

## Current approved boundary

Opportunity Intelligence V1 has six committed dimensions:

1. Eligibility
2. Requirement Fit
3. Estimated Effort
4. Economic Fit
5. Client / Project Risk
6. Success Confidence

Criterion outcomes:
- PASS
- FAIL
- INSUFFICIENT_DATA
- NOT_APPLICABLE

Overall outcomes:
- QUALIFIED
- NOT_QUALIFIED
- REVIEW_REQUIRED

The semantic dimensions are approved, but their concrete evaluation policy semantics are not yet approved.

## Decision 1 — Policy shape

| Option | Shape | Strengths | Trade-offs |
|---|---|---|---|
| A | Fixed built-in rules | Smallest initial surface; simple deterministic implementation | Couples domain behavior to one policy; changing rules requires code changes; poor fit for different users/business contexts |
| B | Configurable threshold/rule policy | Policy can vary without changing evaluator code; explicit configuration | Risks growing into a generic rules engine; thresholds alone do not model every criterion cleanly |
| C | Pluggable criterion evaluators behind a stable policy contract | Separates stable evaluation contract from criterion-specific logic; supports deterministic domain evolution; policy can remain explicit and versioned | More abstraction up front; requires disciplined contracts to avoid over-engineering |

### Recommendation

**Option C — with a deliberately small V1 contract.**

The evaluator contract should be stable, while each criterion implementation remains explicit and deterministic. V1 should not become a general-purpose rules engine.

A criterion evaluator may consume only the evidence/input declared by the policy contract and must return a structured criterion result. Policy configuration can later select or parameterize approved evaluators without allowing arbitrary executable policy.

## Decision 2 — Criterion evaluation contract

Recommended V1 result:

- policy_id
- policy_version
- criterion_id
- outcome
- evidence_refs
- missing_evidence
- uncertainty
- optional human-readable rationale
- deterministic evaluation timestamp/context only where required for provenance

The result is an assessment of available evidence, not a business authorization and not an execution command.

### Required invariants

1. Same policy version + same normalized input/evidence produces the same criterion outcome.
2. Missing evidence is explicit.
3. Provider-specific SDK objects never cross the domain/application boundary.
4. A criterion cannot silently invent facts or defaults.
5. Evidence references remain traceable to the normalized opportunity/evidence layer.
6. A criterion result cannot mutate policy.

## Decision 3 — Missing evidence

### INSUFFICIENT_DATA

Use when the criterion is applicable, but required evidence is missing, ambiguous, stale beyond the policy's accepted freshness, or otherwise insufficient to establish PASS/FAIL.

### NOT_APPLICABLE

Use only when the policy explicitly determines that the criterion does not apply to this opportunity/context.

### Policy fallback

No implicit fallback in V1.

If a policy wants a fallback behavior, it must explicitly declare it. The evaluator must not convert missing evidence into PASS or FAIL merely to complete an evaluation.

## Decision 4 — Overall outcome composition

Recommended V1 composition:

- **NOT_QUALIFIED** if any applicable criterion has FAIL.
- **REVIEW_REQUIRED** if there is no FAIL, but at least one applicable criterion has INSUFFICIENT_DATA.
- **QUALIFIED** only when every applicable required criterion is PASS or explicitly NOT_APPLICABLE.

This is a deterministic categorical composition, not a score or ranking.

### Important boundary

QUALIFIED means qualified under the selected policy and available evidence. It does not mean:

- guaranteed project success;
- economically optimal;
- recommended for automatic application;
- authorized for proposal/bidding;
- approved for execution.

## Decision 5 — Economic boundary

Economic calculations remain reusable Business Economics capabilities.

Opportunity Intelligence may consume an economic assessment as evidence, but the marketplace evaluator must not duplicate pricing/profitability formulas.

The policy should distinguish:
- economic evidence/calculation;
- criterion interpretation;
- overall opportunity qualification.

## Decision 6 — Policy identity and versioning

Every evaluation must identify the policy version used.

Changing a policy must create a new version rather than silently changing the meaning of historical evaluations.

Historical evaluation results must remain interpretable against the policy version that produced them.

## Explicit non-goals

- universal numeric scores;
- ranking opportunities;
- weights across criteria;
- marketplace-specific rules;
- Freelancer API field mapping;
- AI-generated policy;
- AI-generated autonomous decisions;
- proposal/bidding;
- payment or financial execution;
- automatic policy mutation;
- generic arbitrary-code rules engine.

## Approval required

The owner must explicitly approve or modify:

1. Option C as the policy shape.
2. The criterion result contract.
3. The missing-evidence semantics.
4. The deterministic overall composition.
5. The economic boundary.
6. Policy identity/versioning.

Until approved, Issue #453 remains gated and no evaluator behavior should be implemented.