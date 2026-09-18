# Opportunity Intelligence Design Gate

## Status

**DESIGN IN PROGRESS — decisions requiring product-owner confirmation remain open.**

This document defines the proposed domain shape for the first vertical slice. It does not silently convert open questions into committed decisions.

## 1. Concept

Opportunity Intelligence answers:

> "What freelance opportunities are available, what do we reliably know about each one, and how suitable is each opportunity according to the user's configured policy?"

It is an analysis capability over opportunities, not the full freelancer lifecycle.

## 2. Core Concepts

### Opportunity

Represents a freelance work opportunity as the platform understands it after normalization.

It should contain business-relevant information such as:
- stable identity within its source/platform
- title
- description/requirements
- source/platform identity
- client reference when available
- budget/pricing information when available
- published/updated timestamps when available
- required skills
- source URL
- normalized metadata needed for qualification

Opportunity does **not** contain:
- proposal state
- execution state
- communication state
- revision state
- AI provider details
- evaluation result as intrinsic identity

### External Opportunity Observation

Represents data received from a marketplace integration.

Its purpose is to preserve what the external source reported before business interpretation.

It may contain provider-specific fields and raw values.

It should not be treated as the business truth merely because a provider supplied it.

### Normalized Opportunity

Represents the platform's normalized interpretation of an external observation.

Normalization should make equivalent concepts comparable across platforms while preserving provenance.

### Opportunity Evaluation

Represents a derived assessment of an opportunity against an evaluation policy.

It should answer:
- which criteria were evaluated
- what evidence was used
- what result each criterion produced
- what uncertainties/data-quality limitations exist
- the resulting qualification outcome

Evaluation is derived data, not part of the opportunity's immutable identity.

### Evaluation Policy

Represents configurable rules used to evaluate opportunities.

The policy should be independent from a particular marketplace.

The exact criteria and weighting model remain OPEN.

### Evaluation Result

The initial result should be explainable rather than a single unexplained score.

Candidate outcomes:
- QUALIFIED
- NOT_QUALIFIED
- REVIEW_REQUIRED

These names are **PROPOSED**, not yet committed.

## 3. Responsibility

### Opportunity module

Owns the business identity and normalized representation of an opportunity.

### Opportunity Intelligence module

Owns:
- evaluation policy
- evaluation process
- evaluation evidence
- qualification result

### Platform Adapter

Owns:
- communication with an external marketplace
- provider-specific authentication/integration details
- mapping external observations into the platform boundary

It does not decide whether an opportunity is good for the user.

## 4. Boundary

Proposed flow:

External Platform
→ Platform Adapter
→ External Opportunity Observation
→ Normalization
→ Opportunity
→ Evaluation Policy + Evaluation
→ API representation

The external adapter must not directly call evaluation business rules.

The evaluation domain must not depend on marketplace SDKs or HTTP clients.

## 5. External Facts vs Derived Meaning

Example:

**External fact**
- marketplace reports budget = $500

**Normalized fact**
- budget represented as USD 500 with source provenance

**Data-quality assessment**
- budget is missing / ambiguous / inconsistent / valid

**Derived assessment**
- estimated effort may fit configured target range

**Business decision**
- qualification result according to the user's policy

These stages must remain distinguishable.

## 6. Alternatives Considered

### Alternative A — Put evaluation directly inside Opportunity

**Trade-off:** Simple initially, but mixes identity/representation with policy-driven analysis and makes repeated evaluations under different policies harder.

### Alternative B — Separate Opportunity and Evaluation

**Trade-off:** Slightly more domain structure, but keeps derived analysis independent and supports multiple policies/evaluation versions.

**Current proposal:** Alternative B.

### Alternative C — One generic AI Agent owns discovery and evaluation

**Trade-off:** Fast demo path, but couples business rules, external integrations, reasoning, and execution. It conflicts with the committed architecture.

**Decision:** Not selected for this architecture.

## 7. Assumptions

- An opportunity can be evaluated more than once as its data or policy changes.
- External marketplace data can be incomplete or inconsistent.
- Evaluation must preserve enough evidence to explain its result.
- Multiple marketplaces may eventually provide different representations of similar opportunities.

These remain assumptions unless explicitly committed.

## 8. Open Decisions

1. **Evaluation criteria:** Which dimensions are required for the first version?
2. **Scoring:** Should the first version use categorical rule outcomes, numeric scoring, or both?
3. **Policy configuration:** Static application configuration, persisted user policy, or another model?
4. **Opportunity identity:** How should an opportunity be identified when the source changes identifiers or republishes a listing?
5. **Client representation:** Is Client a separate domain entity now, or only a reference in the first slice?
6. **First marketplace:** Which platform should provide the first real adapter?
7. **Persistence/API technology:** These can remain open until the domain behavior is stable.

## 9. Proposed First TDD Behaviors

Before infrastructure, tests should establish domain behavior for:

1. An external observation can be normalized into an opportunity without losing source identity.
2. Missing optional external data does not automatically make an opportunity invalid.
3. Evaluation produces explicit criterion-level evidence.
4. Evaluation does not modify the opportunity's identity.
5. The same opportunity can be evaluated under a different policy.
6. Evaluation can represent uncertainty or insufficient data rather than inventing a fact.

These are proposed behaviors for the first implementation gate.
