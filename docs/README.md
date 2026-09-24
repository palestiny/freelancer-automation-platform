# Documentation Map

This directory is the engineering source of truth for product direction, architecture, decisions, design gates, and current implementation state.

## Start Here

1. ../README.md — product overview and architecture boundary.
2. ../KHALED_ENGINEERING_WORKING_RULES.md — engineering collaboration contract.
3. PROJECT_STATE.md — canonical current state.
4. PRODUCT_VISION.md — product direction and lifecycle.
5. DOMAIN_MAP.md — domain responsibilities and boundaries.
6. ROADMAP.md — authoritative delivery roadmap.
7. ARCHITECTURE.md — architectural direction and runtime boundaries.
8. DECISION_LOG.md — canonical committed decision register.

## Source-of-Truth Rules

- PROJECT_STATE.md contains one current-state summary; it is not a chronological implementation log.
- ROADMAP.md contains one authoritative status for each phase and the current cross-phase pipeline.
- DECISION_LOG.md contains committed decisions only. Each decision identifier is unique.
- Design Gates define approved or proposed boundaries. A PROPOSED gate is not an implementation authorization.
- Historical implementation detail belongs in the relevant Design Gate and Decision Log, not repeated in the current-state documents.
- New implementation must start from a concrete unresolved requirement and the applicable Design Gate.
- Economic scoring formulas, thresholds, baselines, and portfolio posture rules remain changeable policy unless explicitly committed.
- Meaningful increments require applicable TDD, hardening, documentation reconciliation, CI verification, and merge.

## Current Product / Domain Gates

- Opportunity Intelligence — approved; domain foundation implemented.
- Business Economics & Growth — approved; economics foundation implemented.
- Economic Opportunity OS — approved; broader domain foundations implemented.
- Economic Health & Portfolio Policy — approved; multidimensional Economic Profile foundation implemented.
- Resource Economics & Capacity — approved; resource and human-time capacity foundations implemented.
- Market Intelligence & Demand Discovery — approved; provider-independent observation/demand-signal foundation implemented.
- Venture Validation & Experimentation — approved; provider-independent validation foundation implemented.
- Revenue Engine & Recurring Revenue — approved; revenue contract/event foundation implemented.
- Social Presence & Customer Communication — approved; provider-independent communication foundation implemented.
- Marketing & Growth Automation — approved; campaign foundation implemented.
- Business Operations & Multi-Business Execution — approved; business/operations foundation implemented.
- Campaign Optimization & Budget Policy — approved; bounded recommendation foundation implemented.
- Operational Measurement & Learning — approved; deterministic measurement/learning surface implemented and hardened.
- Phase 17 Statistical Learning & Inference — current V1 statistical-method surface closed; Student's t mean uncertainty and Welch historical mean comparison implemented and hardened.
- Statistical Evidence Composition — approved; downstream statistical evidence consumer implemented.
- Performance Evidence Decision Support — approved; descriptive/inferential composition implemented and hardened.
- Evidence Handoff / Policy Review / Authorization — approved boundaries implemented as separate non-executing stages.
- Execution Runtime / Recovery / Retry — bounded single-worker runtime foundations implemented; distributed/background infrastructure remains outside the current boundary.

## Canonical Performance Evidence Flow

Performance History → Baseline/Comparison Eligibility → Descriptive Trend + Statistical Evidence → Evidence Composition → Evidence Handoff → Policy Review → Authorization → Execution Preparation → Provider Execution → Outcome / Recovery Evidence

The stages remain semantically separate. Statistical evidence does not become a universal score or automatic decision.

## Explicit Decision Records

DESIGN_GATE_EXPLICIT_EVIDENCE_DECISION_RECORDS.md is the canonical V1 design gate for recording explicit human/authorized decisions against evidence. The retired singular duplicate gate has been removed.

## Historical Gates

Historical Design Gates remain available when they document an implemented decision or its rationale. Their presence does not imply that the capability is still the active next boundary.

In particular, DESIGN_GATE_PHASE_17_NEXT_STATISTICAL_USE_CASE.md documents the already-implemented Welch use case; it is historical evidence of the design decision, not authorization to add another statistical method.

## Current Engineering Boundary

The current product remains a modular monolith. Domain semantics stay independent from HTTP, UI, concrete marketplace/provider SDKs, AI providers, payment execution, and financial capital movement.

The implemented runtime extends beyond pure domain objects through explicit application ports, provider-independent execution contracts, bounded retry persistence/scheduling, single-worker dispatch, outcome observation, recovery coordination, and safety checks. Distributed workers, queue infrastructure, production daemonization, unrestricted automatic re-execution, payment execution, and automatic capital movement remain outside the committed boundary.
