# Project State

## Current Phase

**Phase 0 — Product & Architecture**

## Completed

- Repository created and verified through GitHub integration.
- Initial README committed.
- Shared engineering working rules established.
- Product direction established: a controlled autonomous freelancer lifecycle platform.
- Opportunity Intelligence Design Gate drafted.
- Proposed Opportunity Evaluation Policy documented without converting open product decisions into commitments.

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

### Proposed — Not Yet Committed

The current evaluation-policy proposal defines:
- Eligibility
- Requirement Fit
- Estimated Effort
- Economic Fit
- Client/Project Risk
- Success Confidence
- Criterion-level evidence and uncertainty
- Categorical outcomes before introducing numeric scoring

See docs/PROPOSED_OPPORTUNITY_EVALUATION_POLICY.md.

### Assumptions

- Initial development can proceed without committing the domain model to one marketplace.
- Official platform APIs/integrations should be preferred where available and permitted.
- An opportunity may be evaluated more than once as data or policy changes.
- Evaluation evidence should remain inspectable after evaluation.

### Open Questions

- Whether the six proposed evaluation dimensions are the correct first-version scope.
- Whether hard eligibility should be separated from softer qualification criteria.
- Whether the proposed overall outcomes are sufficient.
- Whether numeric scoring should remain outside the first vertical slice.
- Which policy constraints are mandatory in version one.
- First marketplace integration.
- Opportunity identity when a marketplace changes/reuses identifiers.
- Whether Client should be a separate domain entity in the first slice.
- Initial persistence technology.
- Initial API technology.
- Initial UI technology.

## Next Step

Do not begin implementation yet.

First complete the Opportunity Intelligence Design Gate by resolving the product-owner decisions above. Once the evaluation behavior is approved, create the first domain TDD tests and proceed through RED → GREEN → REFACTOR.

## Current Boundary

The project is intentionally stopped at the design gate. No marketplace integration, persistence implementation, API implementation, UI implementation, or AI integration should be introduced as part of this gate until the relevant design decisions are made.
