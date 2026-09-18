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

Economic assessment is derived from explicit assumptions, metrics, and opportunity/business-model information.

Expected economics and actual outcomes remain distinct.

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

**Opportunity/Business → Economic Profile**

**Demand/Opportunity → Business Model Hypotheses**

**Venture → Evidence-aware Venture Evaluation**

**Venture → Explicit Lifecycle Stage**

No marketplace SDK, persistence, API, UI, AI provider, or financial execution is required for these slices.
