# TDD: Reconcile Legacy Opportunity Evaluation Surface

## Status

**COMPLETED — legacy semantic owner removed on 2026-09-28.**

## Problem

Eligibility V1 exposed an older parallel evaluation surface:

- `app/domain/opportunity_evaluation.py`
- `tests/domain/opportunity_intelligence/test_eligibility.py`
- `tests/domain/opportunity_intelligence/test_eligibility_budget.py`
- `tests/domain/opportunity_intelligence/test_eligibility_failures.py`
- `tests/domain/opportunity_intelligence/test_evaluation_boundaries.py`

The legacy module owned a separate `EvaluationPolicy`, criterion/overall outcome model, `OpportunityEvaluation`, and `OpportunityEvaluator`. It evaluated eligibility directly from `Opportunity` fields rather than from the approved immutable `EvaluationContext` and explicit evidence contract.

## Evidence Mapping

The current canonical surface is:

- `app/domain/opportunity_intelligence.py`
- `app/domain/evaluation_context.py`
- `app/domain/eligibility.py`
- `app/application/eligibility.py`
- `tests/application/test_eligibility_criterion_v1.py`

The canonical Eligibility V1 tests cover the approved evidence-driven semantics: explicit constraints, evidence quality, missing evidence, contradiction, applicability, subject identity, deterministic evaluation, and policy identity.

The four legacy test files were coupled to the obsolete module and its old semantics. Their behavior was not migrated because doing so would preserve the duplicate contract. Canonical V1 coverage remains authoritative.

## Cleanup Decision

The cleanup removes the duplicate semantic owner and its coupled tests. No compatibility shim was introduced.

No Eligibility V1 behavior was changed.

## Verification

Required completion sequence:

1. Legacy references removed from the branch.
2. Canonical Eligibility V1 tests remain intact.
3. Full CI passes on the final branch head.
4. Pull request merged into `main`.
5. Issue #463 closed as completed.
6. Project state reconciled so Economic Fit remains the next engineering boundary.

## Non-goals

- No changes to Eligibility V1 semantics.
- No changes to Requirement Fit or Estimated Effort.
- No Economic Fit implementation.
- No policy/ranking/scoring changes.
