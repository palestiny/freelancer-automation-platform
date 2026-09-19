# Roadmap

## Phase 0 — Product & Architecture

Define product boundaries, domain model, economics, architecture, security, integration strategy, observability, experimentation, and engineering workflow.

**Status:** Economic Opportunity OS direction approved; modular-monolith and provider-independent domain boundaries established.

## Phase 1 — Opportunity Intelligence

Build:
- marketplace-independent opportunity contracts
- opportunity types
- normalization
- six-dimensional evaluation where applicable
- configurable policy
- evidence and uncertainty
- persistence
- API/dashboard exposure

**Status:** Domain foundations and TDD coverage implemented. Persistence/API/UI remain future slices.

## Phase 2 — Business Economics & Resource Economics

Build:
- economic estimates
- actual-vs-expected economics
- resource cost model
- capacity representation
- profit and margin reporting
- risk-adjusted economics
- opportunity cost
- economic health metrics and history

**Status:** EconomicEstimate, EconomicProfile, ResourceUsage, ResourceKind, and human-time CapacitySnapshot foundations implemented. Actual-vs-expected history, opportunity cost, and historical economics remain future slices.

## Phase 3 — Market Intelligence & Demand Discovery

Build:
- market observations
- demand signals
- competitor/trend observations
- source provenance
- evidence quality
- demand-to-opportunity transformation

**Status:** Initial provider-independent MarketObservation and DemandSignal foundation implemented. Source normalization, trend detection, competitor analysis, and persistence remain future slices.

## Phase 4 — Business Model & Venture Discovery

Build:
- business-model hypotheses
- multiple models per demand signal
- venture thesis
- venture evaluation
- venture lifecycle
- low-touch recurring-revenue attributes

**Status:** Domain foundations implemented.

## Phase 5 — Venture Validation & Experimentation

Build:
- validation experiment model
- cheapest credible validation path
- measurable hypotheses
- controlled variants
- experiment outcomes
- explicit promotion/rejection

**Status:** Provider-independent validation experiment foundation implemented. External execution, statistical methodology, scheduling, and automated promotion remain future work.

## Phase 6 — Decision, Portfolio & Capital Allocation

Build:
- economic posture rules
- opportunity prioritization
- capacity-aware allocation
- capital constraints
- opportunity cost
- portfolio objectives
- evidence-adjusted capital allocation
- human approval controls
- protection of stable profitable assets

**Status:** Design direction exists; portfolio allocation and capital execution are intentionally not implemented.

No automatic capital movement until explicit policy and safety design are approved.

## Phase 7 — Revenue Engine

Build:
- demand acquisition
- offer design
- pricing
- conversion
- delivery
- retention
- expansion
- recurring revenue

**Status:** Provider-independent RevenueContract and RevenueEvent foundation implemented. Payment execution, reconciliation, invoicing, and automatic pricing remain future work.

## Phase 8 — Capability & Project Execution

Build:
- capability registry
- capability selection
- execution planning
- task execution
- verification
- delivery preparation
- execution monitoring

**Status:** Core capability/execution orchestration is not yet implemented. Provider-independent domain foundations exist elsewhere in the roadmap; this phase remains future implementation work.

## Phase 9 — Client Communication & Service Operations

Build:
- communication state machine
- requirement clarification
- negotiation support
- feedback interpretation
- revision planning
- redelivery
- client success

**Status:** Provider-independent SocialPresence, IncomingMessage, ResponseDraft, authorization, escalation, and SentMessage foundation implemented. External delivery remains future work.

## Phase 10 — Measurement, Business Memory & Learning

Build:
- expected vs actual metrics
- variance analysis
- revenue/cost/margin tracking
- delivery time
- acceptance and revision metrics
- capability performance
- venture/business performance
- business memory
- learning signals

**Status:** Phase 16 now contains the dedicated outcome/measurement/learning foundation. Phase 10 remains the broader cross-domain measurement/memory destination; the implemented Phase 16 work is the first operational foundation for that direction.

## Phase 11 — Progressive Autonomy

Build:
- policy versioning
- autonomy levels
- approval workflows
- controlled optimization
- safe automation boundaries
- auditability

**Status:** Autonomy boundaries and approval principles are established. Full policy/versioning/approval infrastructure remains future work.

## Phase 12 — Multi-Marketplace, Multi-Business & Interfaces

Add:
- multiple marketplace adapters
- productized/managed services
- SaaS/API businesses
- games and digital products
- partnerships/acquisitions
- investment research
- web/Windows/mobile interfaces

**Status:** Strategic direction approved. Adapters and interfaces remain future work.

Interfaces must not duplicate business logic.

## Phase 13 — Marketing & Growth Automation

Build:
- positioning and offer definition
- campaign domain and policy
- organic/paid channel planning
- content/post planning
- authorized social presence
- lead acquisition
- customer/comment monitoring
- policy-bound response handling
- campaign measurement
- CAC, conversion, revenue, and ROAS analysis
- controlled campaign experiments
- campaign-to-business economic learning

**Status:** Campaign, communication, and campaign-optimization foundations implemented. External advertising/social integrations and real spend remain future work.

## Phase 14 — Business Operations & Multi-Business Execution

Build:
- business identity and lifecycle
- operational cycles
- work item lifecycle
- explicit business ownership/isolation
- provider-independent execution meaning
- operational outcome evidence

**Status:** Business, OperationalCycle, and WorkItem foundations implemented. Scheduling, workers, external execution, and cross-business optimization remain future work.

## Phase 15 — Campaign Optimization & Budget Policy

Build controlled optimization around measured campaign performance:
- optimization policy
- evidence sufficiency
- budget adjustment recommendations
- pause/continue recommendations
- hard budget limits
- explicit authorization boundaries

**Status:** Provider-independent recommendation foundation implemented. External execution and automatic spend remain future work.

## Phase 16 — Operational Measurement & Learning Integration

Build the missing bridge between operating businesses and the learning loop:
- work-item outcome observations
- expected-vs-actual operational measurements
- business performance history
- variance analysis
- learning signals
- evidence-linked improvement recommendations
- explicit policy/experiment handoff

**Status:** Provider-independent operational outcome, measurement, learning-signal, improvement-handoff, historical aggregation, trend/baseline comparison, evidence eligibility, provenance, source-reliability, evidence-aware operational learning, and the first statistical evidence capabilities are implemented across Phases 16–17. Persistence and external execution remain future work.

## Phase 17 — Statistical Learning & Inference

Build statistical evidence capabilities only through concrete, independently gated use cases.

**Status:** CLOSED for the current V1 statistical-method boundary. Student's t mean uncertainty and Welch's two-sample historical mean comparison are implemented and hardened. Further methods require a concrete downstream consumer and dedicated design gate.

### Phase 17 — Statistical Learning & Inference

**Status:** CLOSED for the current V1 statistical-method boundary.

Implemented and verified:
- Student's t mean uncertainty for an explicit historical mean.
- Welch's two-sample historical mean comparison for two explicit non-overlapping windows.
- explicit applicability and validation precedence.
- unique observation lineage and method provenance.
- standard-library numerical hardening and regression coverage.

No forecasting, causal inference, anomaly detection, automatic method selection, policy mutation, portfolio allocation, persistence, or external execution is included.

**Next boundary:** identify a concrete downstream consumer of statistical evidence before adding another statistical method or automatic integration.

## Guiding Rule

The roadmap grows the platform from a measurable freelance laboratory into a multi-business economic operating system without prematurely implementing every future capability.

Each increment is complete only when applicable design, RED/GREEN TDD, review/refactoring, documentation, tests, commit/push, and project-state update are completed and verified.


### Phase 16 — Business Performance History Foundation

Phase 16 includes normalized business performance history, deterministic windows, historical aggregation, descriptive trend comparison, baseline eligibility, provenance compatibility, source reliability, and evidence-aware operational learning. Persistence and statistical inference remain future work.

### Phase 16 — Deterministic Performance Windows

Added `PerformanceWindow`, explicit start-inclusive/end-exclusive selection, and rolling-window construction. These primitives support deterministic historical evidence; statistical inference is implemented separately in Phase 17.
### Phase 16 — Historical Performance Aggregation

The Phase 16 foundation now includes deterministic per-metric aggregation inside explicit performance windows. Aggregates preserve raw observation identifiers and separate actual summaries from expected-derived summaries. Generic V1 aggregation intentionally avoids universal summation semantics. Statistical inference is implemented separately in Phase 17; persistence and automated external learning remain future work.

### Phase 16 — Evidence & Baseline Policy

Build:
- evidence-aware baseline eligibility
- minimum observation requirements
- evidence-quality thresholds
- explicit baseline freshness
- explainable baseline rejection

**Status:** V1 deterministic evidence-aware baseline eligibility foundation implemented. Automatic baseline selection remains future work; statistical inference is implemented separately in Phase 17.

### Phase 16 — Performance Trend & Baseline Analysis

Added a deterministic comparison foundation for explicit current and baseline windows. Comparisons report descriptive average changes and preserve observation provenance. Forecasting, seasonality, anomaly detection, and policy decisions remain future work; bounded significance testing is implemented separately in Phase 17.

### Phase 16 — Bounded Performance Comparison Policy

Build:
- baseline eligibility enforcement
- current evidence sufficiency
- temporal window ordering
- explicit comparison rejection reasons
- descriptive trend handoff

**Status:** V1 deterministic comparison-policy foundation implemented. Forecasting remains future work; statistical inference is implemented separately in Phase 17.

### Phase 16 — Performance Evidence Provenance

Build:
- preserve source-type provenance in historical aggregates
- require compatible provenance context for descriptive comparisons
- retain raw observation identifiers as authoritative lineage
- keep provenance separate from source-reliability scoring

**Status:** V1 provenance-preserving aggregation foundation implemented. Source reliability scoring is implemented separately; causal attribution remains future work.

### Phase 16 — Performance Source Reliability Policy

The Measurement & Learning foundation now includes a provider-independent source-reliability policy. Reliability is explicitly policy-derived and remains separate from observation-level evidence quality. Mixed-source aggregates use the weakest configured source reliability, and missing source configuration blocks eligibility. No provider ranking, causal inference, automatic action, or policy mutation is introduced.

### Phase 16 — Baseline Reliability Integration

Baseline eligibility can now optionally incorporate the explicit source-reliability policy. Source reliability is an additional evidence gate alongside observation count, observation-level evidence quality, and freshness; failures remain explainable.

### Phase 16 — Current Evidence Source Reliability

Comparison policy can now optionally require explicit source reliability for current evidence. This complements baseline reliability without duplicating its logic; current observation sufficiency and evidence quality remain separate requirements.

### Phase 16 — Evidence-Aware Operational Learning

Operational learning now requires an explicit minimum average evidence-quality threshold in addition to repeated observations and material variance. The default preserves the existing evidence baseline, and learning remains a non-executing evidence signal.

### Phase 16 — Closure Review

Current foundation is complete for the deterministic evidence/measurement slice. Before introducing statistical inference, persistence, or external execution, review semantic duplication, policy composition, provenance invariants, and test coverage as a dedicated design gate.


### Phase 16 — Closure Review Completed

**Status:** CLOSED for the deterministic domain slice. Semantic policy composition, provenance, temporal boundaries, evidence lineage, and test coverage were reviewed. No additional cross-domain abstraction was justified. Statistical inference, persistence, and external execution remain future capabilities requiring dedicated design gates.


## Phase 17 — Statistical Learning & Inference

**Status:** CLOSED for the current V1 statistical-method boundary. Two narrow statistical use cases are implemented and verified: Student's t mean uncertainty and Welch's two-sample historical mean comparison.

Next boundary: identify a concrete downstream consumer for statistical evidence before adding another method or automatic integration.


### Phase 17 — Statistical Evidence Composition Consumer

**Status:** V1 downstream consumer implemented and verified. Existing Welch statistical evidence can now be composed with explicit evidence-quality and source-reliability gates without universal scoring or automatic action.

Next extension remains consumer-driven and requires a dedicated design gate if it changes the statistical surface or introduces a new decision-support semantic.




### Evidence Posture Hardening

**Status:** Completed and CI-verified. Descriptive direction and statistical detection remain explicitly separate; no directional inference is created from statistical significance alone.




### Evidence Decision Support

**Status:** V1 descriptive + inferential evidence composition implemented and CI-verified. The boundary remains non-decisioning; future automation requires an explicit policy/design gate.


### Evidence Composition Boundary

**Status:** Implemented and hardened. The current V1 boundary exposes descriptive performance direction and inferential statistical detection as separate evidence dimensions. It is intentionally non-decisioning; further automation requires an explicit policy/design gate.


### Phase 2 — Actual-vs-Expected Economic Performance

**Status:** V1 economic performance history foundation implemented and CI-verified. Estimates remain separate from realized outcomes; profitability and variance can now be represented as historical evidence. Aggregation, economic health history, opportunity cost, and execution remain future slices.


### Phase 2 — Economic Performance Aggregation

**Status:** V1 deterministic historical aggregation implemented and CI-verified. Raw realized outcomes remain authoritative; aggregates are derived views only. Economic health/stability policy remains a separate future slice.


### Phase 2 — Economic Health & Stability Evidence

**Status:** V1 descriptive evidence implemented and CI-verified. Profitability and stability are now measurable from realized outcomes without a universal health score or automatic business posture.


### Economic Health Window Hardening

**Status:** Completed and CI-verified. Economic health evidence is now explicitly window-scoped and lineage-safe.


### Phase 2 — Economic Stability Policy

**Status:** V1 configurable eligibility policy implemented and CI-verified. Stable profitability is now expressible as an explicit policy result with deterministic reasons, without automatic portfolio action.


### Economic Stability Evidence Support

**Status:** V1 consumer implemented and CI-verified. Economic health metrics and stability-policy eligibility can now be consumed together without collapsing them into a score or automatic business/portfolio action.
