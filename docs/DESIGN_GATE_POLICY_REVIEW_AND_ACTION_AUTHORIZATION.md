# Design Gate — Policy Review & Action Authorization

**Status:** REFERENCE / PARTIALLY RESOLVED. Policy review and the V1 authorization artifact are now implemented through dedicated narrower gates. Execution remains a separate future boundary.

## Why This Boundary Exists

The current system can produce evidence and hand that evidence to policy review. The next boundary must decide how human/system policy reviews evidence without accidentally turning evidence into automatic action.

This gate intentionally stops before execution.

## Candidate V1 Contract

Input:
- EvidenceDecisionHandoff
- explicit policy context
- requested decision scope

Potential output:
- policy review result
- explicit decision status
- rationale/evidence references
- authorization state

## Required Separation

The design must keep these concepts distinct:

1. **Evidence** — what was observed or statistically inferred.
2. **Policy** — what conditions permit an action.
3. **Decision** — whether the policy conditions are satisfied for the requested scope.
4. **Authorization** — whether the decision is authorized for execution.
5. **Execution** — an external side effect.

Evidence must never imply authorization.

## Open Design Questions

### 1. Decision states

Candidates:
- APPROVE
- REJECT
- REQUEST_MORE_EVIDENCE
- ESCALATE

Trade-off:
- fewer states simplify consumers;
- richer states preserve uncertainty and review workflow.

### 2. Authorization model

Candidates:
- always human approval
- policy-only authorization for explicitly safe actions
- hybrid: policy may authorize only actions inside a separately approved autonomy level

Trade-off:
- human-only maximizes control but limits automation;
- policy-only increases autonomy and requires stronger safety boundaries;
- hybrid matches the project's progressive-autonomy direction but requires explicit action classes.

### 3. Policy identity and versioning

The decision must preserve the exact policy identifier/version used for evaluation. Policy mutation must remain outside the review result.

### 4. Evidence sufficiency

The review boundary must be able to distinguish:
- evidence sufficient for review
- evidence incomplete
- context invalid

It must not manufacture missing evidence.

### 5. Irreversible actions

Any action with material or irreversible external impact must remain outside automatic authorization until a dedicated action-safety design gate exists.

## Explicit Non-Goals

This proposal does not implement:
- automatic business decisions
- portfolio allocation
- capital movement
- financial execution
- marketplace submission
- campaign spend changes
- client communication
- external API execution
- generic policy-engine infrastructure
- AI-based policy decisions

## Current Narrow V1 Boundary

The first implementation intentionally resolves only policy evaluation: explicit allowed directions, optional statistical-detection requirement, and optional evidence-completeness requirement. It does not implement authorization or execution. The broader questions below remain for the dedicated action-authorization design gate.

## Design Exit Criteria

Implementation may begin only after the above open questions are explicitly resolved and a concrete V1 action class is selected. A dedicated RED test suite must define invalid context, insufficient evidence, policy rejection, authorization boundaries, and irreversible-action blocking.
