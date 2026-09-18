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

## First Vertical Slice

Freelance Platform Adapter → Opportunity Collection → Normalization → Evaluation → Persistence → API.

The slice should remain small enough to validate the domain model before adding proposals, execution, or communication automation.
