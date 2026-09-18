# Design Gate — Economic Opportunity OS Expansion

**Status: APPROVED — Product/domain direction committed; implementation remains domain-first**

## Purpose

Expand the Business Automation OS from a freelance-first automation system into a broader **Economic Opportunity OS** capable of discovering, evaluating, validating, operating, and learning from multiple business and income opportunities.

Freelancing remains the first laboratory because it provides a concrete, measurable path from demand to sale to delivery to revenue and actual economics.

It is not the permanent architectural boundary.

## Committed Product Direction

The platform should be able to:

1. study multiple markets;
2. discover demand and unmet needs;
3. turn demand signals into candidate business opportunities;
4. generate and compare multiple business-model hypotheses;
5. evaluate ventures using evidence-aware economics and business criteria;
6. identify the lowest-cost validation experiment;
7. measure expected vs actual outcomes;
8. learn from evidence without silently changing policy;
9. progress validated ventures toward recurring, low-touch revenue where appropriate;
10. manage a portfolio of business opportunities over time.

The long-term loop is:

**Market Signals → Opportunity Discovery → Business Model Discovery → Venture Thesis → Economic Evaluation → Validation → MVP → Revenue → Measurement → Learning → Controlled Experimentation → Scale / Kill → Capital Allocation**

## Opportunity Types

The platform recognizes these opportunity types as distinct domain categories:

- Freelance Opportunity
- Service Opportunity
- Product Opportunity
- SaaS Opportunity
- Game Opportunity
- Digital Asset Opportunity
- Recurring Revenue Opportunity
- Partnership Opportunity
- Investment Opportunity
- Acquisition Opportunity

The six existing Opportunity Intelligence dimensions remain valid for their original opportunity context and are not replaced by this expansion.

## Business Model Discovery

A single demand signal may support several business models.

Examples include:

- freelance service
- productized service
- managed service
- SaaS
- API
- digital product
- game
- white-label
- subscription
- partnership

The platform should represent these as hypotheses that can be evaluated rather than treating the first discovered model as fact.

## Venture Evaluation

Broader ventures use a separate evaluation model rather than forcing every opportunity into the six freelance-oriented dimensions.

V1 venture criteria are:

- Market Demand
- Market Size
- Competition
- Capital Requirement
- Time to Revenue
- Recurring Revenue Potential
- Automation Potential
- Scalability
- Risk
- Evidence Quality
- Strategic Fit
- Exit / Expansion Potential

Evaluation remains explainable and evidence-aware.

No numeric master score is required for the first venture domain slice.

## Evidence Model

The system distinguishes:

- FACT
- OBSERVATION
- ESTIMATE
- ASSUMPTION
- HYPOTHESIS
- FORECAST
- EXPERIMENT_RESULT

Evidence quality must be preserved through the lifecycle.

A forecast or hypothesis must never silently become a fact.

## Venture Pipeline

A venture progresses through explicit stages:

**DISCOVERED → RESEARCHING → THESIS_CREATED → ECONOMICALLY_EVALUATED → VALIDATION_REQUIRED → MVP → EARLY_REVENUE → PROVEN → SCALE**

A venture may also transition to **KILLED** from active stages where the business case is rejected or validation fails.

Stages are state, not proof of success.

## Recurring / Low-Touch Revenue

The product should explicitly represent recurring revenue and automation intensity.

The business objective is not to assume that income can be literally passive.

Instead, the system should identify opportunities with high automation potential, recurring revenue, low human dependency, and acceptable maintenance/support economics.

## Investment Boundary

Investment opportunities are initially a research and decision-support concern.

The platform may:

- research markets/assets;
- compare evidence and economics;
- model scenarios;
- surface risks and assumptions;
- produce recommendations for human decision-making.

Automatic financial execution is outside the current implementation boundary and requires a separate explicit policy/approval gate.

## Game Opportunities

Games are valid opportunity types.

Game analysis may later consider:

- market demand;
- genre and competitor patterns;
- monetization;
- development cost;
- time to MVP;
- retention;
- distribution;
- automation potential;
- expected economics.

The platform should mine business-model patterns and differentiation opportunities rather than implement literal copying of another product.

## Capital Allocation

Capital allocation is a future domain gate.

It must not optimize only ROI. Future models should consider:

- economic return;
- risk;
- liquidity;
- capital requirement;
- time to revenue;
- recurring revenue potential;
- automation potential;
- human dependency;
- scalability;
- strategic fit;
- evidence quality;
- exit / expansion potential;
- opportunity cost.

Automatic capital movement remains out of scope until explicit policy, controls, auditability, and approval requirements are designed.

## Architecture Constraints

Committed:

- Modular monolith.
- Domain meaning remains independent from infrastructure.
- AI remains a replaceable capability.
- Marketplace integrations remain replaceable adapters.
- Venture discovery is not owned by a single AI provider.
- External observations, normalized data, analysis, hypotheses, and decisions remain distinct.
- Learning does not silently rewrite policy.
- High-risk or irreversible actions require explicit policy and appropriate approval.

## Current Implementation Scope

This gate adds foundational domain concepts only:

- opportunity types;
- evidence taxonomy;
- business-model hypotheses;
- venture evaluation;
- venture lifecycle.

It does not introduce:

- marketplace SDKs;
- financial execution;
- persistence;
- HTTP/API;
- UI;
- AI provider dependencies;
- portfolio optimization algorithms.

## Next Design Gates

1. Resource Economics / Capacity.
2. Market Intelligence and Demand Discovery.
3. Venture Validation / Experimentation.
4. Portfolio and Capital Allocation.
5. Revenue Engine / Recurring Revenue.

