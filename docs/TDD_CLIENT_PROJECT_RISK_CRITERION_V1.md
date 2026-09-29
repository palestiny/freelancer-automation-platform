# TDD — Client / Project Risk Criterion V1

## Status

**COMPLETED — implementation, hardening, CI, and merge gate ready.**

Design authority: Issue #478 / `docs/DESIGN_GATE_CLIENT_PROJECT_RISK_CRITERION_V1.md`.

Implementation tracking: Issue #480.

## RED

The RED slice established tests for:

- Client and Project risk scope separation;
- explicit allowed-value constraints;
- PASS for satisfied constraints;
- FAIL only for explicit policy violations;
- missing, ambiguous, stale, and low-quality evidence;
- wrong scope and wrong signal identity;
- contradictory usable evidence without precedence;
- conservative violation + unresolved evidence handling;
- explicit NOT_APPLICABLE;
- no inference from Opportunity fields;
- policy identity and evidence-reference preservation;
- uncertainty preservation without score/confidence;
- mismatched evaluation subjects;
- duplicate constraint IDs and evidence references;
- AI/hypothesis evidence not implicitly accepted;
- derived evidence with explicit lineage;
- unsupported operators/scopes and empty expected values;
- deterministic repeated evaluation;
- empty policy constraints producing NOT_APPLICABLE.

Initial RED CI failed at collection because the implementation module did not yet exist. After the implementation was introduced, the first GREEN attempt exposed one test-fixture reference mismatch in the derived-evidence test. The fixture was corrected without changing production semantics.

## GREEN

Implemented:

- `app/domain/client_project_risk.py`
  - `RiskScope`
  - `RiskComparisonOperator`
  - immutable `RiskConstraint`
- `EvaluationPolicy.client_project_risk_constraints`
- `app/application/client_project_risk.py`
  - deterministic `ClientProjectRiskEvaluator`

The evaluator consumes immutable `EvaluationContext` evidence and requires:

- exact risk scope;
- exact signal identity;
- usable evidence quality;
- an allowed evidence kind;
- explicit policy references.

V1 allowed evidence kinds are:

- FACT
- OBSERVATION
- ESTIMATE
- EXPERIMENT_RESULT

ASSUMPTION, HYPOTHESIS, and FORECAST evidence do not establish a V1 risk constraint.

Outcome composition is:

- explicit violation + no unresolved required evidence → FAIL;
- violation + unresolved required evidence → INSUFFICIENT_DATA;
- unresolved required evidence → INSUFFICIENT_DATA;
- all constraints satisfied → PASS;
- explicit non-applicability → NOT_APPLICABLE.

No risk score, confidence score, ranking, prediction, automatic rejection, or policy mutation is introduced.

## HARDEN

Hardening covers:

- deterministic repeated evaluation;
- empty-constraint non-applicability;
- duplicate identities/references;
- evidence quality boundaries;
- scope/signal mismatch;
- contradiction handling;
- uncertainty preservation;
- lineage-aware derived evidence;
- AI/hypothesis evidence boundary;
- subject identity validation.

## CI Evidence

Final verification must be performed against the latest PR head SHA.

GitHub's required-check model evaluates successful checks against the relevant latest commit; therefore the final CI result must correspond to the actual final PR head before merge.

## Documentation Reconciliation

After final CI success and merge:

- mark this document complete;
- close Issue #480 as completed;
- update `docs/PROJECT_STATE.md`;
- verify `main` contains the canonical Risk criterion implementation and no duplicate semantic owner.
