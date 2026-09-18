# Project State

## Current Phase

**Phase 0 — Product & Architecture — Gate Approved; entering Domain TDD**

## Completed

- Repository created and verified through GitHub integration.
- Initial README committed.
- Shared engineering working rules established.
- Product direction established: a controlled autonomous freelancer lifecycle platform.
- Opportunity Intelligence Design Gate drafted.
- Proposed Opportunity Evaluation Policy documented without converting open product decisions into commitments.

## Approved Design Gate

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
- The platform is marketplace-independent and supports multiple marketplaces.
- Marketplace selection is runtime configuration; no single marketplace is a core architectural dependency.
- Marketplace integrations are replaceable, independently evolvable capabilities.
- Integration improvement may use measured reports, user feedback, comments, AI-assisted recommendations, and user input without turning recommendations into automatic decisions.

### Committed Opportunity Evaluation Policy

The first domain slice uses:
- Eligibility
- Requirement Fit
- Estimated Effort
- Economic Fit
- Client/Project Risk
- Success Confidence
- criterion-level evidence and uncertainty
- QUALIFIED / NOT_QUALIFIED / REVIEW_REQUIRED
- no required numeric score in the first slice
- configurable V1 constraints for project type, capabilities/skills, budget, client/location, and project size where applicable

See docs/PROPOSED_OPPORTUNITY_EVALUATION_POLICY.md and docs/PROPOSED_OPPORTUNITY_INTELLIGENCE_GATE_RESOLUTION.md.

### Assumptions

- Initial development can proceed without committing the domain model to one marketplace.
- Official platform APIs/integrations should be preferred where available and permitted.
- An opportunity may be evaluated more than once as data or policy changes.
- Evaluation evidence should remain inspectable after evaluation.

### Open Questions

- Which marketplace integration should be implemented first.
- Marketplace-specific API/data constraints.
- Whether/when advanced numeric ranking should be introduced.
- Initial persistence technology.
- Initial API technology.
- Initial UI technology.
- Opportunity identity when a marketplace changes/reuses identifiers.
- Whether Client should be a separate domain entity in the first slice.
- Initial persistence technology.
- Initial API technology.
- Initial UI technology.

## Next Step

Begin the first domain TDD cycle for Opportunity Intelligence.

Start with the approved behavior only:
RED → GREEN → REFACTOR → REVIEW → DOCUMENT → COMMIT + PUSH.

Do not introduce a marketplace SDK, persistence, HTTP/API, UI, or AI dependency into the first domain tests.

## Current Boundary

The Opportunity Intelligence design gate is closed.

The current implementation boundary is the domain model and domain behavior only. Marketplace adapters, persistence, API, UI, and AI integrations remain outside the first TDD slice until their own design gates/decisions are reached.
