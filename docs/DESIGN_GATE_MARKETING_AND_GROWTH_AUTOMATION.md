# Marketing & Growth Automation Design Gate

## Status

**APPROVED — V1 product and domain direction committed; campaign foundation implemented.**

## Problem

A viable business does not need to be a new category or an empty market.

The platform must be able to recognize and validate opportunities in existing competitive markets when there is a credible economic thesis based on positioning, execution, distribution, automation, niche selection, customer experience, cost structure, or another explicit advantage.

After a business is validated, the platform must also be able to operate the growth loop that turns demand into measurable acquisition and revenue.

## Core Decision

**Competition is an evaluation input, not an automatic rejection rule.**

An existing market, existing service, existing SaaS, game, digital product, or other business can remain a valid opportunity when its business thesis is evidence-backed and economically testable.

The platform therefore supports two related but distinct questions:

1. **Should this business exist?**
2. **How should this business acquire and retain demand?**

The first belongs to Opportunity/Venture Intelligence, Business Model Discovery, Economics, and Validation.

The second belongs to Revenue/Growth and Marketing Automation.

## Growth Loop

The broader operating loop becomes:

**Discover → Evaluate → Validate → Build → Market → Sell → Operate → Measure → Learn → Experiment → Scale / Kill → Portfolio**

Marketing is therefore not a post-processing feature. It is part of the economic operating loop.

## Marketing & Growth Domain Direction

Future responsibility includes:

- positioning and offer communication
- audience definition
- campaign planning
- organic content planning
- paid advertising experiments
- social presence management
- lead acquisition
- campaign measurement
- customer/comment response
- channel performance analysis
- campaign learning and iteration

The domain owns business intent, campaign state, measurable objectives, constraints, and outcomes.

External platforms remain replaceable adapters/capabilities.

## Campaign as an Experiment

A marketing campaign is not assumed to succeed.

A campaign should be representable as a measurable experiment containing:

- business/venture context
- objective
- target audience
- offer/positioning
- channels
- budget constraint when applicable
- approval/authorization state
- campaign lifecycle
- measurable performance observations

Relevant metrics may include:

- impressions
- clicks
- CTR
- leads
- conversions
- spend
- revenue
- CAC
- conversion rate
- ROAS

Metrics are observations. Derived conclusions and decisions must preserve their evidence and uncertainty.

## Social Presence and Customer Communication

The future platform may prepare and operate social pages/accounts, publish approved content, monitor comments, classify incoming feedback, draft or send policy-compliant responses, escalate sensitive cases, and measure resulting engagement.

Account creation, credential handling, publishing, paid spend, and direct customer communication are external actions and must remain behind explicit capabilities and policy/authorization boundaries.

The domain must not depend on a specific social network, advertising provider, AI provider, or communication SDK.

## Safety and Approval

Marketing automation does not bypass existing autonomy and safety rules.

In particular:

- ad spend is an external financial action and requires explicit authorization/policy;
- account creation requires explicit authorization;
- publishing and customer responses must obey content, brand, privacy, and escalation policies;
- sensitive, irreversible, or high-impact actions may require human approval;
- AI can assist campaign creation and response generation but cannot become the owner of business policy.

No automatic ad-spend execution is introduced by this gate.

## Economic Integration

Marketing activity feeds the existing economic model.

Campaign economics may contribute to:

- acquisition cost
- revenue
- margin
- profitability
- demand stability
- recurring revenue
- automation
- capital efficiency
- evidence quality

The platform must preserve the distinction between campaign performance and overall business health.

A successful campaign is not itself proof that the business is healthy; business-level outcomes must be measured over appropriate periods.

## V1 Foundation

The first domain slice establishes:

1. explicit campaign objectives;
2. controlled campaign channels;
3. explicit campaign lifecycle;
4. explicit budget limits;
5. explicit authorization state;
6. measurable campaign performance snapshots;
7. derived CTR, conversion rate, CAC, and ROAS where denominators are defined;
8. validation of non-negative metrics and coherent metric relationships.

This foundation remains provider-independent.

## Explicit Non-Goals

This gate does not implement:

- real social accounts;
- real advertising accounts;
- real ad spend;
- credentials;
- platform-specific APIs;
- automated public replies;
- content generation providers;
- campaign optimization algorithms;
- universal marketing score;
- automatic budget reallocation;
- financial execution.

Those require later application/integration design and policy decisions.

## Trade-offs

### Existing market vs empty market

We choose to treat competition as evidence and context rather than a hard rejection rule.

**Benefit:** the platform can pursue proven demand with differentiated economics or execution.

**Cost:** competition analysis becomes more important and cannot be replaced by a simple market-gap heuristic.

### Campaign model vs provider-specific advertising model

We choose a provider-independent campaign domain.

**Benefit:** the business model survives changes in ad/social providers.

**Cost:** provider-specific capabilities require adapters and mapping.

### Automation vs approval

We choose progressive autonomy rather than unrestricted automation.

**Benefit:** high-risk actions remain controllable.

**Cost:** some workflows require explicit approvals before full automation.

## Follow-Up Design Gates

- Revenue Engine / Recurring Revenue
- Social Presence & Communication
- Campaign Optimization & Budget Policy
- Content Production & Brand Policy
- Measurement & Learning for Growth
