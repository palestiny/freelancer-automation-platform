# Decision Log

## D-001 — Modular Monolith

**Status:** COMMITTED

Start the platform as a modular monolith.

## D-002 — AI Is Replaceable

**Status:** COMMITTED

AI models/providers are capabilities used by the platform, not owners of business architecture.

## D-003 — Explainable Opportunity Evaluation

**Status:** COMMITTED

Opportunity qualification must retain reasons/evidence behind derived results.

## D-004 — External Observation vs Analysis

**Status:** COMMITTED

Provider-supplied facts, normalized data, quality assessment, derived analysis, and business decisions remain separate concepts.

## D-005 — Marketplace-Independent Multi-Marketplace Strategy

**Status:** COMMITTED

The platform supports multiple freelance marketplaces through replaceable adapters.

## D-006 — Marketplace Integrations Are Independently Evolvable Capabilities

**Status:** COMMITTED

Each marketplace integration has its own compatibility, quality, operational, and business-value evidence.

## D-007 — Marketplace Choice Is Runtime Configuration

**Status:** COMMITTED

Marketplace enablement belongs to configuration/policy, not core Opportunity identity.

## D-008 — Business Automation OS Direction

**Status:** COMMITTED

The platform's long-term product boundary is Business Automation OS. Freelancing is the first market used to validate the platform.

## D-009 — Profitability Is a First-Class Domain Concern

**Status:** COMMITTED

Expected revenue, expected cost, expected profit, margin, profit per hour, and risk-adjusted economics are part of business-domain reasoning.

## D-010 — Resource Economics

**Status:** COMMITTED

The platform will treat constrained resources such as human time, AI/tool usage, infrastructure, review effort, communication effort, and marketplace fees as economic inputs.

## D-011 — Expected vs Actual Measurement Loop

**Status:** COMMITTED

The platform will preserve the distinction between estimates and actual outcomes and use variance as a learning signal.

**Flow:** Expected → Actual → Variance → Learning Signal.

## D-012 — Learning Does Not Silently Rewrite Policy

**Status:** COMMITTED

Learning and AI-assisted analysis can produce recommendations, but policy changes require an explicit decision and versioned change.

## D-013 — Controlled Experimentation

**Status:** COMMITTED

The platform will support measurable experiments for policies, pricing, proposals, capability selection, and execution strategies.

## D-014 — Progressive Autonomy

**Status:** COMMITTED

Automation capability will be represented through explicit autonomy levels from observation through controlled optimization.

## D-015 — Economic Estimate as Derived Domain Data

**Status:** COMMITTED

Economic estimates are separate derived data and do not mutate Opportunity identity.

## D-016 — Economic Opportunity OS

**Status:** COMMITTED

The long-term product expands from a freelancer automation system into an Economic Opportunity OS / Business Automation OS capable of discovering and evaluating multiple business and income opportunities.

Freelancing remains the first laboratory, not the permanent architectural boundary.

## D-017 — Opportunity Types Are Explicit

**Status:** COMMITTED

The domain recognizes multiple opportunity types: freelance, service, product, SaaS, game, digital asset, recurring revenue, partnership, investment, and acquisition.

Different opportunity types may require different evaluation models.

## D-018 — Business Model Discovery

**Status:** COMMITTED

Demand may be converted into multiple business-model hypotheses rather than assuming one implementation path.

## D-019 — Separate Venture Evaluation

**Status:** COMMITTED

Broader ventures use a dedicated evaluation model instead of forcing SaaS, games, services, investments, and acquisitions into the six-dimensional Opportunity Intelligence model.

## D-020 — Evidence Taxonomy

**Status:** COMMITTED

The domain distinguishes FACT, OBSERVATION, ESTIMATE, ASSUMPTION, HYPOTHESIS, FORECAST, and EXPERIMENT_RESULT.

## D-021 — Low-Touch Recurring Revenue

**Status:** COMMITTED

The system should explicitly identify recurring-revenue and high-automation opportunities. "Passive income" is represented as low-touch recurring economics rather than assumed literal passivity.

## D-022 — Investment Execution Boundary

**Status:** COMMITTED

Investment opportunities are initially research and decision-support concerns. Automatic financial execution requires a separate explicit policy and approval design.

## D-023 — Capital Allocation Is a Future Gate

**Status:** COMMITTED

Future capital allocation will consider return, risk, liquidity, capital requirement, time to revenue, recurring revenue, automation, human dependency, scalability, strategic fit, evidence quality, exit/expansion potential, and opportunity cost.

Automatic capital movement is not part of the current domain implementation.

## D-024 — Business Model Pattern Mining, Not Literal Copying

**Status:** COMMITTED

The system may study successful business/game patterns and derive differentiated hypotheses, but it is not designed around literal copying of another product.

## D-025 — Economic Quality Is Multi-Dimensional

**Status:** COMMITTED

Profitability, profit potential, profit stability, demand stability, safety, recurring revenue, automation, capital efficiency, scalability, and evidence quality are separate measurable economic dimensions.

The platform must not assume that maximum theoretical profit is the only objective.

## D-026 — Stable Profitability Must Be Protectable

**Status:** COMMITTED

A small, stable, profitable business or recurring-revenue asset is economically valuable even when growth upside is limited. Future portfolio policy must be able to protect and monitor such assets rather than sacrificing them automatically for higher theoretical upside.

## D-027 — No Universal Economic Master Score

**Status:** COMMITTED

Economic dimensions remain a vector rather than one permanent weighted score. Different policies may emphasize different dimensions for protection, maintenance, controlled optimization, growth, harvesting, turnaround, or exit decisions.

## D-028 — Economic Scores Are Derived and Evidence-Aware

**Status:** COMMITTED

Economic scores are derived assessments, not raw facts. The system must preserve supporting evidence/metrics and their quality. Scoring formulas, thresholds, baselines, and time windows remain changeable policy.

## D-029 — Portfolio Posture Is Policy-Derived

**Status:** COMMITTED

PROTECT, MAINTAIN, OPTIMIZE_CAREFULLY, GROW, HARVEST, TURNAROUND, and EXIT are future policy-derived actions, not intrinsic business states and not part of the core Economic Profile score vector.

## D-030 — Resource Usage Is Explicit

**Status:** COMMITTED

A resource consumption record explicitly identifies its resource kind, quantity, and monetary unit cost. Total resource cost is derived as quantity × unit cost.

## D-031 — Resource Kinds Are Explicit

**Status:** COMMITTED

V1 recognizes HUMAN_TIME, CAPABILITY_USAGE, INFRASTRUCTURE, COMMUNICATION, MARKETPLACE_FEE, and REVIEW_TIME as controlled resource categories.

## D-032 — Human Time Is the First Capacity Model

**Status:** COMMITTED

V1 capacity is modeled as human-time hours for a defined period, distinguishing total, committed, reserved, remaining capacity, and utilization.

## D-033 — Capacity Is Not Profit

**Status:** COMMITTED

Capacity availability is an operational constraint, not an economic-quality score. Business Economics may consume capacity information, while Economic Health remains a separate derived assessment.

## Open Decisions

- How capacity periods are generated from actual availability.
- Whether capacity should support multiple currencies.
- How resource costs are normalized across currencies.
- How actual resource usage is captured.
- How capacity reservations interact with execution lifecycle.
- How opportunity cost is calculated from scarce capacity.
- How capacity feeds future portfolio posture policies.
- Economic score calculation policies and evidence requirements by opportunity/business type.
- Historical stability metric windows and baselines.
- Market Intelligence and demand-source boundaries.
- Venture validation experiment model.
- Portfolio posture rules and optimization constraints.
- Capital allocation policy and approval controls.
- Exact experiment statistics/decision methodology.
- First marketplace adapter.
- Initial persistence technology.
- Initial API technology.
- Initial UI technology.


## D-034 — Existing Markets Are Valid Opportunities

**Status:** COMMITTED

An existing competitive market is not automatically rejected.

A Service, Game, SaaS, Product, Digital Asset, or other business can be a valid opportunity when its thesis is economically credible, evidence-backed, and testable. Competition is an evaluation input rather than a hard rejection condition.

## D-035 — Marketing & Growth Are First-Class Capabilities

**Status:** COMMITTED

After validation/build, the platform must be able to operate a measurable growth loop including positioning, campaigns, content/distribution, lead acquisition, customer feedback, measurement, and learning.

Marketing is part of the business operating loop rather than a side feature.

## D-036 — Campaigns Are Measurable Experiments

**Status:** COMMITTED

A campaign is represented as a provider-independent business experiment with an explicit objective, channels, lifecycle, budget constraint when applicable, authorization state, and measurable performance observations.

Campaign success is not guaranteed; actual outcomes become evidence for learning.

## D-037 — Marketing Providers Are Replaceable

**Status:** COMMITTED

Advertising networks, social networks, communication providers, content tools, and AI providers are external capabilities/adapters. They must not own core business meaning.

## D-038 — Marketing Automation Has Explicit Safety Boundaries

**Status:** COMMITTED

Real ad spend, account creation, credentials, public publishing, and customer communication are external actions governed by policy and authorization.

Automatic financial spend is not introduced by the marketing domain foundation. High-impact or irreversible actions may require human approval under the existing progressive-autonomy model.