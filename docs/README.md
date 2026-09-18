# Documentation Map

This directory is the engineering source of truth for product direction, architecture, decisions, domain design, and current implementation state.

## Start Here

1. ../README.md — project overview.
2. ../KHALED_ENGINEERING_WORKING_RULES.md — engineering collaboration contract.
3. PROJECT_STATE.md — current phase and active implementation boundary.
4. PRODUCT_VISION.md — product goal and lifecycle.
5. DOMAIN_MAP.md — domain responsibilities and boundaries.
6. ROADMAP.md — phased delivery roadmap.
7. ARCHITECTURE.md — architectural direction.
8. DECISION_LOG.md — committed architectural/product decisions.
9. DESIGN_GATE_OPPORTUNITY_INTELLIGENCE.md — Opportunity Intelligence gate.
10. DESIGN_GATE_BUSINESS_ECONOMICS_AND_GROWTH.md — economics/growth gate.
11. DESIGN_GATE_ECONOMIC_OPPORTUNITY_OS.md — broader Economic Opportunity OS expansion gate.
12. PROPOSED_OPPORTUNITY_EVALUATION_POLICY.md — committed V1 evaluation behavior.
13. OPPORTUNITY_INTELLIGENCE_DECISION_MATRIX.md — Opportunity Intelligence decisions.
14. TDD_OPPORTUNITY_INTELLIGENCE_PLAN.md — active Opportunity Intelligence TDD sequence.

## Source-of-Truth Rules

- PROJECT_STATE.md describes where the project currently is.
- DECISION_LOG.md contains committed decisions only.
- Design Gate documents define approved boundaries and implementation intent.
- Documents explicitly marked PROPOSED remain proposals unless a decision is recorded in DECISION_LOG.md.
- Open questions remain visible until resolved.
- Implementation must follow the active Design Gate rather than silently redefining it.
- After meaningful implementation, update project state and decision documentation as appropriate.

## Current Gates

- Opportunity Intelligence: approved; domain TDD continues.
- Business Economics & Growth: approved; economic estimate foundation implemented.
- Economic Opportunity OS expansion: approved; domain foundations implemented.
- Resource Economics / Capacity: next.
- Market Intelligence / Demand Discovery: future.
- Venture Validation / Experimentation: future.
- Portfolio / Capital Allocation: future.
- Revenue Engine / Recurring Revenue: future.

## Current Implementation Rule

Do not introduce marketplace SDKs, persistence, HTTP/API, UI, AI-provider dependencies, financial execution, or automatic capital movement into the current domain-only slices.
