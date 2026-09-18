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

**Status:** Planned. Core capability/execution orchestration is not yet implemented.

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

**Status:** Architectural direction established, but the dedicated outcome/measurement/learning domain is not yet implemented.

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

**Status:** Provider-independent operational outcome, measurement, learning-signal, and improvement-handoff foundation implemented. Repeated-variance learning policy and multi-source evidence foundation are implemented. Persistence, richer provenance, historical aggregation, and automated learning remain future work.

## Guiding Rule

The roadmap grows the platform from a measurable freelance laboratory into a multi-business economic operating system without prematurely implementing every future capability.

Each increment is complete only when applicable design, RED/GREEN TDD, review/refactoring, documentation, tests, commit/push, and project-state update are completed and verified.


### Phase 16 — Business Performance History Foundation

The Phase 16 implementation now includes a normalized `BusinessPerformanceObservation` and business-scoped `BusinessPerformanceHistory`. The history preserves source identity, business isolation, optional expected values, deterministic variance, chronological ordering, and metric/unit filtering. Rich historical aggregation, persistence, and statistical inference remain future work.

### Phase 16 — Deterministic Performance Windows

Added `PerformanceWindow`, explicit start-inclusive/end-exclusive selection, and rolling-window construction. These primitives prepare historical aggregation while deliberately avoiding statistical inference or policy decisions.
### Phase 16 — Historical Performance Aggregation

The Phase 16 foundation now includes deterministic per-metric aggregation inside explicit performance windows. Aggregates preserve raw observation identifiers and separate actual summaries from expected-derived summaries. Generic V1 aggregation intentionally avoids universal summation semantics. Statistical inference, trend modeling, persistence, and automated learning remain future work.

### Phase 16 — Evidence & Baseline Policy

Build:
- evidence-aware baseline eligibility
- minimum observation requirements
- evidence-quality thresholds
- explicit baseline freshness
- explainable baseline rejection

**Status:** V1 deterministic evidence-aware baseline eligibility foundation implemented. Statistical inference and automatic baseline selection remain future work.

### Phase 16 — Performance Trend & Baseline Analysis

Added a deterministic comparison foundation for explicit current and baseline windows. Comparisons report descriptive average changes and preserve observation provenance. Forecasting, significance testing, seasonality, anomaly detection, and policy decisions remain future work.

### Phase 16 — Bounded Performance Comparison Policy

Build:
- baseline eligibility enforcement
- current evidence sufficiency
- temporal window ordering
- explicit comparison rejection reasons
- descriptive trend handoff

**Status:** V1 deterministic comparison-policy foundation implemented. Forecasting and statistical inference remain future work.

### Phase 16 — Performance Evidence Provenance

Build:
- preserve source-type provenance in historical aggregates
- require compatible provenance context for descriptive comparisons
- retain raw observation identifiers as authoritative lineage
- keep provenance separate from source-reliability scoring

**Status:** V1 provenance-preserving aggregation foundation implemented. Source reliability scoring, causal attribution, and statistical inference remain future work.

### Phase 16 — Performance Source Reliability Policy

The Measurement & Learning foundation now includes a provider-independent source-reliability policy. Reliability is explicitly policy-derived and remains separate from observation-level evidence quality. Mixed-source aggregates use the weakest configured source reliability, and missing source configuration blocks eligibility. No provider ranking, causal inference, automatic action, or policy mutation is introduced.
