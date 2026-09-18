# Decision Log

## D-001 — Modular Monolith

**Status:** COMMITTED

**Decision:** Start the platform as a modular monolith.

**Reason:** The product is at an early domain-discovery stage. A modular monolith gives clear boundaries without premature distributed-system complexity.

**Consequence:** Module boundaries must be designed deliberately so later extraction remains possible where justified.

## D-002 — AI Is Replaceable

**Status:** COMMITTED

**Decision:** AI models/providers are capabilities used by the platform, not the owner of business architecture.

**Reason:** The product must remain operable and evolvable as models, tools, and providers change.

## D-003 — Explainable Opportunity Evaluation

**Status:** COMMITTED

**Decision:** Opportunity qualification must retain reasons/evidence behind its derived result.

**Reason:** Automated business decisions need auditability and later analysis.

## D-004 — External Observation vs Analysis

**Status:** COMMITTED

**Decision:** Provider-supplied facts, normalized data, quality assessment, derived analysis, and business decisions are separate concepts.

**Reason:** A suspicious provider value should not silently become a business-domain truth.

## Open Decisions

- First marketplace adapter.
- Evaluation criteria and policy configuration.
- Initial persistence technology.
- Initial API technology.
- Initial UI technology.
