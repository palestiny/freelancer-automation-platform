# TDD — Marketplace Observation Normalization

## Status

**GREEN — HARDENED CANDIDATE**

This slice converts the existing provider-neutral ExternalOpportunityObservation into the existing domain Opportunity contract.

## Boundary

Input:
- provider key
- external opportunity id
- observation timestamp
- title
- description

Output:
- Opportunity
- provider identity preserved as source_platform
- external identity preserved as source_opportunity_id
- title/description preserved without rewriting
- OpportunityType.FREELANCE because this adapter represents marketplace freelance opportunities

## Data Integrity Rule

The normalizer must not invent missing required domain content.

If title or description is unavailable, normalization fails with ValueError rather than silently creating an incomplete domain Opportunity.

Provider fields not present in the observation are intentionally left outside this slice. In particular, project type, required capabilities, and budget are not inferred.

## RED / GREEN

- RED: contract test defined for successful normalization and missing required content.
- GREEN: implementation maps only verified fields and rejects missing required content.
- HARDENING: no provider SDK imports or provider-specific types are introduced into the domain.

## Non-goals

- Provider ranking
- opportunity scoring
- six-dimensional evaluation expansion
- budget/capability inference
- AI extraction
- persistence/API/UI
- proposal/bid execution
- production marketplace access

## Completion

The slice is complete when CI passes, the PR is merged, and the current-state documentation remains reconciled.
