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


## D-005 — Marketplace-Independent Multi-Marketplace Strategy

**Status:** COMMITTED

**Decision:** The platform will support multiple freelance marketplaces through replaceable adapters. The user can enable one, several, or none through configuration/dashboard controls.

**Reason:** Marketplace selection is a runtime/product configuration, not a foundation-level architectural dependency. The core domain must remain portable across marketplaces.

**Consequence:** Marketplace-specific behavior belongs behind adapter/integration boundaries. The first marketplace implementation may be selected later based on product priorities and evidence without redesigning the core opportunity domain.

## D-006 — Marketplace Integrations Are Independently Evolvable Capabilities

**Status:** COMMITTED

**Decision:** A marketplace integration is treated as an independently evolvable project/capability with its own compatibility, quality, operational, and performance evidence.

**Reason:** Integrations can differ substantially in APIs, data quality, rate limits, authentication, coverage, reliability, and business value.

**Consequence:** Integration selection and improvement can be informed by reports, metrics, user feedback, comments, AI-assisted recommendations, and user input. Derived recommendations do not automatically become product or architecture decisions.

## D-007 — Marketplace Choice Is Runtime Configuration

**Status:** COMMITTED

**Decision:** Marketplace enablement belongs to configuration/policy, not to the core Opportunity domain identity or architecture.

**Reason:** The system must be able to operate across multiple enabled marketplaces and remain extensible without rebuilding the domain around one provider.
