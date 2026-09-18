# Project State

## Current Phase

**Phase 0 — Product & Architecture**

## Completed

- Repository created and verified through GitHub integration.
- Initial README committed.
- Shared engineering working rules established.
- Product direction established: a controlled autonomous freelancer lifecycle platform.

## Current Design Gate

### Concept

**Opportunity Intelligence**: collect freelance opportunities, normalize their external data, evaluate them against configurable criteria, and expose explainable results.

### Responsibility

Opportunity Intelligence owns opportunity qualification and analysis representation.

### Non-Responsibility

- Platform-specific transport/API behavior
- Proposal generation or submission
- Client negotiation
- Project execution
- Revision handling
- Irreversible business actions outside configured policy

### Committed Decisions

- Start as a modular monolith.
- AI capabilities are replaceable components, not the system's core domain owner.
- External freelance platforms are isolated behind adapters/ports.
- Opportunity evaluation must be explainable.
- External observations and derived analysis are distinct concepts.
- Windows/mobile clients will consume backend capabilities rather than duplicate business logic.

### Assumptions

- Initial development can proceed without committing the domain model to one marketplace.
- Official platform APIs/integrations should be preferred where available and permitted.

### Open Questions

- First marketplace integration.
- Exact opportunity evaluation criteria and configuration model.
- Initial persistence technology.
- Initial API technology.
- Initial UI technology.

## Next Step

Complete the Phase 0 product and architecture documents, then pass the Opportunity Intelligence Design Gate before implementation.
