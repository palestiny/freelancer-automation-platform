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
- controlled experimentation beyond the currently bounded assignment/exposure/evidence infrastructure
- portfolio posture and allocation policy
- progressive autonomy beyond the current bounded execution runtime

## Engineering Rule

**UNDERSTAND → MAP → DESIGN → TRADE-OFFS → DECIDE → RED → GREEN → HARDEN → DOCUMENT → CI → MERGE → RECONCILE**

No new infrastructure or policy is introduced merely because a lower-level capability exists.



## Implemented Current Boundaries

The canonical roadmap above is authoritative. The following cross-cutting boundaries are implemented and verified; their detailed design history belongs in dedicated design gates and the decision log:

- Evidence composition and downstream decision-support handoff.
- Evidence review handoff and explicit non-authorizing review decisions.
- Policy evaluation, evidence/policy lineage, policy identity binding, and action authorization lineage.
- Prepared execution request lineage and freshness safety assessment.
- Provider adapter conformance, registry, capability declaration/verification, credential references/resolution, and authenticated dispatch.
- Performance observation persistence and application-service boundary.
- Controlled experiment assignment, exposure, observation, linkage, lineage, temporal, authority, and idempotency boundaries.
- Execution outcome temporal/type/reference hardening and durable persistence.
- Retry runtime observability, lifecycle control, crash/recovery reconciliation, provider-status observation, deterministic assessment, atomic state application, and single-observation coordination.
- Business learning memory and evidence-to-learning handoff.

These are not invitations to reopen completed slices. New work must start from a concrete unresolved requirement and a dedicated design gate where the boundary changes semantics.

## Current Runtime Safety Boundary

**Evidence → Policy Review → Authorization → Preparation → Freshness → Capability/Credential Checks → Provider Execution Port → Outcome Observation → Recovery Assessment → Atomic State Application → Learning / Review Evidence**

The system remains provider-independent at the domain boundary. Distributed workers, queue frameworks, automatic restart, continuous provider polling, unrestricted automatic re-execution, payment execution, automatic capital movement, and portfolio allocation execution remain outside the current boundary.

## Engineering Rule

**UNDERSTAND → MAP → DESIGN → TRADE-OFFS → DECIDE → RED → GREEN → HARDEN → DOCUMENT → CI → MERGE → RECONCILE**

No new infrastructure or policy is introduced merely because a lower-level capability exists.


### Persisted Execution Coordination

**Status:** V1 application boundary implemented and CI-verified. Authoritative execution outcomes are persisted before policy assessment/recovery handoff; no new retry or execution semantics are introduced.


### Current Evidence Interpretation

**Status:** Explicit metric-polarity interpretation is implemented and bounded. Controlled-experiment evidence lineage and retry-safe exposure recording are implemented; causal attribution and automatic experiment optimization remain outside scope.


### Evidence Decision Support

**Status:** V1 descriptive + inferential evidence composition implemented and CI-verified. The boundary remains non-decisioning; future automation requires an explicit policy/design gate.


### Statistical Direction Provenance

**Status:** Hardened and CI-verified. Inferential direction is preserved from the Welch mean difference and descriptive/inferential disagreement remains explicit.

### Evidence Decision Support

**Status:** V1 descriptive + inferential evidence composition implemented and CI-verified. Future automation requires an explicit policy/design gate.


