# TDD: Estimated Effort Criterion V1

**Status: IMPLEMENTATION IN PROGRESS — GREEN/HARDEN committed; CI verification pending.**

## Approved boundary

Estimated Effort evaluates explicit `EvidenceKind.ESTIMATE` evidence against policy-defined effort constraints. It does not generate estimates.

## RED

PR #471 started with failing tests for:

- usable estimate within explicit constraint;
- explicit constraint violation;
- missing/ambiguous/stale/low-quality evidence;
- missing scope;
- conflicting estimates without precedence;
- assumptions not treated as estimates;
- uncertainty preservation;
- explicit non-applicability;
- no inference from opportunity fields;
- unit mismatch;
- context identity;
- policy identity.

RED CI run #1409 failed as expected at test collection because `app.application.estimated_effort` did not exist:

`ModuleNotFoundError: No module named 'app.application.estimated_effort'`

## GREEN

Implemented:

- `app.domain.estimated_effort.EffortConstraint`
- `EvaluationPolicy.estimated_effort_constraints`
- `app.application.estimated_effort.EstimatedEffortEvaluator`

The evaluator is provider-independent and deterministic. It validates evidence quality/kind, explicit scope, unit compatibility, contradiction, and policy-defined maximum effort constraints.

## Hardening decisions

- Conflicting usable estimates without explicit policy precedence produce `INSUFFICIENT_DATA`.
- An explicit violation produces `FAIL` only when the relevant evidence is otherwise usable and no unresolved uncertainty remains.
- Evidence uncertainty is preserved in the criterion result and is not converted into a score/confidence value.
- `ASSUMPTION` evidence is not silently promoted to `ESTIMATE`.
- Unit conversion is not silently inferred.
- No estimate is derived from opportunity title/description/budget.
- No cross-criterion outcome is consumed as evidence.

## Verification

Latest implementation commits are on `feat/estimated-effort-criterion-v1`. CI verification must pass on the latest head before merge. GitHub requires required checks to pass against the latest commit SHA.

## Completion criteria

This slice is not complete until:

**RED → GREEN → HARDEN → DOCUMENT → CI success → MERGE → project-state reconciliation**

No production marketplace/provider integration, AI estimation, scheduling, scoring, ranking, or execution is introduced.
