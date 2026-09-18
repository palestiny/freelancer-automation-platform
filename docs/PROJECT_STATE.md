# Project State

## Current Phase

**Phase 16 — Operational Measurement & Learning Integration**

The project has completed the provider-independent foundations for opportunity intelligence, economics, market intelligence, venture validation, revenue, communication, marketing optimization, and multi-business operations. The next missing domain bridge is operational outcomes → measurement → learning.

## Verified Test / CI State

- The repository contains one canonical GitHub Actions CI workflow: `.github/workflows/ci.yml`.
- A previous verified run on commit `7bf259b68bc24bcf3ab8b40ba1752c27e4427b8c` completed successfully with **119 passed** tests.
- The latest CI run for commit `b0d5e6659ae1067cd775fa747c84cb68e8320185` reached the test step successfully; final workflow completion should be verified before calling the latest run green.
- CI is intentionally dependency-minimal at this stage: it installs pytest directly because the repository currently has no `requirements.txt` or `pyproject.toml`.

## Implemented Domain Foundations

- Opportunity types and evidence taxonomy.
- Six-dimensional Opportunity Evaluation foundations.
- Business Model Hypothesis.
- Venture evaluation and lifecycle.
- EconomicEstimate and EconomicProfile.
- ResourceUsage and human-time CapacitySnapshot.
- MarketObservation and DemandSignal.
- ValidationExperiment and ExperimentResult.
- RevenueContract and RevenueEvent.
- SocialPresence, IncomingMessage, ResponseDraft, authorization, and SentMessage.
- MarketingCampaign and CampaignPerformanceSnapshot.
- CampaignOptimizationPolicy and non-executing optimization recommendations.
- Business lifecycle.
- OperationalCycle and WorkItem lifecycle.

## Current Product Direction

The platform is an **Economic Opportunity OS / Business Automation OS**.

Freelancing is the first laboratory, not the permanent architectural boundary.

The broader loop is:

**Discover → Evaluate → Validate → Build → Market → Sell → Operate → Measure → Learn → Experiment → Scale / Kill → Portfolio**

## Opportunity Evaluation

The original six dimensions remain committed for applicable opportunity contexts:

1. Eligibility
2. Requirement Fit
3. Estimated Effort
4. Economic Fit
5. Client / Project Risk
6. Success Confidence

Criterion-level evidence and uncertainty remain mandatory.

Overall outcomes:

- QUALIFIED
- NOT_QUALIFIED
- REVIEW_REQUIRED

## Economic Health

Economic quality is represented as a vector rather than a universal master score:

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

Scores are derived assessments supported by evidence/metrics. Stable profitable businesses remain representable as economically valuable assets even when growth upside is modest.

## Resource Economics & Capacity

V1 explicitly models:

- resource kind
- quantity
- monetary unit cost
- total resource cost
- human-time capacity
- committed/reserved/remaining hours
- utilization

Resource cost and capacity remain separate concepts.

## Market Intelligence & Validation

The current discovery/validation boundaries are:

**External Observation → Demand Signal → Opportunity Hypothesis**

and:

**Venture Thesis → Hypothesis → Experiment → Result → Evidence → Explicit Decision**

Experiment results do not silently rewrite policy, economics, venture lifecycle, or portfolio posture.

## Revenue

The revenue boundary is:

**Business Model → Revenue Contract → Realized Revenue Event → Economic Measurement → Learning**

Actual revenue remains distinct from expected revenue. Payment execution remains outside the domain.

## Communication & Growth

Communication:

**Presence → Incoming Message → Classification → Response Draft → Authorization → Sent Message → Learning**

Marketing:

**Campaign → Performance Observation → Optimization Policy → Recommendation → Authorization → External Execution → New Observation**

Recommendations do not execute external actions. Budget limits are hard constraints.

## Business Operations

Operations:

**Business → Operational Cycle → Work Item → Outcome Observation → Measurement / Learning**

Business identity is separate from operational state. Each operational cycle and work item belongs to exactly one business.

Scheduling, workers, provider APIs, credentials, payment execution, automatic capital movement, and AI model selection remain outside the domain.

## Next Implementation Slice

The next Design Gate should define **Operational Measurement & Learning Integration**.

It should connect actual work outcomes to the existing economic/revenue/campaign/venture evidence model without:
- silently changing policy
- inventing forecasts from observations
- coupling to providers
- introducing persistence prematurely
- introducing automatic financial execution


## Opportunity Evaluation Model

The original six Opportunity Intelligence dimensions remain committed for their applicable opportunity context:

1. Eligibility
2. Requirement Fit
3. Estimated Effort
4. Economic Fit
5. Client / Project Risk
6. Success Confidence

Criterion-level evidence and uncertainty remain mandatory.

Overall outcomes:

- QUALIFIED
- NOT_QUALIFIED
- REVIEW_REQUIRED

Numeric scoring is not required for the first Opportunity Intelligence slice.

## Economic Health Model

Economic quality is represented separately from the six-dimensional Opportunity Evaluation model.

The V1 Economic Profile contains bounded 0–100 scores for:

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

The platform deliberately does **not** collapse these into a universal master score.

Scores are derived assessments. Future scoring policies may change formulas, thresholds, evidence requirements, time windows, and baselines without changing business or opportunity identity.

A stable profitable business must be representable as an economically valuable asset even when its theoretical growth upside is modest.

Future portfolio postures may include:

- PROTECT
- MAINTAIN
- OPTIMIZE_CAREFULLY
- GROW
- HARVEST
- TURNAROUND
- EXIT

These are policy-derived actions, not intrinsic business properties.

## Resource Economics & Capacity

V1 now has explicit domain foundations for resource consumption and human-time capacity.

Resource usage captures:

- resource kind
- quantity
- monetary unit cost
- derived total cost

Supported resource kinds:

- HUMAN_TIME
- CAPABILITY_USAGE
- INFRASTRUCTURE
- COMMUNICATION
- MARKETPLACE_FEE
- REVIEW_TIME

Capacity snapshots capture:

- planning period
- total human-time hours
- committed hours
- reserved hours
- remaining hours
- utilization

Capacity remains operational constraint data. It is not itself a profitability or economic-health score.

## Broader Opportunity Model

Supported opportunity types now include:

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

These are not forced into one universal evaluation algorithm.

## Venture Evaluation

The broader venture model evaluates:

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

The evaluation remains evidence-aware and explainable.

## Evidence Model

The domain distinguishes:

FACT → OBSERVATION → ESTIMATE → ASSUMPTION → HYPOTHESIS → FORECAST → EXPERIMENT_RESULT

These labels represent epistemic status, not a ranking of value.

## Business Model Discovery

The domain can represent multiple business-model hypotheses for the same opportunity, including service, productized service, managed service, SaaS, API, digital product, game, white-label, subscription, and partnership models.

Recurring revenue and automation intensity are explicit attributes.

## Venture Pipeline

**DISCOVERED → RESEARCHING → THESIS_CREATED → ECONOMICALLY_EVALUATED → VALIDATION_REQUIRED → MVP → EARLY_REVENUE → PROVEN → SCALE**

A venture can be killed through explicit lifecycle transitions.

## Current Implementation Boundary

Still domain-only:

- domain models
- domain services
- domain value objects
- domain tests

Still outside the current slice:

- marketplace SDKs
- real marketplace credentials
- persistence
- HTTP/API
- UI
- AI provider dependencies
- financial execution
- automatic capital movement

## Next Design Gates

1. Market Intelligence / Demand Discovery.
2. Venture Validation / Experimentation.
3. Portfolio posture and allocation policy.
4. Revenue Engine / Recurring Revenue.

## Learning Loop

**Expected → Actual → Variance → Learning Signal → Controlled Policy/Experiment Improvement**

Learning must not silently rewrite policy.

## Project Health Rule

A meaningful increment is done only after applicable design, RED/GREEN TDD, review, refactoring, documentation, passing tests, commit/push, and project-state update.


## Marketing & Growth Direction

The platform now explicitly supports the thesis that existing competitive markets can contain valid opportunities. Competition is an evaluation input, not an automatic rejection rule.

A validated Service, Game, SaaS, Product, Digital Asset, or other business can move into a growth loop:

**Build → Market → Sell → Operate → Measure → Learn → Experiment**

The first provider-independent marketing campaign foundation is implemented:

- campaign objectives
- controlled channels
- lifecycle state
- budget limit
- authorization state
- performance snapshot
- CTR
- conversion rate
- CAC
- ROAS

No real ad spend, social credentials, account creation, provider APIs, or automatic public communication are implemented in the current domain-only slice.

## Current Next Design Gates

1. Market Intelligence / Demand Discovery.
2. Venture Validation / Experimentation.
3. Revenue Engine / Recurring Revenue.
4. Social Presence & Customer Communication.
5. Campaign Optimization & Budget Policy.
6. Portfolio posture and allocation policy.

## Current Implementation Addition

`app/domain/marketing_campaign.py` is the provider-independent foundation for campaign lifecycle and measurable campaign performance.

## Market Intelligence & Demand Discovery

The first Market Intelligence foundation is now implemented.

Provider-independent domain objects represent:

- external market observations
- source provenance
- observation time
- evidence quality
- derived demand signals
- demand strength
- supporting observation count

The boundary is explicit:

**External Observation → Demand Signal → Opportunity Hypothesis**

Market observations do not become business truth automatically, and existing competitive demand remains valid input for opportunity discovery.

## Updated Current Next Design Gates

1. Venture Validation / Experimentation.
2. Revenue Engine / Recurring Revenue.
3. Social Presence & Customer Communication.
4. Campaign Optimization & Budget Policy.
5. Portfolio posture and allocation policy.
6. Market Intelligence normalization, trend, and source-reliability follow-up.

## Venture Validation & Experimentation

The validation foundation now represents a measurable, bounded experiment independently of any provider.

A ValidationExperiment preserves:

- hypothesis
- objective
- success criterion
- controlled variants
- budget limit
- explicit lifecycle

ExperimentResult preserves:

- outcome: VALIDATED / INVALIDATED / INCONCLUSIVE
- observed measurement
- success-criterion status
- evidence statement
- explicit decision: PROMOTE / REJECT / CONTINUE_TESTING

An experiment result is evidence and does not silently mutate venture lifecycle, economics, policy, or portfolio posture.

External execution, statistical inference, spending, scheduling, and persistence remain outside this slice.


## Revenue Engine / Recurring Revenue

The V1 revenue foundation now separates expected business-model economics from realized revenue observations.

Implemented:

- RevenueContract
- explicit ONE_TIME / RECURRING revenue type
- explicit recurring periods
- RevenueEvent for realized revenue
- provider-independent currency and amount representation

Payment execution, refunds, reconciliation, invoicing, and automatic pricing remain outside the current domain slice.


## Social Presence & Customer Communication

Implemented the provider-independent communication foundation:

- SocialPresence
- IncomingMessage
- MessageClassification
- ResponseDraft
- explicit response authorization
- escalation requirement
- SentMessage

External account creation, credentials, publishing, and message delivery remain outside the domain.
