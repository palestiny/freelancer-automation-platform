# Architecture

## Architectural Direction

The system is a **Modular Monolith**.

Business domains remain internally separated while distributed-system complexity is deferred until requirements justify it.

## Platform Shape

The platform is an **Economic Opportunity OS / Business Automation OS**.

Freelancing is the first laboratory, not the permanent architectural boundary.

## Domain Areas

### Market Intelligence

Future responsibility:

- market observations
- demand signals
- research provenance
- data quality
- competitor and trend observations

### Opportunity Intelligence

Owns:

- opportunity representation
- opportunity type
- normalization
- applicable opportunity evaluation
- evidence and uncertainty
- qualification results

The existing six-dimension model remains intact for its applicable opportunity context.

### Business Model Discovery

Owns:

- alternative business-model hypotheses
- customer/value proposition
- revenue model
- recurring revenue attributes
- automation intensity

### Business Economics

Owns:

- economic assumptions
- expected revenue
- expected cost
- expected profit
- expected margin
- profit per hour
- risk-adjusted economics
- economic health profile

It may consume resource usage and capacity information, but it does not own capacity scheduling.

### Resource Economics

Owns:

- explicit resource consumption
- resource kind
- quantity
- monetary unit cost
- derived resource cost

V1 resource kinds are HUMAN_TIME, CAPABILITY_USAGE, INFRASTRUCTURE, COMMUNICATION, MARKETPLACE_FEE, and REVIEW_TIME.

### Capacity

Owns constrained human-time availability for a defined planning period:

- total hours
- committed hours
- reserved hours
- remaining hours
- utilization

V1 intentionally models capacity as a snapshot rather than a scheduling system.

### Economic Health

Owns the changeable economic-quality view of a business/opportunity:

- profitability
- profit potential
- profit stability
- demand stability
- safety
- recurring revenue
- automation
- capital efficiency
- scalability
- evidence quality

The Economic Health model is a score vector, not a universal master score.

Scores are derived from evidence and metrics. Scoring policy remains separate so it can evolve by opportunity/business type.

### Venture Intelligence

Owns broader venture evaluation across market, economics, automation, scalability, risk, evidence quality, strategic fit, and expansion potential.

It is intentionally separate from the freelance Opportunity Evaluation model.

### Decision & Portfolio Planning

Future responsibility:

- opportunity selection
- portfolio allocation
- capacity-aware planning
- capital allocation
- opportunity cost
- business objectives
- policy-derived economic posture

Portfolio posture may distinguish protection, maintenance, controlled optimization, growth, harvesting, turnaround, and exit without making any of those states intrinsic to a business.

### Capability & Execution

Future responsibility:

- capability registry
- capability selection
- cost/quality/reliability metadata
- execution planning
- execution monitoring

AI providers and tools are capabilities, not domain owners.

### Quality & Delivery

Future responsibility:

- quality gates
- verification
- delivery readiness
- acceptance evidence
- revision handling

### Measurement & Learning

Future responsibility:

- expected vs actual
- variance
- outcome metrics
- capability performance
- marketplace performance
- venture/business performance
- business memory
- learning signals

### Experimentation & Validation

Future responsibility:

- validation experiments
- hypotheses
- controlled variants
- measurable outcomes
- promotion/rejection decisions

### Revenue Engine

Future responsibility:

- demand acquisition
- offer design
- pricing
- conversion
- retention
- expansion
- recurring revenue

## Cross-Cutting Concerns

- Policy
- Risk
- Auditability
- Explainability
- Autonomy
- Versioning
- Resource constraints
- Provenance
- Capital constraints

## High-Level Layers

- Interface / API
- Application
- Domain
- Infrastructure
- External Platform Adapters
- Capability / AI Integrations

Business meaning remains independent from delivery mechanisms.

## Dependency Direction

**Business Meaning → Domain Model → Application Logic → Infrastructure → External Systems**

Domain logic must not depend on:

- HTTP frameworks
- databases/ORMs
- marketplace SDKs
- UI frameworks
- AI providers
- financial execution providers

## External Data Boundary

**External Observation → Normalization → Data Quality → Analysis → Hypothesis → Business Decision**

External observations never become business truth automatically.

## Economic Boundary

Economic assessment is derived from explicit assumptions, metrics, resource information, and opportunity/business-model information.

Expected economics and actual outcomes remain distinct.

Resource cost is not the same concept as profit. Capacity is an operational constraint and not an economic-quality score.

Economic quality is multidimensional. Profitability, stability, safety, demand stability, recurring revenue, automation, capital efficiency, scalability, and evidence quality may all matter simultaneously.

No permanent universal master score is part of the domain contract.

## Marketplace Strategy

Marketplace integrations are replaceable adapters responsible for provider-specific authentication, transport, rate limits, mapping, submission, and errors.

Marketplace choice is configuration, not Opportunity identity.

## Autonomy Boundary

Automation operates under explicit policy:

- L0 Observe
- L1 Recommend
- L2 Prepare
- L3 Execute with Approval
- L4 Execute Automatically within Policy
- L5 Optimize within Policy

AI cannot bypass the policy boundary.

## Financial Boundary

Investment analysis and capital-allocation reasoning are domain concerns.

Actual financial transactions are external, high-risk actions and remain outside the current implementation boundary until explicit policy, permissions, auditability, and approval controls are designed.

## First Vertical Slice

Current domain slices include:

**External Opportunity Observation → Normalized Opportunity → Opportunity Evaluation**

**Opportunity → Economic Estimate**

**Resource Consumption → Resource Cost**

**Human-Time Capacity → Remaining Capacity / Utilization**

**Opportunity/Business → Economic Profile**

**Demand/Opportunity → Business Model Hypotheses**

**Venture → Evidence-aware Venture Evaluation**

**Venture → Explicit Lifecycle Stage**

No marketplace SDK, persistence, API, UI, AI provider, or financial execution is required for these slices.


## Marketing & Growth Automation

Marketing/Growth is a first-class future domain connected to Revenue Engine, Experimentation & Validation, and Measurement & Learning.

It owns:

- campaign intent
- objective
- target audience and positioning metadata
- channel selection
- campaign lifecycle
- budget constraints
- authorization state
- provider-independent performance observations
- derived campaign metrics

It does not own provider credentials, social-network APIs, advertising SDKs, or AI models.

### Campaign Boundary

The domain represents a campaign as a business experiment, not as a provider-specific ad object.

External flow:

**Campaign Intent → Policy/Authorization → Provider Adapter → External Execution → Performance Observation → Normalization → Measurement → Learning**

The current foundation includes a provider-independent campaign lifecycle and performance snapshot.

### Marketing Safety Boundary

Paid advertising can spend money and social/customer actions can create external commitments. Therefore:

- campaign spend is subject to explicit budget and authorization policy;
- account creation requires explicit authorization;
- public publishing and responses require content/brand/privacy policy;
- sensitive actions may require approval;
- AI may prepare or recommend content but cannot bypass policy.

No real ad spend, credentials, social account creation, or provider API is part of the current domain-only implementation.

## Market Intelligence Boundary

The first Market Intelligence slice is provider-independent:

**External Observation → MarketObservation → DemandSignal → Opportunity Hypothesis**

MarketObservation preserves provenance and observation time.

DemandSignal preserves derived demand strength and evidence quality plus the number of supporting observations.

The domain intentionally does not implement scraping, search APIs, social APIs, marketplace APIs, or AI research providers. Those belong behind replaceable external capabilities.

## Venture Validation & Experimentation Boundary

The first validation slice is provider-independent:

**Venture Thesis → ValidationExperiment → External Execution Boundary → ExperimentResult → Evidence / Decision**

The domain owns experiment meaning:

- hypothesis
- objective
- success criterion
- controlled variants
- budget constraint
- lifecycle
- measured result
- explicit decision

The domain does not own:

- ad or marketplace execution
- customer communication
- scheduling
- statistical inference
- financial spending
- persistence
- automatic venture lifecycle mutation

External execution remains behind capabilities/adapters and authorization policy. Experiment results become evidence; learning cannot silently rewrite policy.


## Revenue Engine Boundary

The revenue domain is provider-independent.

It owns:

- RevenueContract
- RevenueType
- RecurringPeriod
- RevenueEvent

It does not own:

- payment processor integration
- money movement
- refunds
- invoicing
- tax accounting
- provider reconciliation
- automatic pricing

**Business Model → Revenue Contract → Payment Capability Boundary → Revenue Event → Economic/Learning Loop**

Actual revenue remains distinct from expected revenue.


## Social Presence & Customer Communication Boundary

The domain owns communication meaning:

- SocialPresence
- IncomingMessage
- MessageClassification
- ResponseDraft
- ResponseAuthorization
- SentMessage
- escalation state

Adapters/capabilities own provider-specific operations such as account access, publishing, sending, and webhook/API handling.

Credentials are not part of the domain model. AI is a replaceable drafting/classification capability.


## Campaign Optimization & Budget Policy

The campaign domain separates performance observation from optimization policy and recommendation.

**Performance Observation → Optimization Policy → Recommendation → Authorization → External Execution → New Observation**

The V1 optimization foundation owns changeable thresholds and non-executing recommendations. Budget limits are hard safety constraints. Insufficient evidence cannot produce a budget-changing recommendation.

It does not own ad-provider APIs, credentials, payment execution, statistical attribution, or automatic spend.


## Business Operations & Multi-Business Execution

Business operations now have an explicit provider-independent domain foundation:

**Business → Operational Cycle → Work Item → Outcome Observation → Measurement / Learning**

Business identity is separate from operational state. Each cycle and work item belongs to one business, preventing cross-business execution and measurement contamination. Scheduling, workers, provider APIs, credentials, payments, and AI remain outside the domain.


## Operational Measurement & Learning Boundary

The current operational learning foundation is provider-independent:

**Work Item → Outcome Observation → Measurement → Variance → Learning Signal → Improvement Recommendation → Policy Review / Experiment**

The domain owns the meaning of outcomes, expected-vs-actual measurements, variance, business performance snapshots, learning signals, and explicit improvement handoffs.

It does not own scheduling, workers, persistence, external providers, AI model selection, automatic policy mutation, automatic experiment execution, or financial execution.

Business ownership is enforced on measurements and snapshots to prevent cross-business contamination.


## Business Performance History Boundary

Business Performance History is a normalized evidence view across bounded source domains:

**Source Observation → Normalized Business Performance Observation → Business Performance History → Analysis / Learning**

The normalized observation preserves:

- business identity
- source type and source identifier
- metric and unit
- optional expected value
- actual value
- observation time
- evidence quality

It derives variance only when an expected value exists. The history enforces one-business isolation and provides deterministic ordering and metric filtering.

The history model does not replace operational, revenue, campaign, or economic source models and does not mutate them. Source-specific mapping belongs outside this core model.

Persistence, statistical inference, attribution, and automatic policy changes remain outside the current slice.
## Business Performance Aggregation Boundary

The Measurement & Learning area now includes a deterministic historical aggregation layer:

**BusinessPerformanceObservation → PerformanceWindow → PerformanceAggregate → Trend / Learning**

The aggregate is a derived, provider-independent view. It preserves business identity, metric/unit, explicit window, evidence quality, and source observation identifiers.

V1 provides count, average, minimum, maximum, and expected-derived variance summaries. Missing expected values are not treated as zero, and zero expected values do not produce relative variance.

Universal summation, statistical inference, persistence, attribution, automatic policy mutation, and external execution remain outside this slice.

## Performance Trend & Baseline Boundary

Measurement & Learning now includes a deterministic comparison layer:

**PerformanceAggregate(current) + PerformanceAggregate(baseline) → PerformanceTrend**

The comparison requires compatible business/metric/unit context and explicit windows. It reports average-level absolute and relative change while preserving source observation identifiers and evidence quality.

Trend output is descriptive evidence only. Forecasting, statistical significance, seasonality, anomaly detection, and automatic policy mutation remain outside this boundary.
