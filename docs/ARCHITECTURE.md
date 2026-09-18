# Architecture

## Architectural Direction

The initial architecture is a **Modular Monolith**.

The system keeps business domains internally separated while avoiding distributed-system complexity until real requirements justify it.

## Platform Shape

The platform is a Business Automation OS initially validated through freelance work.

Freelancing is an application/domain context, not the permanent architectural boundary.

## Domain Areas

### Opportunity Intelligence

Owns:

- external observation normalization
- opportunity representation
- six-dimensional evaluation
- evidence and uncertainty
- qualification result

### Business Economics

Owns:

- economic assumptions
- expected revenue
- expected cost
- expected profit
- expected margin
- profit per hour
- risk-adjusted economics

### Decision & Planning

Future responsibility:

- opportunity selection
- portfolio allocation
- capacity-aware planning
- execution strategy selection

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
- variance analysis
- outcome metrics
- capability performance
- marketplace performance
- learning signals

### Experimentation

Future responsibility:

- hypotheses
- controlled policy/strategy variants
- experiment metrics
- promotion/rejection decisions

## Cross-Cutting Concerns

- Policy
- Risk
- Auditability
- Explainability
- Autonomy level
- Versioning
- Resource constraints
- Provenance

## High-Level Layers

- Interface / API
- Application
- Domain
- Infrastructure
- External Platform Adapters
- Capability / AI Integrations

Business meaning must remain independent from delivery mechanisms and infrastructure.

## Dependency Direction

**Business Meaning → Domain Model → Application Logic → Infrastructure → External Systems**

Domain logic must not depend on:

- HTTP frameworks
- databases/ORMs
- marketplace SDKs
- UI frameworks
- AI providers

## External Data Boundary

**External Observation → Normalization → Data Quality → Analysis → Business Decision**

Provider data is an observation, not automatically business truth.

## Economic Boundary

Economic assessment is derived from explicit assumptions and opportunity information.

It must not mutate Opportunity identity.

Expected economics and actual economics are distinct. Actual outcomes later feed the measurement and learning loop.

## Marketplace Strategy

The core domain is marketplace-independent.

Each marketplace is isolated behind a replaceable adapter responsible for provider-specific:

- authentication
- transport/API behavior
- rate limits
- data mapping
- submission mechanics
- provider-specific errors

Marketplace integrations are independently evolvable capabilities.

## Autonomy Boundary

Automation operates under explicit policy.

Future autonomy levels:

- L0 Observe
- L1 Recommend
- L2 Prepare
- L3 Execute with Approval
- L4 Execute Automatically within Policy
- L5 Optimize within Policy

AI cannot bypass the policy boundary.

## First Vertical Slice

The current domain slices are:

**External Opportunity Observation → Normalized Opportunity → Opportunity Evaluation**

and

**Opportunity → Economic Estimate**

No marketplace SDK, persistence, API, UI, or AI provider is required for these slices.
