# TDD: Eligibility Criterion V1

## Status

**IN PROGRESS — implementation and hardening complete on branch; merge reconciliation pending.**

## Design reference

Issue #461: Design Gate: Eligibility Criterion Semantics V1.

## RED

PR #462 first added criterion-specific tests covering:

- satisfied constraint → PASS;
- violated constraint → FAIL;
- missing evidence → INSUFFICIENT_DATA;
- ambiguous evidence → INSUFFICIENT_DATA;
- stale evidence → INSUFFICIENT_DATA;
- low-quality evidence → INSUFFICIENT_DATA;
- explicit non-applicability → NOT_APPLICABLE;
- no inference from title/budget/reputation;
- contradictory evidence without precedence → INSUFFICIENT_DATA;
- policy identity/version;
- deterministic evaluation.

CI run #1386 failed as expected because app.application.eligibility did not exist.

## GREEN

Implemented:

- provider-independent EligibilityConstraint;
- policy-owned eligibility constraints;
- deterministic EligibilityEvaluator;
- explicit evidence-quality handling;
- contradiction handling;
- context/opportunity identity validation.

## HARDEN

Added tests for:

- mismatched context subject rejection;
- duplicate evidence-reference rejection;
- empty allowed-values rejection.

A repository-level test-module basename collision was also discovered by CI because an existing legacy test and the new V1 test shared the same Python module name. The V1 test was renamed to a unique module name; the existing legacy test was not silently removed.

## Verification

Latest verified CI before documentation reconciliation:

- workflow: CI
- run: #1391
- head commit: 12cc81a6313dbfe2eeb9681f6b6b1fb217635f18
- result: **SUCCESS**
- test result: **880 passed**

## Merge

Pending PR #462 merge and post-merge project-state reconciliation.

## Boundary

No score, ranking, selection, bidding, execution, or automatic policy mutation was added.
