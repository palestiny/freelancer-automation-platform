# Opportunity Intelligence Design Gate

## Status

**APPROVED — V1 domain direction committed; domain TDD in progress.**

## Concept

Opportunity Intelligence answers:

> What freelance opportunities are available, what do we reliably know about each one, and how suitable is each opportunity according to the user's configured policy?

It is an analysis capability over opportunities, not the full freelancer lifecycle.

## Core Concepts

### Opportunity

Represents a freelance work opportunity after normalization.

It contains business-relevant information such as:

- stable identity within its source/platform
- title
- description/requirements
- source/platform identity
- client reference when available
- budget/pricing information when available
- timestamps when available
- required capabilities
- source URL
- normalized metadata needed for qualification

Opportunity does not contain proposal, execution, communication, revision, AI-provider, or evaluation-result state.

### External Opportunity Observation

Represents data received from a marketplace integration.

Provider data remains an observation until normalized and assessed.

### Normalized Opportunity

Represents the platform's normalized interpretation of an external observation while preserving provenance.

### Opportunity Evaluation

Represents a derived assessment against an Evaluation Policy.

It preserves:

- evaluated criteria
- criterion outcomes
- evidence
- uncertainty
- overall qualification outcome

### Evaluation Policy

Represents configurable rules used to evaluate opportunities.

The policy remains independent from a particular marketplace.

## Committed V1 Evaluation Dimensions

1. Eligibility
2. Requirement Fit
3. Estimated Effort
4. Economic Fit
5. Client / Project Risk
6. Success Confidence

These dimensions are the first evaluation model. They can evolve through explicit decisions and versioning.

## Committed Overall Outcomes

- QUALIFIED
- NOT_QUALIFIED
- REVIEW_REQUIRED

Criterion outcomes include:

- PASS
- FAIL
- INSUFFICIENT_DATA
- NOT_APPLICABLE

## Economic Boundary

Economic Fit is one of the six Opportunity Intelligence dimensions.

Reusable economic calculations belong to the separate Business Economics domain so they can later support pricing, resource planning, portfolio allocation, and actual-vs-expected measurement.

## Responsibility

### Opportunity module

Owns business identity and normalized opportunity representation.

### Opportunity Intelligence module

Owns evaluation policy, evaluation process, evidence, and qualification result.

### Business Economics module

Owns reusable economic calculations and derived economic estimates.

### Platform Adapter

Owns provider-specific communication, authentication, transport, mapping, and submission mechanics.

It does not decide whether an opportunity is good for the user.

## Boundary

External Platform
→ Platform Adapter
→ External Opportunity Observation
→ Normalization
→ Opportunity
→ Evaluation Policy + Evaluation
→ Economic Assessment
→ later Decision/Planning

The evaluator must not depend on marketplace SDKs or HTTP clients.

## External Facts vs Derived Meaning

External fact:
- marketplace reports budget = $500

Normalized fact:
- budget represented as USD 500 with provenance

Data-quality assessment:
- budget is missing / ambiguous / inconsistent / valid

Derived assessment:
- economic and effort calculations

Business decision:
- qualification or later pursuit decision according to explicit policy

These stages remain distinguishable.

## Alternatives Rejected for V1

### Evaluation inside Opportunity

Rejected because it mixes immutable opportunity identity with policy-driven derived analysis.

### Generic AI Agent as domain owner

Rejected because business rules, integrations, reasoning, and execution become coupled.

## Open Decisions

- First marketplace.
- Persistence/API/UI technology.
- Opportunity identity behavior for source identifier changes and republishing.
- Client representation.
- Advanced numeric ranking.

These remain separate from the committed V1 evaluation dimensions.
