# Design Gate — Economic Health, Stability & Portfolio Posture

## Status

**APPROVED — V1 domain direction**

This gate records the decision that profitability, profit potential, profit stability, demand stability, safety, and related economic qualities are first-class measurable concepts.

The model is intentionally designed for change. Scoring policies may evolve without changing the identity of the underlying business or opportunity.

## Problem

Optimizing only for maximum theoretical profit can destroy economically valuable assets.

Examples include:
- a small but consistently profitable service;
- a stable recurring-revenue product;
- a low-risk, highly automated business with modest upside;
- a reliable cash-generating operation that funds experiments elsewhere.

The platform therefore needs to distinguish **current economic health** from **growth attractiveness**.

## V1 Economic Profile

The platform will represent an economic profile as a vector of bounded scores (0–100), rather than one opaque master score.

V1 dimensions:

1. Profitability
2. Profit Potential
3. Profit Stability
4. Demand Stability
5. Safety
6. Recurring Revenue
7. Automation
8. Capital Efficiency
9. Scalability
10. Evidence Quality

A higher score means more favorable characteristics for that dimension.

**Human dependency is not included as a positive-score dimension in V1.** It remains a measurable operating metric and can later become a policy-specific score without changing the profile contract.

## Why No Universal Master Score?

Different decisions require different objectives.

A growth decision may emphasize potential and scalability.
A protection decision may emphasize profitability, stability, demand stability, and safety.
A validation decision may emphasize evidence quality and time/capital efficiency.

Collapsing these dimensions into one permanent number would hide trade-offs and make policy changes harder to explain.

## Derived vs Observed

Scores are derived assessments, not raw facts.

The system must preserve the evidence and/or metrics from which a score was produced.

Examples:
- Profitability may use actual margin, profit per hour, or risk-adjusted profit.
- Profit Stability may use historical profit variance and downside behavior.
- Demand Stability may use demand history, retention, repeat purchases, or recurring contracts.
- Safety may use downside exposure, dependency concentration, operational failure modes, and policy constraints.
- Evidence Quality measures how well supported the assessment is; it is not a measure of business quality itself.

The exact scoring formulas remain policy decisions and may differ by opportunity/business type.

## Economic Asset Protection

The platform must be able to represent a stable profitable business as an asset worth protecting.

A future portfolio policy may classify economic assets into postures such as:

- PROTECT
- MAINTAIN
- OPTIMIZE_CAREFULLY
- GROW
- HARVEST
- TURNAROUND
- EXIT

These are **policy-derived actions**, not intrinsic properties of the business and not part of the V1 score vector.

## Safety

Safety is a first-class economic dimension.

The platform must not treat higher expected profit as sufficient justification for higher risk.

Safety assessments must remain evidence-backed, policy-aware, auditable, and compatible with progressive autonomy.

Financial execution remains outside the current implementation boundary.

## Stability

Stability is not the same as profitability.

The platform should be able to distinguish:
- high profit / unstable;
- modest profit / highly stable;
- high potential / weak evidence;
- low profit / strategically useful;
- recurring revenue / low growth.

This distinction is required for future portfolio and capital-allocation decisions.

## Changeability

The following remain intentionally configurable/future-policy concerns:
- scoring formulas;
- dimension weights, if weights are introduced;
- thresholds;
- required evidence;
- time windows;
- comparison baselines;
- portfolio posture rules.

Changing these policies must not require rewriting Opportunity identity or Business Model identity.

## Current Boundary

This gate introduces the domain contract for the economic profile and documents the future portfolio posture concept.

It does **not** implement:
- automatic capital allocation;
- automatic financial execution;
- a universal optimization objective;
- final scoring formulas for every business type;
- portfolio rebalancing;
- AI-owned economic decisions.

## Follow-up

Next work can extend the profile with:
- historical metric snapshots;
- resource/capacity economics;
- scoring policies by opportunity type;
- portfolio posture rules;
- actual-vs-expected learning;
- evidence provenance.

## Decision Gate Result

**APPROVED**

The platform may proceed with a changeable, evidence-aware economic profile while keeping scoring policy separate from core domain identity.
