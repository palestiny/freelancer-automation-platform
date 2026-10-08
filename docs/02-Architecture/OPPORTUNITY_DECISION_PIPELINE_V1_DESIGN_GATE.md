# Opportunity Decision Pipeline V1 — Design Gate

**Status: PROPOSED — owner decision required**  
**Scope:** Compose existing Opportunity Intelligence evaluation and Opportunity Prioritization into one explicit application-level use case.  
**Prerequisites:** Opportunity Intelligence V1 and Opportunity Prioritization V1.  
**Out of scope:** Persistence, APIs, background jobs, marketplace polling, production Freelancer mapping, automatic selection, bidding, messaging, execution, policy mutation, portfolio/capital allocation.

## 1. Problem

The repository now has separate application services for canonical opportunity evaluation and policy-gated prioritization. They are tested independently, but there is no single application use case that runs them in order and returns one coherent result for a caller.

A consuming workflow should not need to reimplement qualification gates, evidence handling, or evaluation-to-prioritization sequencing. At the same time, the composition must not become a hidden global ranker, provider adapter, persistence layer, or execution trigger.

## 2. Options

### Option A — Keep orchestration entirely with each caller
Callers directly invoke `OpportunityIntelligenceEvaluator`, inspect its result, then invoke `OpportunityPrioritizer`.

- **Benefits:** no additional abstraction; maximum caller flexibility.
- **Costs / risks:** callers may duplicate sequencing and accidentally diverge on evidence gates, timestamps, or lineage handling.
- **Disposition:** acceptable for one-off internal tests, not preferred as the reusable application boundary.

### Option B — Add a small application-level composition service (recommended)
Introduce an `OpportunityDecisionPipeline` that accepts an already normalized domain `Opportunity`, explicit evaluation and prioritization policies, the existing evaluator/prioritizer services, caller-supplied opportunity/evaluation references, and a timezone-aware decision timestamp. It runs evaluation first, passes the canonical result to prioritization, and returns an immutable combined result containing both outputs.

- **Benefits:** one canonical sequence; reuses existing services; easy to test; no provider dependency or duplicate evaluation logic.
- **Costs / risks:** adds a thin orchestration contract and requires callers to supply identity references until an authoritative identity/persistence contract exists.
- **Constraints:** no implicit default policies, no generated or guessed references, no hidden global service locator, no persistence, and no external side effects.

### Option C — Build a persisted workflow/API endpoint now
Add storage, an endpoint, identity registry, and a broader opportunity workflow around the services.

- **Benefits:** closer to a user-facing feature.
- **Costs / risks:** introduces persistence/API/identity decisions not yet designed and could imply provider readiness that has not been proven.
- **Disposition:** defer; separate design gates are required.

## 3. Recommended decision

**Recommend Option B.** This is the smallest reusable application boundary that makes the existing capabilities consumable without broadening the system's authority.

The pipeline should:
1. Validate required input types and explicit non-empty references.
2. Run the existing `OpportunityIntelligenceEvaluator` exactly once.
3. Pass that exact `OpportunityEvaluation` to `OpportunityPrioritizer`.
4. Return an immutable result containing the canonical evaluation and the resulting priority decision.
5. Preserve the caller's evaluation and prioritization policy identities/versions and the criterion evidence context already captured by those contracts.
6. Remain deterministic for equivalent semantic inputs, excluding any caller-supplied time value.
7. Perform no persistence, provider I/O, ranking across multiple opportunities, authorization, or execution.

## 4. Important semantic boundaries

- `NOT_QUALIFIED` must remain `BLOCKED`; `REVIEW_REQUIRED` must remain review-only.
- The pipeline processes one opportunity at a time. It does not produce a global list or within-tier ordering.
- Identity references are caller-supplied and carried through; this service does not claim that they are registered, current, unique, or persisted.
- Reference freshness validation remains deferred until an authoritative registry/contract exists.
- Provider normalization remains a separate preceding step. The pipeline consumes the canonical domain `Opportunity`; it does not depend on a real Freelancer payload.
- Policy versions are explicit inputs. The pipeline must not select or mutate policies.

## 5. Required tests before implementation

1. Qualified evaluation is passed to prioritization exactly once and the same evaluation is returned.
2. `NOT_QUALIFIED` yields `BLOCKED`; `REVIEW_REQUIRED` remains `REVIEW_REQUIRED`.
3. Missing mandatory evidence and ambiguous/no-match tier rules retain existing prioritizer semantics.
4. Evaluation and prioritization policy IDs/versions remain visible in the combined result.
5. Criterion evidence snapshots survive through the combined result without reconstruction or loss.
6. Invalid input references and naive timestamps fail closed.
7. Equivalent inputs yield equivalent results; no policy mutation or external side effects occur.
8. The pipeline does not normalize provider payloads, persist records, sort multiple opportunities, or invoke execution ports.

## 6. Acceptance criteria

- [ ] Product owner approved the recommended composition boundary.
- [ ] Existing service contracts and constructors are rechecked before implementation.
- [ ] RED tests cover sequencing, identity lineage, outcome pass-through, and no side effects.
- [ ] Implementation reuses existing services and does not duplicate evaluation or prioritization logic.
- [ ] Canonical project state and roadmap are updated after implementation.
- [ ] CI passes and the change is reviewed and merged.

## 7. Owner decision

**Recommended: Option B — small application-level composition service.**  
Approval of this gate authorizes only the non-persisted, single-opportunity composition described above. API, persistence, provider integration, batch ranking, and execution require separate decisions.
