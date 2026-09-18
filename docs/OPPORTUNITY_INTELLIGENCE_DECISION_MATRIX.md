# Opportunity Intelligence Decision Matrix

## Status

**PARTIALLY RESOLVED — V1 evaluation dimensions and core outcomes are committed. Remaining product/architecture questions stay open.**

## Decision 1 — First Evaluation Dimensions

**Decision: COMMITTED**

V1 uses:

1. Eligibility
2. Requirement Fit
3. Estimated Effort
4. Economic Fit
5. Client / Project Risk
6. Success Confidence

## Decision 2 — Hard Eligibility vs Soft Evaluation

**Decision: COMMITTED**

Hard eligibility is distinguished from softer derived assessments.

Hard constraints can fail qualification directly. Uncertain softer criteria can produce review rather than inventing certainty.

## Decision 3 — Overall Qualification Outcomes

**Decision: COMMITTED**

- QUALIFIED
- NOT_QUALIFIED
- REVIEW_REQUIRED

## Decision 4 — Numeric Scoring

**Decision: DEFERRED**

Numeric scoring is not required for the first domain slice.

A later ranking model must be introduced as explicit derived behavior with defensible weighting and evidence.

## Decision 5 — Version-One Policy Constraints

**Decision: PARTIALLY COMMITTED**

The domain supports policy-driven constraints for:

- project type
- capabilities/skills
- budget
- client/location constraints
- project size where applicable

Exact user-facing configuration and persistence remain open.

## Decision 6 — First Marketplace

**Decision: OPEN**

Select the first marketplace later based on product priorities, permitted integration mechanisms, data quality, and evidence.

## Decision 7 — Opportunity Identity

**Decision: OPEN**

The opportunity boundary keeps source/platform identity and provenance separate from external observations.

The detailed rules for identifier changes, republishing, duplicates, and cross-platform similarity remain open.

## Decision 8 — Client Representation

**Decision: OPEN**

Whether Client becomes a separate domain entity in the first persisted slice remains open.

## Decision 9 — Technology Selection

**Decision: DEFERRED**

Persistence, API, and UI technology should be selected at the appropriate architecture gate rather than driving the current domain model.
