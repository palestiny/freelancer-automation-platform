# Opportunity Intelligence Decision Matrix

## Status

**DECISION INPUT — product-owner decisions remain open.**

This document turns the current Opportunity Intelligence open questions into explicit decision points so the Design Gate can be closed without mixing proposals with commitments.

## Decision 1 — First Evaluation Dimensions

### Current proposal

1. Eligibility
2. Requirement Fit
3. Estimated Effort
4. Economic Fit
5. Client / Project Risk
6. Success Confidence

### Alternative

Start with fewer dimensions and add the rest after the first real evaluation workflow is validated.

### Trade-off

More dimensions provide broader qualification earlier, but increase domain complexity and require more evidence/modeling.

### Decision required

Confirm the first-version dimensions, or specify which dimensions should be removed/deferred.

---

## Decision 2 — Hard Eligibility vs Soft Evaluation

### Current proposal

Separate hard eligibility from softer criteria.

Hard constraints can fail qualification directly. Other criteria contribute evidence and may result in review rather than automatic rejection.

### Alternative

Treat all criteria uniformly.

### Trade-off

Separation makes explicit user constraints easier to reason about, while a uniform model is simpler but can blur the difference between a mandatory constraint and an uncertain assessment.

### Decision required

Choose whether hard eligibility is a distinct evaluation stage.

---

## Decision 3 — Overall Qualification Outcomes

### Current proposal

- QUALIFIED
- NOT_QUALIFIED
- REVIEW_REQUIRED

### Trade-off

Three outcomes explicitly represent uncertainty. A binary result is simpler but requires uncertainty to be represented elsewhere.

### Decision required

Confirm these outcomes or define the desired set.

---

## Decision 4 — Numeric Scoring

### Current proposal

Do not require a numeric score in the first vertical slice.

### Alternative

Introduce a score immediately.

### Trade-off

A score enables ranking, but requires defensible weighting and can create false precision before evaluation behavior is validated.

### Decision required

Confirm whether numeric scoring is deferred.

---

## Decision 5 — Version-One Policy Constraints

The policy proposal can support:
- project type
- skills/capabilities
- budget
- client/location constraints
- project size
- economic thresholds
- risk tolerance

### Decision required

Identify which constraints are mandatory for version one.

---

## Decision 6 — First Marketplace

### Decision required

Select the first marketplace integration.

### Constraint

The integration should use an official/permitted API or integration mechanism where available. Marketplace-specific behavior must remain behind the adapter boundary.

---

## Decision 7 — Opportunity Identity

### Current proposal

Keep source/platform identity and provenance as part of the opportunity boundary, while treating external observations as separate input records.

### Open case

A marketplace may change identifiers, republish a listing, or expose inconsistent identifiers.

### Decision required

Define the identity rule for:
- source identifier changes
- republished opportunities
- duplicate observations
- cross-platform similar opportunities

---

## Decision 8 — Client Representation

### Current options

**Option A — Client reference only**
- Keep a client reference/value in the first vertical slice.
- Introduce a full Client domain entity later.

**Option B — Client entity now**
- Model Client as a separate domain concept from the beginning.

### Trade-off

Reference-only keeps the first slice smaller. A full entity supports richer client history and later reputation/risk analysis but expands the current domain surface.

### Decision required

Choose the first-slice representation.

---

## Decision 9 — Technology Selection

Persistence, API, and UI technology remain intentionally open.

They should be selected after the domain behavior is stable enough to avoid letting framework choices drive the domain model.

### Decision required

Technology choices can be made as a separate architecture gate after the domain gate, unless a technical constraint requires an earlier decision.

---

## Gate-Close Checklist

The Opportunity Intelligence Design Gate can close when:

- [ ] First evaluation dimensions are approved.
- [ ] Hard vs soft evaluation behavior is decided.
- [ ] Overall outcomes are approved.
- [ ] Numeric scoring decision is made.
- [ ] Version-one policy constraints are defined.
- [ ] First marketplace is selected.
- [ ] Opportunity identity rule is defined sufficiently for the first slice.
- [ ] Client representation is decided.
- [ ] Persistence/API/UI choices are either explicitly deferred or decided at the appropriate architecture gate.

After closure:

**Design → RED test → GREEN implementation → REFACTOR → Review → Documentation → Commit/Push**
