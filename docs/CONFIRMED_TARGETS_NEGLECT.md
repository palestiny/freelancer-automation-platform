# Confirmed Targets — Neglect / Do Not Rebuild

**Purpose:** This document is a practical checklist of project targets that are already committed, implemented, or sufficiently settled that future autonomous work should treat them as **closed unless a new requirement explicitly reopens them**.

**Review rule:** Khaled reviews this file and may manually delete/modify entries. Until then, autonomous work should avoid recreating these capabilities merely because they appear again in older roadmap/decision-log wording.

## A. Strategic Direction — Treat as Committed

- [x] Economic Opportunity OS / Business Automation OS is the product direction.
- [x] Freelancing is the first proving ground, not the permanent architectural boundary.
- [x] Modular monolith is the current architecture.
- [x] Provider independence is a core boundary.
- [x] AI is a replaceable capability, not the domain owner.
- [x] External observations, normalized evidence, derived analysis, hypotheses, decisions, authorization, and execution outcomes remain separate semantic layers.
- [x] Learning does not silently mutate policy.
- [x] Authorization is separate from execution.
- [x] Financial execution and automatic capital movement are outside the current boundary.
- [x] Progressive autonomy remains explicit: Observe → Recommend → Prepare → Execute with Approval → Execute within Policy → Optimize within Policy.

## B. Opportunity / Economics — Closed Foundation

- [x] Opportunity Evaluation has six dimensions: Eligibility, Requirement Fit, Estimated Effort, Economic Fit, Client/Project Risk, Success Confidence.
- [x] Criterion-level evidence and uncertainty are preserved.
- [x] Economic quality is multidimensional; no universal master score.
- [x] Profitability, profit potential, profit stability, demand stability, safety, recurring revenue, automation, capital efficiency, scalability, and evidence quality are first-class economic dimensions.
- [x] Expected economics and realized outcomes remain separate.
- [x] Resource economics and capacity are provider-independent.
- [x] Opportunity-cost evidence does not silently allocate resources.

## C. Market / Venture / Revenue — Closed V1 Foundations

- [x] Market observations and demand signals preserve provenance/evidence quality.
- [x] Business-model hypotheses are separate from demand observations.
- [x] Venture evaluation/lifecycle exists.
- [x] Validation experiments produce explicit measurable results and explicit decisions.
- [x] Revenue contracts explicitly distinguish one-time vs recurring revenue.
- [x] Payment execution remains outside the revenue domain.

## D. Communication / Marketing / Operations — Closed V1 Foundations

- [x] Customer communication is provider-independent.
- [x] Drafts are separate from sent messages.
- [x] Escalation overrides automated approval.
- [x] Campaigns are measurable experiments.
- [x] Marketing providers are replaceable.
- [x] Marketing optimization produces recommendations, not silent spend changes.
- [x] Budget limits are hard safety constraints.
- [x] Business is a first-class entity.
- [x] Operations are separate from business identity.
- [x] Work is provider-independent.
- [x] Multi-business isolation is explicit.
- [x] Operational outcomes produce evidence.

## E. Measurement / Learning — Do Not Rebuild

- [x] Performance history is a normalized evidence view.
- [x] Raw observations remain authoritative.
- [x] Explicit time windows are required.
- [x] Generic V1 aggregation is count/range/average-style; no universal sum semantics.
- [x] Trend analysis is descriptive and uses explicit current/baseline windows.
- [x] Baseline eligibility is policy-derived and explainable.
- [x] Source provenance is preserved through aggregation.
- [x] Source reliability is policy-derived and separate from observation evidence quality.
- [x] Operational learning requires evidence sufficiency and remains non-executing.

## F. Phase 17 Statistical Surface — Closed

- [x] Student's t mean uncertainty is implemented and hardened.
- [x] Welch two-sample historical mean comparison is implemented and hardened.
- [x] Statistical applicability is explicit/consumer-declared.
- [x] Statistical assumptions are not silently proven.
- [x] Statistical results are evidence artifacts, not policy.
- [x] Statistical methods use explicit numerical contracts.
- [x] No generic statistics framework is authorized.
- [x] New statistical methods require a concrete downstream consumer/use case and a dedicated design gate.
- [x] Statistical evidence composition exists.
- [x] Performance evidence decision support composes descriptive and inferential evidence without scoring/ranking/automatic decisions.

## G. Evidence → Policy → Authorization → Execution — Closed Current Boundary

- [x] Evidence handoff is separate from policy review.
- [x] Policy review is explicit and non-executing.
- [x] Authorization is separate from execution and bounded by explicit autonomy.
- [x] Execution preparation is separate from execution.
- [x] Execution outcomes are provider-independent evidence.
- [x] Execution outcome assessment is non-executing.
- [x] Recovery handoff does not execute recovery.
- [x] Execution adapter access is behind an application-layer port.
- [x] Execution adapter results are runtime-validated.
- [x] Execution attempt history is immutable evidence.
- [x] Retry policy consumes history-consistent attempt evidence.
- [x] Retry orchestration has explicit durable identity and pre-execution revalidation.
- [x] Retry persistence and scheduling are replaceable ports with SQLite V1 adapters.
- [x] Atomic execution claims are separate from execution.
- [x] Retry outcomes do not automatically retry.
- [x] Single-command worker dispatch is implemented.
- [x] Finite bounded worker batch invocation is implemented.
- [x] Continuous single-worker lifecycle is implemented and observable.
- [x] Crash/recovery reconciliation for ambiguous in-flight execution is implemented.
- [x] Provider execution status observation is implemented as non-executing evidence.
- [x] Status reconciliation assessment is implemented.
- [x] Durable expected-state reconciliation application is implemented.
- [x] Status reconciliation coordination is implemented.
- [x] No distributed workers, queue framework, automatic restart, or automatic re-execution are implied by these boundaries.

## H. Explicitly NOT Closed — Do Not Mark as Completed

These remain legitimate future targets and must not be accidentally placed in the neglect list:

- [ ] Real marketplace/provider adapters and credentials.
- [ ] Real external marketing/social/ad adapters.
- [ ] Payment execution and reconciliation.
- [ ] Production UI/dashboard and Windows/mobile/web interfaces.
- [ ] Production background daemon/queue infrastructure.
- [ ] Distributed workers, leases, heartbeats, worker pools.
- [ ] Automatic restart.
- [ ] Automatic retry / automatic provider re-execution.
- [ ] Portfolio posture/allocation policy and capital execution.
- [ ] Cross-business resource optimization.
- [ ] AI provider selection/execution policy.
- [ ] Production deployment/observability infrastructure.
- [ ] Broader business-memory/cross-domain learning.
- [ ] Controlled experimentation infrastructure.

## I. Historical Wording Warning

Older roadmap/decision-log entries may still describe an earlier "next slice" such as lifecycle or crash recovery even though those slices are already implemented. The canonical current state and merged code take precedence. Future documentation reconciliation should remove stale forward-looking wording rather than reopening completed work.

## J. Autonomous-Work Rule

When choosing the next task:

1. Do not reimplement anything in sections A–G.
2. Verify the current GitHub state before claiming a target is complete.
3. If a task touches a closed boundary, treat it as hardening/regression work only unless a new requirement explicitly reopens the design.
4. Prefer the next unresolved boundary from section H or a concrete product consumer that connects existing foundations.
5. Every new boundary still follows:
   **UNDERSTAND → MAP → DESIGN → TRADE-OFFS → DECIDE → RED → GREEN → HARDEN → DOCUMENT → CI → MERGE → RECONCILE.**
