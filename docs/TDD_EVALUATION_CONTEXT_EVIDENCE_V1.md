# TDD: EvaluationContext and Evidence Contract V1

## Status

**COMPLETED — implementation merged on 2026-09-28.**

## Scope

Issue #459 implemented the approved semantic foundation for Opportunity Intelligence evaluation context and evidence.

Implemented:

- immutable provider-independent `EvaluationContext`;
- explicit `Evidence` identity, epistemic kind, value, provenance, observation time, and uncertainty;
- explicit evidence quality states;
- explicit criterion applicability representation;
- immutable applicability mapping;
- evidence identity uniqueness;
- evidence derivation lineage;
- provenance protection against self-reference and references outside the evaluation snapshot;
- timezone-aware evaluation/observation timestamps.

## TDD verification

### RED

PR #460 initially introduced tests before the production module existed.

CI run #1376 failed during test collection with:

`ModuleNotFoundError: No module named 'app.domain.evaluation_context'`

This verified that the new tests exercised a genuinely missing implementation boundary.

### GREEN

The minimal implementation was added.

CI run #1378 initially exposed one construction defect: the empty applicability default was a tuple rather than a mapping. The root cause was corrected with a mapping default factory.

CI run #1378 then passed with **866 tests passed**.

### HARDEN

Additional tests and implementation were added for:

- immutable applicability mapping;
- unknown derivation-reference rejection;
- self-referential lineage rejection.

CI run #1380 passed.

## Architectural boundary

The context is an immutable evaluation-time evidence snapshot.

It is not:

- a mutable user/profile aggregate;
- a hidden dependency container;
- a policy;
- a criterion result;
- a provider-specific object.

The generic Opportunity Intelligence evaluator remains unchanged in this slice. Concrete criterion evaluators will consume `EvaluationContext` only in their dedicated implementation slices.

## Explicit non-goals

This slice does not implement:

- concrete semantics for the six criteria;
- numeric scoring or weighting;
- ranking or automatic selection;
- AI-generated evidence without provenance;
- policy mutation;
- proposal/bidding/execution behavior;
- marketplace-specific production heuristics.

## Merge verification

PR #460 was squash-merged into `main`.

Merge commit: `ee66af7a6a1997dc32256635d940c1a64de18007`

The latest verified CI run before merge was #1380 on the PR head and passed.
