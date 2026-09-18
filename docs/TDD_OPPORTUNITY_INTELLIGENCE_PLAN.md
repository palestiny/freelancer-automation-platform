# Opportunity Intelligence TDD Plan

## Status

**PREPARATION ONLY — implementation must wait for Design Gate approval.**

This plan defines how the first domain behavior will be tested after the Opportunity Intelligence Design Gate is closed.

## Testing Boundary

The first tests should exercise domain behavior only.

They should not require:
- HTTP
- database
- marketplace SDK
- real marketplace credentials
- AI provider
- UI

## RED Sequence

### RED-01 — Eligibility passes

Given an opportunity satisfying a hard policy constraint, evaluation records the criterion as PASS.

### RED-02 — Eligibility fails

Given an opportunity violating a hard policy constraint, evaluation records FAIL and the overall result can become NOT_QUALIFIED.

### RED-03 — Missing evidence is explicit

Given a required value that is unavailable, evaluation records INSUFFICIENT_DATA rather than inventing a value.

### RED-04 — Criterion evidence is preserved

Given an evaluated criterion, the result contains the evidence used to reach that criterion outcome.

### RED-05 — Opportunity identity is unchanged

Evaluating an opportunity does not mutate its business identity or normalized source identity.

### RED-06 — Policy independence

The same opportunity can be evaluated against two different policies and produce different derived results without changing the opportunity itself.

### RED-07 — Review state represents uncertainty

Given unresolved information that prevents a confident qualification decision, the overall result can be REVIEW_REQUIRED.

### RED-08 — No numeric score required

The first evaluation behavior is complete without requiring a numeric opportunity score.

## TDD Order

For each behavior:

1. Write the smallest failing test.
2. Implement the minimum behavior needed to pass.
3. Refactor without changing behavior.
4. Review the boundary against the Design Gate.
5. Commit a coherent increment.
6. Update project state when the gate or milestone changes.

## Expected Domain Separation

The tests should keep these concepts distinguishable:

**External Observation → Normalized Opportunity → Evaluation Policy → Evaluation Result**

The evaluator must consume domain representations, not marketplace transport objects.

## Explicit Non-Goals

The first TDD slice will not test:
- marketplace scraping or API behavior
- persistence mechanics
- REST contracts
- authentication
- proposal generation
- AI model selection
- client communication
- project execution

Those belong to later design/implementation gates.

## Gate Dependency

This plan is ready for implementation once the product-owner decisions listed in `docs/PROPOSED_OPPORTUNITY_INTELLIGENCE_GATE_RESOLUTION.md` are approved and recorded as committed decisions.
