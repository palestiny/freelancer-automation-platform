# Proposed Opportunity Intelligence Gate Resolution

## Status

**PROPOSAL ONLY — NOT COMMITTED**

This document is a concrete default proposal intended to make the first implementation gate actionable. It does not change the committed architecture or product decisions.

## Proposed Resolution

### 1. Evaluation Dimensions

Use these six dimensions initially:
- Eligibility
- Requirement Fit
- Estimated Effort
- Economic Fit
- Client / Project Risk
- Success Confidence

Reason: together they cover the minimum decision questions needed to determine whether an opportunity is worth pursuing without yet modeling proposal, execution, or communication behavior.

### 2. Hard vs Soft Evaluation

Use two categories:

**Hard constraints**
- explicit user requirements that must be satisfied
- failure produces NOT_QUALIFIED

**Soft / assessable criteria**
- evaluated independently
- uncertainty does not automatically mean rejection
- unresolved important uncertainty can produce REVIEW_REQUIRED

This keeps policy constraints distinct from estimates and interpretations.

### 3. Overall Outcomes

Use:
- QUALIFIED
- NOT_QUALIFIED
- REVIEW_REQUIRED

These are business outcomes of the evaluation, not properties of Opportunity identity.

### 4. Numeric Scoring

Defer numeric scoring from the first domain slice.

First validate criterion behavior, evidence, uncertainty, and qualification semantics. Ranking can later introduce a separate derived score.

### 5. Version-One Policy

Initial policy should support only constraints needed by the first marketplace/use case:
- allowed project type
- required capabilities/skills
- minimum and maximum budget where applicable
- client/location constraint where applicable
- project-size constraint where available

Economic thresholds and risk tolerance should be represented only if the first real workflow needs them.

### 6. First Marketplace

**OPEN — product-owner selection required.**

No marketplace-specific domain implementation should begin until this is selected.

### 7. Opportunity Identity

For the first slice, identity should be based on:

**source/platform + source opportunity identifier**

The observation retains the external identifier and provenance. Duplicate/republication handling should be treated as a separate policy once real marketplace behavior is known.

### 8. Client Representation

Use a client reference/value in the first vertical slice rather than introducing a full Client aggregate.

A full Client domain model can be introduced when client history, communication, reputation, or analytics require it.

### 9. Technology

Keep persistence/API/UI technology explicitly deferred until the domain behavior is approved.

The first implementation should be domain-first and testable without infrastructure.

## Remaining Product-Owner Decisions

Only these decisions still require explicit approval before the proposal becomes committed:

1. Approve the six initial evaluation dimensions.
2. Approve hard-vs-soft evaluation.
3. Approve the three overall outcomes.
4. Approve deferring numeric scoring.
5. Confirm the minimum version-one policy constraints.
6. Select the first marketplace.

Everything else above is intentionally a proposed default, not a committed architectural decision.

## After Approval

**RED → GREEN → REFACTOR → REVIEW → DOCUMENT → COMMIT + PUSH**
