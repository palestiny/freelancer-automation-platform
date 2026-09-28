# TDD: Opportunity Intelligence V1 Evaluation Contract

**Status:** COMPLETED — RED/GREEN/HARDEN verified and merged to `main` on 2026-09-28.

## Approved contract

Design Gate #454 is approved.

- Policy shape: small stable policy contract with pluggable criterion evaluators.
- Six V1 criteria:
  - Eligibility
  - Requirement Fit
  - Estimated Effort
  - Economic Fit
  - Client / Project Risk
  - Success Confidence
- Criterion outcomes:
  - PASS
  - FAIL
  - INSUFFICIENT_DATA
  - NOT_APPLICABLE
- Overall outcomes:
  - QUALIFIED
  - NOT_QUALIFIED
  - REVIEW_REQUIRED
- Missing evidence remains explicit.
- No implicit PASS/FAIL fallback.
- Overall composition is deterministic and categorical.
- No universal score, ranking, or weights.
- Economic calculations remain reusable Business Economics concerns.
- Policy identity/version is part of evaluation identity.

## RED

Tests were added first for:

- explicit policy input;
- pluggable criterion evaluator boundary;
- criterion result evidence/missing-evidence/uncertainty preservation;
- FAIL precedence over INSUFFICIENT_DATA;
- REVIEW_REQUIRED when no criterion fails but applicable evidence is insufficient;
- NOT_APPLICABLE does not force review;
- policy identity/version preservation;
- rejection of evaluator results with mismatched policy identity.

## GREEN

Implemented:

- immutable domain enums and contracts;
- deterministic overall outcome composition;
- application evaluator dispatch through criterion evaluator ports;
- policy/result identity validation;
- no marketplace SDK or provider-specific dependency.

## HARDEN

Verified before merge:

- repository implementation reviewed for domain/application boundary consistency;
- immutable/typed contract invariants reviewed;
- final PR head CI passed: GitHub Actions run `36427376196`, pytest job successful;
- PR #456 merged squash to `main`;
- merge commit: `40ce2473b09e15aa89e6ed5d7e9ada501c871249`.

GitHub's status-check model requires required checks to pass on the latest PR commit; a separate workflow run on the merge commit itself is not required for an already validated, up-to-date PR. citeturn0search1

## Boundary after completion

This slice establishes the generic Opportunity Intelligence evaluation contract only.

Concrete business semantics for the six criteria are intentionally **not invented here**. Implementing criterion-specific rules, evidence requirements, thresholds, or heuristics requires an explicit semantic design decision before TDD implementation.

## Explicit non-goals

No scoring/ranking, AI policy generation, marketplace-specific heuristics, proposal/bidding, payment, execution, or automatic policy mutation.
