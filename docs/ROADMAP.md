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

**Next slice:** crash/recovery reconciliation for ambiguous in-flight execution; continuous single-worker lifecycle is implemented.

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

The bounded retry worker batch invocation is implemented. It preserves durable command identity, deterministic scheduled-work selection, atomic claims, authorization/policy revalidation, explicit failure states, bounded termination, and ordered per-invocation results. Continuous worker lifecycle remains a separate future boundary.

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
