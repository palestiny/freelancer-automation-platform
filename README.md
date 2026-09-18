# Economic Opportunity OS

## Product Direction

This repository is evolving from a freelancer automation platform into an **Economic Opportunity OS / Business Automation OS**.

Freelancing remains the first laboratory because it gives us a concrete, measurable path from demand to sale to delivery to revenue and actual economics.

It is not the permanent architectural boundary.

The long-term system discovers opportunities across multiple markets, proposes multiple business models, evaluates economics and evidence, validates cheaply, operates proven businesses, learns from outcomes, and eventually supports portfolio and capital-allocation decisions under explicit policy.

## Core Economic Loop

**Market Signals → Opportunity Discovery → Business Model Discovery → Venture Thesis → Economic Evaluation → Validation → Revenue → Measurement → Learning → Experimentation → Scale / Kill → Portfolio / Capital Allocation**

## Economic Health

Profitability is not the only economic objective.

The platform maintains a changeable Economic Profile with separate 0–100 dimensions for:

- Profitability
- Profit Potential
- Profit Stability
- Demand Stability
- Safety
- Recurring Revenue
- Automation
- Capital Efficiency
- Scalability
- Evidence Quality

There is intentionally no permanent universal master score. A stable, profitable, safe business can therefore be protected even when its growth potential is modest.

Economic scores are derived assessments supported by evidence/metrics. Scoring formulas, thresholds, baselines, and time windows remain policy and may evolve without changing business identity.

Future portfolio postures such as PROTECT, MAINTAIN, GROW, and TURNAROUND are policy decisions, not intrinsic business states.

## Resource Economics & Capacity

Resource economics is now a first-class domain foundation.

Resource usage explicitly captures:

- resource kind
- quantity
- monetary unit cost
- derived total cost

V1 resource kinds are:

- HUMAN_TIME
- CAPABILITY_USAGE
- INFRASTRUCTURE
- COMMUNICATION
- MARKETPLACE_FEE
- REVIEW_TIME

Human time is the first constrained capacity model. Capacity snapshots track total, committed, reserved, remaining, and utilization hours for a defined planning period.

Resource cost answers **what was consumed and what it cost**. Capacity answers **what constrained availability remains**. They are operational/economic inputs, not Economic Health scores.

## Opportunity Types

- Freelance
- Service
- Product
- SaaS
- Game
- Digital Asset
- Recurring Revenue
- Partnership
- Investment
- Acquisition

These types are explicit domain categories. They are not forced into one universal evaluation algorithm.

## Opportunity Intelligence

The original six dimensions remain committed for their applicable opportunity context:

1. Eligibility
2. Requirement Fit
3. Estimated Effort
4. Economic Fit
5. Client / Project Risk
6. Success Confidence

Evaluation remains explainable and preserves criterion-level evidence and uncertainty.

## Venture Intelligence

Broader ventures use a separate evaluation model covering:

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

## Evidence

The domain distinguishes:

**FACT → OBSERVATION → ESTIMATE → ASSUMPTION → HYPOTHESIS → FORECAST → EXPERIMENT_RESULT**

This prevents estimates and hypotheses from silently becoming facts.

## Business Model Discovery

The same demand can produce multiple hypotheses:

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

Recurring revenue and automation intensity are explicit.

## Low-Touch Recurring Revenue

The system should search for businesses with recurring revenue, high automation potential, low human dependency, and acceptable maintenance/support economics.

"Passive income" is modeled as low-touch recurring economics, not assumed literal passivity.

## Investment Boundary

Investment opportunities are initially research and decision support.

Automatic financial execution and automatic capital movement are outside the current domain implementation boundary.

## Architecture

- Modular monolith initially.
- Domain logic is independent from HTTP, persistence, marketplace SDKs, UI, AI providers, and financial execution providers.
- External platforms are isolated behind replaceable adapters.
- AI and tools are replaceable capabilities.
- Business decisions are explainable and auditable.
- Learning produces evidence and recommendations; it does not silently rewrite policy.
- High-risk or irreversible actions require explicit policy and appropriate approval.
- Economic scoring policy remains changeable and separate from core business identity.

## Current Domain Foundations

Implemented:

- OpportunityType
- Evidence taxonomy
- BusinessModelHypothesis
- Venture evaluation
- Venture lifecycle
- EconomicEstimate
- EconomicProfile
- ResourceUsage
- ResourceKind
- CapacitySnapshot
- Opportunity Intelligence foundations

Still outside the current slice:

- marketplace SDKs
- real credentials
- persistence
- HTTP/API
- UI
- AI provider dependencies
- financial execution
- automatic capital movement
- scheduling/calendar integration
- actual-vs-expected historical measurement

## Engineering Process

**UNDERSTAND → MAP → DESIGN → DISCUSS TRADE-OFFS → DECIDE → TEST → IMPLEMENT → REVIEW → REFACTOR → DOCUMENT → LEARN → UPDATE THE MAP**

See KHALED_ENGINEERING_WORKING_RULES.md and docs/README.md.


## Existing Markets & Growth Automation

The platform does not require an empty market.

An existing Service, Game, SaaS, Product, Digital Asset, or other business can be a valid opportunity when its economic thesis is evidence-backed and testable. Competition is an input to evaluation, not an automatic rejection rule.

The broader operating loop is:

**Discover → Evaluate → Validate → Build → Market → Sell → Operate → Measure → Learn → Experiment → Scale / Kill → Portfolio**

Marketing and growth are therefore first-class future platform capabilities. The platform should eventually be able to design measurable campaigns, prepare content, manage authorized social presence, monitor customer feedback, and learn from campaign performance.

The first provider-independent campaign domain foundation is implemented in `app/domain/marketing_campaign.py`. It models objectives, channels, lifecycle, authorization, budget limits, and measurable performance snapshots.

Real advertising spend, social accounts, credentials, provider APIs, and automatic public communication remain outside the current domain-only boundary.

## Market Intelligence & Demand Discovery

The platform now distinguishes external market observations from derived demand signals.

**External Observation → Demand Signal → Opportunity Hypothesis**

The first provider-independent foundation is implemented in `app/domain/market_intelligence.py` with:

- MarketObservation
- source provenance
- observation timestamp
- evidence quality
- DemandSignal
- demand strength
- supporting observation count

Search engines, scraping systems, social networks, marketplaces, data providers, and AI research tools remain replaceable external capabilities.


## Venture Validation & Experimentation

The platform now has a provider-independent validation experiment foundation.

**Venture Thesis → Hypothesis → Experiment → Measurable Result → Explicit Decision → Evidence / Learning**

Experiments support:

- measurable success criteria
- controlled variants
- budget limits
- explicit lifecycle
- VALIDATED / INVALIDATED / INCONCLUSIVE outcomes
- PROMOTE / REJECT / CONTINUE_TESTING decisions

Validation results become evidence. They do not silently change venture state, policy, economics, or portfolio posture.

External execution, real spending, customer communication, statistical inference, persistence, and scheduling remain outside the current domain-only slice.


## Revenue & Recurring Economics

The platform now has a provider-independent revenue foundation:

**Business Model → Revenue Contract → Realized Revenue Event → Economic Measurement → Learning**

Recurring revenue is explicit and period-bound. Actual revenue is represented separately from expected revenue. Payment execution remains outside the domain.


## Social Presence & Customer Communication

The platform now models the communication loop independently of external providers:

**Presence → Incoming Message → Classification → Response Draft → Authorization → Sent Message → Learning**

External account access and message delivery remain capability boundaries, and AI cannot bypass authorization.


## Campaign Optimization & Budget Policy

Campaign performance now feeds a provider-independent optimization recommendation layer:

**Performance Observation → Optimization Policy → Recommendation → Authorization → External Execution**

V1 supports CONTINUE, INCREASE_BUDGET, DECREASE_BUDGET, and PAUSE recommendations. Recommendations are bounded by campaign budget limits and require sufficient observations before optimization. They do not execute external actions.

Paid advertising remains an explicitly authorized financial action. Ad-provider APIs, credentials, payment execution, statistical attribution, and automatic spend remain outside the current domain-only boundary.


## Business Operations

The platform now models businesses as first-class managed entities with provider-independent operational cycles and work items:

**Business → Operational Cycle → Work Item → Outcome Observation → Measurement / Learning**

This creates the foundation for operating multiple businesses without coupling core business meaning to schedulers, workers, marketplaces, payment providers, or AI.


## Operational Measurement & Learning

The first operational learning bridge is now implemented:

**Work Item → Outcome Observation → Operational Measurement → Variance → Learning Signal → Improvement Recommendation**

The foundation preserves expected and actual values separately, derives variance, keeps measurement explicitly owned by a business, and requires improvement recommendations to hand off explicitly to policy review or experimentation.

Learning is evidence and recommendation, not silent policy mutation. Historical aggregation, persistence, statistical inference, and external execution remain future work.
