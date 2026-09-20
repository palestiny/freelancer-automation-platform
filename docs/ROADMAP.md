# Roadmap

## Phase 0 — Product & Architecture
**Status: ESTABLISHED**

Economic Opportunity OS direction, modular-monolith architecture, provider-independent domain boundaries, replaceable AI/capability integrations, evidence taxonomy, progressive autonomy, and safety boundaries are established.

## Phase 1 — Opportunity Intelligence
**Status: FOUNDATION IMPLEMENTED**

Marketplace-independent opportunity contracts, opportunity types, six-dimensional evaluation, evidence/uncertainty, and configurable policy foundations exist. Persistence, API, UI, and real marketplace adapters remain future application slices.

## Phase 2 — Business Economics & Resource Economics
**Status: FOUNDATION IMPLEMENTED**

Economic estimates, economic profiles, resource usage, human-time capacity, realized economic evidence, economic health/stability evidence, and bounded opportunity-cost evidence exist. Portfolio allocation and financial execution remain outside scope.

## Phase 3 — Market Intelligence & Demand Discovery
**Status: FOUNDATION IMPLEMENTED**

Market observations and demand signals exist with provenance/evidence quality. Normalization, trend intelligence, competitor intelligence, and persistence remain future slices.

## Phase 4 — Business Model & Venture Discovery
**Status: FOUNDATION IMPLEMENTED**

Business-model hypotheses, venture evaluation/lifecycle, and recurring-revenue/automation attributes exist.

## Phase 5 — Venture Validation & Experimentation
**Status: FOUNDATION IMPLEMENTED**

Validation experiments, explicit variants, measurable results, and explicit promotion/rejection decisions exist. External experiment execution remains future work.

## Phase 6 — Decision, Portfolio & Capital Allocation
**Status: STRATEGIC DESIGN ONLY**

Portfolio posture, allocation policy, opportunity prioritization, and capital constraints remain future policy slices. Automatic capital movement is explicitly outside the current boundary.

## Phase 7 — Revenue Engine
**Status: FOUNDATION IMPLEMENTED**

Revenue contracts and realized revenue events exist. Payment execution, reconciliation, invoicing, and automatic pricing remain future work.

## Phase 8 — Capability & Project Execution
**Status: PARTIAL / FOUNDATIONS IN PLACE**

Capability/execution contracts and the current generic execution boundary exist, but full marketplace/provider capability execution remains future work.

## Phase 9 — Client Communication & Service Operations
**Status: FOUNDATION IMPLEMENTED**

Provider-independent presence, incoming messages, classification, drafts, authorization, escalation, and sent-message contracts exist. External delivery remains future work.

## Phase 10 — Measurement, Business Memory & Learning
**Status: OPERATIONAL FOUNDATION IMPLEMENTED**

Expected-vs-actual measurement, business performance history, windows, aggregation, trend/baseline comparison, evidence quality, source reliability, learning signals, and improvement handoffs exist.

## Phase 11 — Progressive Autonomy
**Status: V1 EXECUTION BOUNDARIES IMPLEMENTED**

Authorization, autonomy bounds, human-approval requirements, safety blocks, execution preparation, provider-independent outcomes, recovery policy, execution coordination, retry policy, durable retry infrastructure, worker dispatch, and provider-failure handling exist.

**Current runtime slice:** crash/recovery reconciliation, provider status observation, durable assessment application, and single-observation coordination are implemented and CI-verified.

## Phase 12 — Multi-Marketplace, Multi-Business & Interfaces
**Status: STRATEGIC DIRECTION**

Marketplace adapters, multi-business interfaces, Windows/mobile/web interfaces, and broader business types remain future application slices. Business isolation is already a domain invariant.

## Phase 13 — Marketing & Growth Automation
**Status: FOUNDATION IMPLEMENTED**

Campaigns, measurable performance, optimization policy, communication boundaries, and non-executing recommendations exist. External ad/social integrations and real spend remain future work.

## Phase 14 — Business Operations & Multi-Business Execution
**Status: FOUNDATION IMPLEMENTED**

Business identity, lifecycle, operational cycles, work items, outcomes, and business isolation exist. General scheduling and production worker infrastructure remain future work.

## Phase 15 — Campaign Optimization & Budget Policy
**Status: FOUNDATION IMPLEMENTED**

Evidence-gated optimization recommendations, budget limits, and authorization boundaries exist. Automatic spend remains outside the current boundary.

## Phase 16 — Operational Measurement & Learning Integration
**Status: CLOSED FOR CURRENT DETERMINISTIC SURFACE**

Performance history, explicit windows, historical aggregation, trend comparison, baseline eligibility, provenance compatibility, source reliability, and evidence-aware operational learning are implemented and hardened.

## Phase 17 — Statistical Learning & Inference
**Status: CLOSED FOR CURRENT V1 METHOD SURFACE**

Student's t mean uncertainty and Welch's two-sample historical mean comparison are implemented and hardened. The statistical surface is extended only by concrete downstream use cases with dedicated design gates.

## Current Cross-Phase Pipeline

**Observe → Normalize → Measure → Compare → Infer → Compose Evidence → Handoff → Review Policy → Authorize → Prepare → Execute → Observe Outcome → Recover / Learn**

The pipeline deliberately separates evidence, policy, authorization, and execution.

## Current Runtime Boundary

The retry runtime boundary now includes bounded worker invocation, continuous single-worker lifecycle, crash/recovery reconciliation, provider status observation, deterministic assessment, atomic expected-state application, and single-observation coordination. Distributed workers, queue frameworks, automatic restart, polling, and automatic re-execution remain outside scope.

## Future Strategic Work

- production marketplace/provider adapters
- persistence/API/UI integration
- broader business-model execution
- business memory and cross-domain learning
- controlled experimentation infrastructure
- portfolio posture and allocation policy
- progressive autonomy beyond the current bounded execution runtime

## Engineering Rule

**UNDERSTAND → MAP → DESIGN → TRADE-OFFS → DECIDE → RED → GREEN → HARDEN → DOCUMENT → CI → MERGE → RECONCILE**

No new infrastructure or policy is introduced merely because a lower-level capability exists.


### Retry Runtime Observability

**Status:** V1 immutable invocation observation implemented and CI-verified. This records finite runtime outcomes without introducing a metrics backend, daemon, queue, or automatic recovery.


### Evidence Decision Support

**Status:** V1 descriptive + inferential evidence composition implemented and CI-verified. The boundary remains non-decisioning; future automation requires an explicit policy/design gate.


### Continuous Retry Worker Lifecycle

**Status:** V1 lifecycle controller and immutable lifecycle observation implemented and CI-verified. The continuous runtime remains single-worker and non-distributed; crash/recovery reconciliation is the next separate boundary.


### Retry Worker Runtime Lifecycle

**Status:** V1 lifecycle controller and immutable lifecycle observation implemented and CI-verified. The continuous runtime remains single-worker and non-distributed; crash/recovery reconciliation and production deployment lifecycle are separate boundaries.


### Retry Worker Crash / Recovery Reconciliation

**Status:** DESIGN GATE APPROVED — provider-independent ambiguous in-flight execution reconciliation defined. No provider status polling or automatic retry is included.


### Retry Worker Crash / Recovery Reconciliation

**Status:** V1 provider-independent reconciliation implemented and CI-verified. Unknown provider outcomes remain unknown, terminal commands are not reopened, and no automatic re-execution or provider polling is introduced.


### Provider Execution Status Observation

**Status:** V1 observation boundary implemented and CI-verified. Provider-specific status adapters, continuous polling, automatic reconciliation, and automatic re-execution remain outside this boundary.


### Retry Status Reconciliation Assessment

**Status:** V1 non-mutating assessment implemented and CI-verified. Durable state application, provider polling, automatic retry, and automatic execution remain outside the boundary.


### Retry Status Assessment State Application

**Status:** V1 durable application implemented and CI-verified. State mutation uses expected-state compare-and-set; ambiguous outcomes, terminal commands, and stale concurrent applications do not trigger automatic re-execution.


### Retry Status Reconciliation Coordination

**Status:** V1 application coordination implemented and CI-verified. One provider status observation is composed with deterministic assessment and atomic state application; no polling, automatic retry, or provider re-execution is introduced.


### Performance Evidence Decision Support — Current State

**Status:** V1 descriptive + inferential evidence composition is implemented and CI-verified. The boundary remains non-decisioning; future automation requires an explicit policy/design gate.


### Runtime State Reconciliation

**Status:** Current runtime documentation reconciled with the implemented lifecycle and crash/recovery boundaries. Future runtime work must not reopen completed lifecycle/reconciliation slices without a new requirement.


### Evidence Review Handoff

**Status:** V1 non-executing review handoff implemented and CI-verified. Scheduling, notifications, persistence, authorization, and policy mutation remain separate boundaries.


### Evidence Review Decision

**Status:** V1 explicit non-executing review outcome implemented and CI-verified. Review outcomes remain separate from authorization and execution.


### Provider Adapter Conformance

**Status:** V1 reusable runtime conformance boundary implemented and CI-verified. Concrete provider integrations remain separate provider-specific design and integration work.


### Provider Adapter Registry

**Status:** V1 explicit provider-key registration/resolution implemented and CI-verified. Concrete provider integrations remain separate provider-specific design and integration work.


### Provider Capability Registry

**Status:** V1 explicit capability declaration and lookup implemented and CI-verified. Capability metadata remains non-executing and non-ranking; concrete provider integrations remain a separate boundary.


### Capability-Aware Provider Dispatch

**Status:** V1 explicit capability precondition implemented and CI-verified. Provider capability checks occur before authorized execution dispatch; fallback, ranking, inference, and provider selection remain outside scope.


### Statistical Evidence Lineage Hardening

**Status:** V1 lineage hardening implemented and CI-verified. Welch comparison windows and mean difference are preserved in the downstream statistical evidence artifact.


### Provider Credential Reference

**Status:** V1 opaque credential-reference contract implemented and CI-verified. Secret resolution and concrete provider authentication remain separate infrastructure/integration boundaries.


### Provider Credential Resolution

**Status:** V1 application/infrastructure resolver boundary implemented and CI-verified. Secret stores, rotation/refresh, provider authentication, authorization, and provider execution remain separate boundaries.


### Provider-Authenticated Execution Dispatch

**Status:** V1 application boundary implemented and CI-verified. Capability verification and credential resolution now precede authenticated adapter invocation. Provider-specific authentication, secret stores, refresh/rotation, fallback, and concrete provider integrations remain separate boundaries.


### Evidence-to-Decision Policy Boundary

**Status:** V1 explicit policy evaluation foundation implemented. Decision support remains non-executing and policy inputs remain explicit; executable automation requires a separate authorization/execution gate.


### Evidence-to-Decision Policy Lineage

**Status:** V1 lineage hardening implemented and CI-verified. Policy outcomes now preserve the evidence identity and observation IDs that support them.


### Policy Identity Binding

**Status:** V1 traceability/safety hardening implemented and CI-verified. Evidence policy review and action authorization now share an explicit immutable policy identity/version contract.


### Action Authorization Evidence Lineage

**Status:** V1 lineage hardening implemented and CI-verified. Authorization remains separate from execution and preserves the reviewed evidence context.


### Prepared Execution Request Evidence Lineage

**Status:** V1 traceability hardening implemented and CI-verified. Authorization evidence lineage is preserved into prepared execution requests; execution semantics are unchanged.


### Prepared Execution Request Freshness

**Status:** V1 explicit non-mutating freshness assessment implemented and CI-verified. Freshness is a safety precondition only; re-authorization, retry, scheduling, and provider execution remain separate boundaries.


### Evidence Decision Support

**Status:** V1 descriptive + inferential evidence composition implemented and CI-verified. Future automation requires an explicit policy/design gate.


### Freshness-Aware Provider-Authenticated Dispatch

**Status:** V1 explicit freshness safety precondition integrated into authenticated provider dispatch and CI-verified. Provider execution remains blocked for stale/ineligible prepared requests; retry, scheduling, re-authorization, and fallback remain separate boundaries.


### Evidence → Learning Handoff

**Status:** V1 explicit handoff implemented and CI-verified. Statistical evidence can now reach a controlled policy-review or experiment boundary without automatic policy mutation.


### Business Learning Memory

**Status:** V1 immutable learning-memory artifact implemented and CI-verified. Persistence, querying, retention, cross-business aggregation, and automatic policy mutation remain separate boundaries.


### Learning Lineage Hardening

**Status:** V1 handoff identity and memory source-lineage hardening implemented and CI-verified. No learning-policy or execution behavior changed.


### Performance Evidence Direction Hardening

**Status:** Implemented and CI-verified. Evidence movement is now neutral at the evidence layer; favorable/unfavorable interpretation remains an explicit policy concern.


### Metric Direction Policy

**Status:** V1 explicit metric-polarity interpretation policy implemented and CI-verified. Evidence remains neutral; favorable/unfavorable interpretation requires explicit policy.


### Metric Direction Interpretation in Evidence Decision Support

**Status:** V1 explicit polarity interpretation integrated and CI-verified. Raw movement remains neutral and no action semantics are introduced.


### Canonical Current Boundary Reconciliation — 2026-09-20

Earlier roadmap entries that describe retry lifecycle or crash/recovery reconciliation as the “next” boundary are historical. Those boundaries are implemented and CI-verified.

The current implemented pipeline is:

**Evidence → Policy Review → Authorization → Prepared Execution → Freshness → Capability/Credential Checks → Provider Execution Port → Outcome Observation → Recovery Assessment → Atomic State Application → Learning / Review Evidence**

The next unresolved boundary remains deliberately unselected until a concrete requirement/design gate is established. Candidate areas include provider integrations, production persistence/API/UI, controlled experimentation infrastructure, production background runtime infrastructure, broader business-model execution, cross-domain learning, and progressive autonomy.


### Performance Evidence Persistence

**Status:** V1 durable persistence boundary implemented and CI-verified. Authoritative performance observations are persisted through an application repository port with a reference SQLite adapter; derived evidence remains outside this persistence slice.


### Performance Observation Application Service

**Status:** V1 application use-case boundary implemented and CI-verified. It delegates authoritative observation persistence through the application port and keeps derived analysis outside the write/read service.


### Performance Observation Temporal Contract

**Status:** V1 temporal validity hardening implemented and CI-verified. Naive authoritative observation timestamps are rejected; existing fixtures and temporal expectations were migrated to explicit UTC.


### Controlled Experiment Evidence

**Status:** V1 immutable assignment and observation evidence implemented and CI-verified. Allocation optimization, scheduling, execution, causal/statistical analysis, and automatic experiment decisions remain separate boundaries.


### Controlled Experiment Evidence Readiness

**Status:** V1 readiness assessment implemented and CI-verified. Evidence sufficiency is now a separate handoff from raw experiment evidence; analysis and experiment execution remain separate boundaries.


### Controlled Experiment Outcome Summary

**Status:** V1 descriptive outcome summary implemented and CI-verified. Causal/statistical analysis and automatic experiment decisions remain separate boundaries.


### Controlled Experiment Variant Comparison

**Status:** V1 descriptive two-variant comparison implemented and CI-verified. Difference semantics remain neutral; ranking, winner selection, statistical significance, and automatic experiment decisions remain separate boundaries.


### Controlled Experiment Statistical Comparison

**Status:** V1 inferential comparison implemented and CI-verified. Welch is reused as an approved statistical method; experiment-specific identity remains explicit. No winner selection, causal claim, lifecycle mutation, or execution is introduced.


### Controlled Experiment Evidence Synthesis

**Status:** V1 descriptive + inferential evidence synthesis implemented and CI-verified. Winner selection, causal interpretation, lifecycle mutation, allocation optimization, and execution remain separate boundaries.


### Controlled Experiment Hypothesis Policy

**Status:** V1 explicit hypothesis-policy evaluation implemented and CI-verified. Winner selection, allocation changes, experiment lifecycle mutation, and execution remain separate boundaries.


## Controlled Experiment Policy Review Handoff

V1 now has an explicit non-executing handoff from experiment hypothesis-policy evaluation to downstream review. The handoff preserves experiment/metric/direction, exact policy outcome, explicit handoff identity, and observation lineage. It does not authorize or execute actions.


### Controlled Experiment Authorization Preparation

**Status:** V1 non-authorizing preparation artifact implemented and CI-verified. Generic action authorization remains a separate explicit boundary; execution is unchanged.


### Controlled Experiment Allocation

**Status:** V1 deterministic allocation foundation implemented and CI-verified. Assignment persistence, scheduling/exposure enforcement, provider execution, reallocation, and optimization remain separate boundaries.


### Controlled Experiment Allocation Decision Hardening

**Status:** V1 allocation decision auditability hardening implemented and CI-verified. The decision artifact preserves deterministic allocation context; persistence and exposure enforcement remain separate boundaries.


### Controlled Experiment Assignment Persistence

**Status:** V1 authoritative assignment persistence implemented and CI-verified. Assignment identity is unique, experiment/subject assignment is stable, and later observations can reference persisted assignment identity. Exposure scheduling and provider execution remain separate boundaries.


### Controlled Experiment Exposure Evidence

**Status:** V1 exposure confirmation evidence implemented and CI-verified. Assignment and exposure are now distinct persisted artifacts; delivery scheduling and provider execution remain separate boundaries.


### Controlled Experiment Exposure-to-Outcome Linkage

**Status:** V1 temporal/provenance linkage implemented. Exposure and outcome remain distinct evidence artifacts; linkage does not establish causality or trigger experiment decisions.
