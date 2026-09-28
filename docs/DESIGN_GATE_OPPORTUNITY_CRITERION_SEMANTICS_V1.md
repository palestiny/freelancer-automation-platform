# Design Gate: Opportunity Criterion Semantics & Evidence Contract V1

## Status

**APPROVED — semantic boundary accepted and evidence/context foundation implemented and merged on 2026-09-28.**

This document records the approved V1 semantic boundary for Issue #457. Concrete implementation must remain within these semantics; any semantic expansion requires a new design decision.

## 1. Design objective

The generic Opportunity Intelligence contract is already committed:

- six criteria;
- categorical criterion outcomes;
- categorical overall outcome;
- immutable policy identity/version;
- pluggable evaluator boundary;
- explicit missing-evidence handling.

The next boundary is to define what each criterion actually means without introducing hidden scoring, marketplace-specific heuristics, unsupported user assumptions, or circular reasoning.

## 2. Root architectural finding

The current evaluator signature is:

`evaluate(opportunity, policy)`

That is sufficient for the generic orchestration contract but insufficient for several real criterion semantics.

Eligibility, Requirement Fit, Economic Fit, and parts of Estimated Effort require context that does not belong to the opportunity itself. Examples include the user's declared capabilities, availability, economic policy, and approved planning assumptions.

### Proposed decision

Introduce an immutable, provider-independent `EvaluationContext` at the application/domain boundary before implementing concrete evaluators.

The context should be an explicit snapshot of inputs required by the selected policy. It must not become a mutable "user state" aggregate or a hidden dependency container.

Proposed conceptual shape:

- `subject`: opportunity under evaluation;
- `profile evidence`: declared capabilities/constraints relevant to this evaluation;
- `economic evidence`: approved economic inputs/calculations;
- `capacity evidence`: only when a criterion/policy explicitly requires it;
- `prior outcome evidence`: only where a criterion explicitly permits it;
- `evaluation time`: for provenance/freshness, not as a hidden decision rule;
- `evidence snapshot`: immutable references to the evidence consumed.

The exact code shape remains open until the owner approves the semantic boundary.

## 3. Evidence architecture

The repository already has a generic `Evidence` type and an epistemic taxonomy:

FACT → OBSERVATION → ESTIMATE → ASSUMPTION → HYPOTHESIS → FORECAST → EXPERIMENT_RESULT

The existing generic object is intentionally small. It must not be silently overloaded with criterion-specific semantics.

### Proposed V1 evidence layers

External observation
→ normalized fact
→ evidence-quality assessment
→ derived criterion evidence
→ criterion evaluation

Each derived item must preserve lineage to its source evidence.

### Required evidence metadata

For criterion evaluation, evidence should be able to identify:

- stable evidence identity;
- epistemic kind;
- statement/value;
- source/provenance reference;
- observation/collection time when applicable;
- evidence quality state;
- derivation references when derived;
- uncertainty when material;
- freshness only when a policy explicitly defines freshness.

No universal numeric confidence is required. A confidence number must not be introduced merely because the current generic `Evidence` model permits one.

## 4. Evidence quality

V1 should distinguish:

- PRESENT_AND_USABLE
- PRESENT_BUT_AMBIGUOUS
- PRESENT_BUT_STALE
- PRESENT_BUT_LOW_QUALITY
- MISSING

These are evidence states, not criterion outcomes.

A quality state does not itself mean PASS or FAIL.

A criterion defines which quality states are sufficient for its own interpretation.

## 5. Applicability

Applicability must be explicit.

A criterion may return NOT_APPLICABLE only when the selected policy and evaluation context establish that the criterion does not apply.

Missing information about applicability is not equivalent to NOT_APPLICABLE. If applicability cannot be established and the criterion is required, the evaluator must use INSUFFICIENT_DATA.

## 6. Criterion semantic proposals

### 6.1 Eligibility

**Question:** Is the opportunity eligible for this evaluation context under the selected policy?

Consumes:

- opportunity classification/status;
- explicit policy constraints;
- declared user/context constraints;
- required marketplace/context restrictions when represented as normalized evidence.

PASS requires sufficient evidence that all applicable eligibility constraints are satisfied.

FAIL requires reliable evidence that an applicable eligibility constraint is violated.

INSUFFICIENT_DATA applies when an eligibility condition is required but cannot be established.

NOT_APPLICABLE applies only to an explicitly non-applicable policy condition.

Must never infer eligibility from title, budget, client reputation, or missing fields.

### 6.2 Requirement Fit

**Question:** Do the opportunity's declared requirements have sufficient support in the evaluation context?

Consumes:

- normalized required capabilities;
- declared user capabilities/evidence;
- explicit requirement interpretation where available.

PASS requires every required capability covered by sufficient declared evidence.

FAIL requires explicit evidence of an incompatible or unavailable required capability.

INSUFFICIENT_DATA applies when a required capability or the corresponding user evidence is unknown/ambiguous.

NOT_APPLICABLE only when the policy explicitly has no applicable capability requirement.

Must never infer a user's capability from silence, generic profile claims, or AI output that has not been approved as evidence.

### 6.3 Estimated Effort

**Question:** Is there sufficient evidence to produce an effort assessment usable by the selected policy?

Consumes:

- scope/requirements evidence;
- explicit deliverables;
- known constraints;
- approved effort estimates;
- uncertainty/assumption lineage.

PASS means the policy's required effort evidence is sufficient for the permitted estimate.

FAIL should be reserved for explicit policy-defined contradictions or impossible constraints; an uncertain estimate is not a FAIL.

INSUFFICIENT_DATA is the default when material scope is unknown or uncertainty prevents the policy from establishing the required estimate.

NOT_APPLICABLE only when the policy explicitly excludes effort assessment.

Effort estimates remain ESTIMATE evidence. They must not be represented as observed fact.

### 6.4 Economic Fit

**Question:** Do the available economic calculations satisfy the selected policy's explicit economic conditions?

Consumes:

- normalized pricing/budget evidence;
- effort evidence;
- reusable Business Economics calculations;
- explicit economic policy inputs.

PASS/FAIL must be based on approved policy interpretation of the supplied economic evidence.

INSUFFICIENT_DATA applies when required economic inputs are unavailable, ambiguous, or materially uncertain.

NOT_APPLICABLE only when the policy explicitly excludes economic evaluation.

Economic Fit must not duplicate Business Economics formulas and must not introduce a universal profitability score.

### 6.5 Client / Project Risk

**Question:** Is there sufficient observable evidence to establish whether policy-defined risk conditions are satisfied?

Consumes only observable, traceable evidence such as:

- scope ambiguity;
- contradictory requirements;
- missing material information;
- explicit project constraints;
- reliable historical outcome evidence when such evidence is actually available and approved.

PASS means no policy-defined risk condition is evidenced at the required level.

FAIL requires explicit evidence of a policy-defined unacceptable condition.

INSUFFICIENT_DATA applies when a material risk condition cannot be established because evidence is incomplete or ambiguous.

NOT_APPLICABLE only when explicitly excluded.

The evaluator must never turn weak signals into a subjective client label, infer intent, or fabricate reputation/history.

### 6.6 Success Confidence

**Question:** Does the available evidence support the policy's required level of success confidence without circular reasoning?

Consumes:

- explicitly approved evidence sources;
- relevant requirement/effort/economic evidence only when the policy explicitly permits them;
- historical outcome evidence where valid and traceable.

The criterion must not silently reuse other criterion outcomes as evidence.

PASS requires the policy's approved evidence basis to be sufficient.

FAIL requires explicit policy-defined evidence of an unacceptable success condition.

INSUFFICIENT_DATA applies when the evidence base is insufficient.

NOT_APPLICABLE only when explicitly excluded.

V1 should not introduce a universal probability or percentage unless separately approved.

## 7. Cross-criterion dependency rule

Default V1 rule: criterion evaluators are independent.

A criterion may consume another criterion's derived evidence only if the policy explicitly declares that dependency and the dependency is represented as evidence with lineage.

Criterion outcomes themselves must not be silently fed into another criterion.

This prevents circular reasoning such as:

Success Confidence → Requirement Fit → Success Confidence.

## 8. Policy/context boundary

The policy defines interpretation.

The evaluation context supplies immutable evidence/input.

The evaluator applies deterministic semantics.

The result records:

- policy identity/version;
- criterion identity;
- outcome;
- evidence references;
- missing evidence;
- uncertainty;
- rationale where useful.

No evaluator may mutate policy, context, opportunity, or evidence.

## 9. Main trade-offs

### Option A — Keep `(Opportunity, Policy)`

Pros:
- smallest code change;
- simplest API.

Cons:
- forces user/context information into Opportunity;
- encourages hidden globals or evaluator-specific dependencies;
- makes Eligibility, Requirement Fit, and Economic Fit semantically weak.

**Not preferred.**

### Option B — Add a broad mutable User/Profile aggregate

Pros:
- easy access to many inputs.

Cons:
- creates a large coupling point;
- mixes durable identity/state with evaluation-time evidence;
- weakens reproducibility.

**Rejected for V1.**

### Option C — Immutable `EvaluationContext` evidence snapshot

Pros:
- explicit inputs;
- reproducible evaluation;
- preserves provenance;
- supports future users/businesses without changing Opportunity;
- keeps provider independence.

Cons:
- one additional abstraction;
- requires disciplined construction of the context.

**Proposed direction.**

## 10. V1 non-goals

- numeric master score;
- criterion weighting;
- opportunity ranking;
- automatic selection;
- automatic proposal/bidding;
- AI-generated policy;
- AI-generated facts without provenance;
- hidden user-profile inference;
- marketplace-specific production heuristics;
- automatic policy mutation;
- autonomous execution.

## 11. Implementation sequence and current boundary

1. Approve/revise this semantic gate.
2. Commit the `EvaluationContext` boundary if approved. **Completed in Issue #459 / PR #460.**
3. Define the minimal evidence types required by V1. **Completed in Issue #459 / PR #460.**
4. RED tests for context and evidence invariants. **Completed in PR #460.**
5. GREEN implementation. **Completed in PR #460.**
6. Implement one criterion at a time with criterion-specific tests. **This is the next implementation boundary.**
7. Hardening for missing, ambiguous, stale, contradictory, and provenance-breaking evidence.
8. Reconcile design/TDD/project-state documentation.
9. Run CI on the PR head and verify merge readiness.
10. Merge only after the design and implementation states agree.

## 12. Exit criteria for this design gate

The gate is ready for owner approval when:

- the context boundary is accepted or explicitly rejected;
- evidence metadata requirements are accepted;
- applicability semantics are accepted;
- all six criterion semantics are accepted/revised;
- cross-criterion dependency rules are accepted;
- trade-offs are recorded;
- implementation issues can be split without inventing new semantics during coding.

**No implementation should begin from this document until the owner approves the semantic contract.**
