# Opportunity Prioritization V1 — Design Gate

**Status: ACCEPTED FOR V1 IMPLEMENTATION — owner approved Option C on 2026-10-09**  
**Scope:** Provider-independent, non-executing prioritization of already evaluated opportunities.  
**Parent capability:** Opportunity Intelligence V1  
**Out of scope:** Marketplace integration, ranking by AI, proposal generation, authorization, execution, portfolio/capital allocation, policy mutation.

## 1. Problem

Opportunity Intelligence can evaluate one opportunity across six dimensions and return `QUALIFIED`, `NOT_QUALIFIED`, or `REVIEW_REQUIRED`. It does not answer the distinct question: **which opportunity should a human inspect or work on first?**

Adding a universal score would collapse unlike evidence (eligibility, fit, effort, economics, risk, confidence) into a deceptively precise number. Prioritization therefore needs an explicit policy boundary, with reasons and evidence lineage preserved.

## 2. Decision required

Select a V1 model for comparing evaluated opportunities. This document recommends **Option C: policy-gated tiers**. The recommendation is not an assertion that the product owner has approved implementation.

### Option A — Universal master score

Produce one numeric score (for example, 0–100) across all dimensions.

- **Benefits:** easy to sort and display.
- **Costs / risks:** hides trade-offs, depends on implicit weights, creates false precision, and encourages a single score to become a de facto policy.
- **Disposition:** reject for V1.

### Option B — Weighted ranking

Let a configurable policy assign weights to dimensions and sort by a weighted result.

- **Benefits:** more configurable and explainable than a fixed score.
- **Costs / risks:** still compresses distinct criteria and uncertainty into one number; missing evidence and incomparable scales need additional policy; changes to weights can silently change ordering.
- **Disposition:** defer until a concrete validated consumer justifies it and a separate gate defines scale normalization, missing-data behavior, calibration, and versioning.

### Option C — Policy-gated tiers (recommended)

First apply explicit qualification and review gates; then place eligible opportunities into named priority tiers using explicit, versioned policy rules. A tier is a policy outcome, not a probability or a universal measure of value.

- **Benefits:** preserves qualification semantics, makes blockers visible, and allows human-readable reasons without hidden weights.
- **Costs / risks:** requires policy authors to define meaningful rules; ties within a tier need a deterministic, disclosed rule or must remain unordered.
- **Disposition:** recommended V1 boundary.

## 3. Proposed V1 semantics

The policy evaluates a canonical Opportunity Intelligence evaluation; it does not reimplement the six criteria.

1. **BLOCKED** — evaluation is `NOT_QUALIFIED`, or an explicit hard-block rule matches. A blocked item cannot receive a priority tier.
2. **REVIEW_REQUIRED** — evaluation is `REVIEW_REQUIRED`, required evidence is unavailable/invalid for the policy, or a rule explicitly requires human review. No priority tier is assigned.
3. **PRIORITIZED** — evaluation is `QUALIFIED`, all mandatory evidence and policy preconditions pass, and exactly one tier rule matches. The decision records the tier.
4. **UNPRIORITIZED** — evaluation is `QUALIFIED` but no tier rule matches, or the policy is incomplete/ambiguous. This is not a failure of the underlying Opportunity Intelligence evaluation.

These outcomes must remain distinct from authorization and execution. A priority decision never authorizes an action.

### Tier rules

- Tier names and order are policy-defined, versioned identifiers (for example, `P1`, `P2`, `P3`); names do not imply a numeric score.
- Hard blockers take precedence over tier rules.
- Review conditions take precedence over prioritization.
- Zero or multiple matching tier rules produce `UNPRIORITIZED` (or a validation error if the policy contract declares overlapping rules invalid); the policy must not choose arbitrarily.
- V1 should prefer rejecting invalid/overlapping policy definitions at construction/validation time where overlap can be detected deterministically.
- No hidden/default weights, AI inference, learned ordering, or implicit economic thresholds.
- Decisions preserve the evaluation identity, policy identity and version, outcome, tier if any, matched rule identifiers, blockers/review reasons, evidence references/quality, and decision time.
- Same evaluation snapshot + same policy version + same explicit evaluation time/context must produce the same semantic outcome and reasons. Generated decision IDs may differ only if identity is explicitly defined as generated metadata rather than decision semantics.
- A collection is not automatically globally ranked. Within-tier ordering is **not part of V1** unless a separately specified deterministic tie-break contract is approved. Consumers may display tiers and rationale without inventing an order.

## 4. Evidence and policy integrity

- Consume the canonical Opportunity Intelligence contract only; do not create a parallel evaluator.
- Preserve source evidence lineage and criterion-level uncertainty; do not upgrade estimates, assumptions, hypotheses, or missing evidence into facts.
- Distinguish evaluation outcome from prioritization outcome.
- Bind every decision to immutable policy identity/version and evaluation identity.
- A policy update creates a new policy version; it does not rewrite historical decisions.
- Policy evaluation is deterministic and non-executing.
- No automatic policy mutation, learning mutation, opportunity selection for execution, authorization, bidding, messaging, payment, or external side effect.

## 5. Candidate contracts (illustrative, not implementation approval)

- `PrioritizationPolicy`: immutable policy identity/version; required evaluation conditions; hard-block rules; review rules; ordered tier definitions and explicit matching rules.
- `OpportunityPriorityDecision`: immutable opportunity/evaluation/policy references; outcome; optional tier; matched rule IDs; reasons/blockers; evidence lineage/quality; evaluated-at timestamp.

Exact module ownership, value-object shape, rule expression language, persistence/API integration, and public naming must be confirmed against existing repository conventions before implementation. Do not introduce a generic rule engine or infrastructure merely to support this slice.

## 6. Required RED tests before implementation

1. `NOT_QUALIFIED` cannot produce a tier.
2. `REVIEW_REQUIRED` cannot silently become `PRIORITIZED`.
3. A qualified evaluation with missing mandatory evidence is not prioritized.
4. A qualified evaluation with no matching tier is `UNPRIORITIZED`.
5. Ambiguous or overlapping tier rules are rejected or explicitly return an unprioritized result according to the chosen contract; no arbitrary first-match behavior.
6. Decision preserves evaluation ID, policy ID/version, evidence lineage/quality, reasons, and tier-rule identity.
7. Same semantic inputs produce the same outcome, tier, and reasons.
8. Policy version changes do not mutate prior decisions.
9. Invalid or stale evaluation/policy references fail closed.
10. No authorization, provider execution, external side effect, policy mutation, or learning mutation occurs.

## 7. Acceptance criteria

- [x] Product owner confirmed Option C (policy-gated tiers) on 2026-10-09.
- [ ] Existing Opportunity Intelligence contracts and module conventions are inspected before choosing exact implementation shape.
- [ ] Domain/application ownership is explicit; no duplicate evaluator or hidden global ranker.
- [ ] RED tests prove the safety and determinism requirements above.
- [ ] GREEN implementation is minimal and provider-independent.
- [ ] Hardening covers malformed policy, missing evidence, ambiguity, and immutable lineage.
- [ ] Decision log and canonical project state/roadmap are reconciled.
- [ ] CI passes; changes are reviewed and merged; final repository state is verified.

## 8. Explicit non-goals

No 0–100 master score, weighted ranking, global list ordering, recommendation to bid, proposal drafting, autonomous opportunity selection, AI-based policy selection, marketplace-specific rules, production Freelancer mapping, or financial/portfolio action is introduced by this gate.

## 9. Current recommendation

**Decision:** Option C — policy-gated tiers is approved for V1. Implementation may proceed within this gate. Approval does not authorize a weighted/master score, hidden ordering, autonomous selection, authorization, or execution. Exact contracts must follow repository conventions discovered during implementation; any material semantic change requires a new gate.
