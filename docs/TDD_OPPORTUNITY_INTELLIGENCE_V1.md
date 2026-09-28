# TDD: Opportunity Intelligence V1 Evaluation Contract

**Status:** IN PROGRESS — RED/GREEN implementation on branch `feat/opportunity-intelligence-v1`

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

Tests define:

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

Remaining before merge:

- repository-wide compatibility review;
- validation of immutable/typed contract invariants;
- CI success on the final PR head;
- documentation and roadmap reconciliation.

## Explicit non-goals

No scoring/ranking, AI policy generation, marketplace-specific heuristics, proposal/bidding, payment, execution, or automatic policy mutation.
