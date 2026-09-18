# Architecture

## Architectural Direction

The initial architecture is a **Modular Monolith**.

The system should keep business domains internally separated while avoiding distributed-system complexity until real requirements justify it.

## High-Level Layers

- API / Interface
- Application
- Domain
- Infrastructure
- External Platform Adapters
- AI / Capability Orchestration

## Domain Candidates

- Opportunity
- Client
- Opportunity Intelligence / Evaluation
- Proposal / Pricing
- Project
- Execution
- Communication
- Revision
- Quality Gate
- Analytics / Business Intelligence
- AI Operations
- Experimentation / Release Management

These are candidate boundaries, not permission to create modules without a demonstrated responsibility.

## Dependency Direction

Business meaning should remain independent of delivery mechanisms and infrastructure. External platforms and AI providers are replaceable at explicit boundaries.

## Marketplace Integration Strategy

The core domain is marketplace-independent.

A marketplace is selected at runtime through configuration/policy. Multiple marketplaces may be enabled simultaneously. The domain must not encode assumptions that require a particular marketplace.

Each marketplace is isolated behind a replaceable adapter boundary responsible for provider-specific concerns such as:
- authentication and authorization
- API/transport behavior
- rate limits and provider constraints
- mapping provider data into external observations
- provider-specific submission/communication mechanics
- provider-specific error handling

Marketplace integrations are independently evolvable capabilities. Their quality and business value can be evaluated using operational metrics, reports, user feedback, comments, and AI-assisted recommendations.

## First Vertical Slice

Marketplace-independent domain behavior:

External Opportunity Observation → Normalization → Opportunity → Evaluation Policy → Evaluation Result.

The first slice should validate the domain without requiring a real marketplace integration, persistence engine, API framework, dashboard, or AI provider.

A later integration slice can plug a concrete marketplace adapter into the established boundary without changing the core Opportunity Intelligence semantics.
