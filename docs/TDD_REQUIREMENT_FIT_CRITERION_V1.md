# TDD: Requirement Fit Criterion V1

**Status:** COMPLETED — merged into main on 2026-09-28.

## Scope
Implements the approved Requirement Fit V1 semantic boundary:
- exact normalized capability identity only;
- mandatory requirements only;
- explicit incompatibility is the only FAIL path;
- missing, ambiguous, stale, low-quality, contradictory, or unsupported evidence remains INSUFFICIENT_DATA;
- explicit NOT_APPLICABLE only when policy/context establishes it;
- deterministic provider-independent evaluation;
- evidence references, uncertainty, and policy identity/version are preserved.

## TDD Evidence
- RED: CI run #1400 failed as expected because app.application.requirement_fit did not yet exist.
- GREEN: implementation added domain CapabilityRequirement, policy support, and RequirementFitEvaluator.
- Initial GREEN CI: #1402 succeeded on commit 5a8ead370e817cff9b33ad483d36274beffafec0.
- HARDENING: added coverage for unsupported capability assertions, duplicate requirement IDs, capability identity mismatch, and conflicting supported/incompatible evidence.
- Final CI: #1403 succeeded on commit 77c271e2c609e116ecd3f84aba1ef73a4eda78af.

## Implementation Boundary
No semantic similarity, aliases, version compatibility, generic ontology/rules engine, scoring/ranking, selection, bidding, execution, provider SDK dependency, or policy mutation was introduced.

## Merge
PR #467 was merged into main after the latest head commit passed CI.
