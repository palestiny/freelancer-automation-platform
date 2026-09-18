# Project State

## Current Phase

**Phase 16 — Operational Measurement & Learning Integration**

The project has completed the provider-independent foundations for opportunity intelligence, economics, market intelligence, venture validation, revenue, communication, marketing optimization, and multi-business operations. The operational outcomes → measurement → learning bridge is now implemented as a provider-independent domain foundation.

## Verified Test / CI State

- The repository contains one canonical GitHub Actions CI workflow: `.github/workflows/ci.yml`.
- CI run **245** for commit `b342928c79a5abfdc2376f0d8b28eaca448fbaf9` completed successfully after the evidence-aware operational-learning change. The merged PR is now in `main`; a post-merge `main` workflow result has not been independently exposed by the current repository workflow interface.
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

## Current Implementation Slice

Phase 16 — Operational Measurement & Learning Integration is implemented through deterministic performance history, explicit windows, aggregation, descriptive trend comparison, baseline eligibility, provenance compatibility, source-reliability policy, and evidence-aware operational learning.

The current boundary remains domain-only. Statistical inference, persistence, provider integration, automatic experiment execution, automatic policy mutation, and financial execution remain outside the implementation.

The next architectural decision should therefore be a deliberate Phase 16 closure review: identify any remaining semantic gaps or duplicated policy logic before opening a new statistical-learning or infrastructure slice.


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

1. Phase 16 closure / semantic consistency review.
2. Statistical learning or inference under a dedicated design gate.
3. Persistence/API when required by a concrete application boundary.
4. Portfolio posture and allocation policy as a future strategic domain.

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

1. Phase 16 closure / semantic consistency review.
2. Statistical learning or inference only after an explicit design gate.
3. Persistence / API only when a concrete product boundary requires it.
4. Portfolio posture and allocation policy remains a future strategic domain.

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


## Operational Measurement & Learning

The first operational learning foundation is now implemented:

**Work Item → Outcome Observation → Operational Measurement → Variance → Learning Signal → Improvement Recommendation**

Implemented domain objects:

- WorkItemOutcomeObservation
- OperationalMeasurement
- BusinessPerformanceSnapshot
- LearningSignal
- ImprovementRecommendation

The domain preserves expected and actual values separately, derives variance, enforces business ownership, and requires an explicit policy-review or experiment handoff for improvement recommendations.

Learning remains evidence/recommendation, not silent policy mutation.

Repeated-variance learning policy and multi-source evidence are now implemented. Historical persistence, scheduling, statistical inference, automatic experiment execution, provider integrations, and financial execution remain future work.


## Current Implementation Addition — Business Performance History

The Phase 16 foundation now includes a normalized business-level performance history:

**Operational / Revenue / Campaign Evidence → BusinessPerformanceObservation → BusinessPerformanceHistory → Variance / Learning**

The normalized observation preserves source type/source identifier, business ownership, metric/unit, optional expected value, actual value, observation time, and evidence quality. Variance is derived only when an expectation exists.

BusinessPerformanceHistory enforces single-business isolation and provides deterministic chronological ordering, metric/unit filtering, and latest-observation access.

This is a normalized evidence view, not a replacement for source domains and not a policy or execution mechanism.

Those evidence/provenance, baseline, and bounded comparison foundations are now implemented. The next engineering work is a Phase 16 closure review before introducing statistical learning or infrastructure.

## Current Implementation Addition — Evidence-Aware Measurement Learning

Operational measurements now carry bounded evidence quality. Repeated-variance learning derives the resulting LearningSignal evidence quality from the average quality of its contributing measurements.

The implementation therefore no longer relies on the previous neutral evidence baseline. Rich provenance and more advanced evidence aggregation remain future policy/design work.

The latest implementation slices remain domain-only. CI has been verified green on the relevant pull-request runs; no claim is made about an unexposed post-merge run.

## Current Implementation Addition — Performance Windows

Phase 16 now has deterministic time-window primitives for business performance history. Window selection is explicit and does not infer trends, aggregate across businesses, or mutate policy.
## Current Measurement Addition — Historical Aggregation

The current Phase 16 foundation now includes deterministic historical aggregation through `app/domain/performance_aggregation.py`.

The aggregate is:
- business/metric/unit scoped
- restricted to an explicit performance window
- traceable to source observation IDs
- based on actual count/average/minimum/maximum
- based on expected values only where expectations exist
- evidence-quality aware

Missing expectations are not converted to zero, and zero expectations do not create relative variance. No provider, persistence, statistical inference, or automatic policy mutation has been introduced.

## Immediate Next Slice

Trend comparison and evidence-aware baseline eligibility are now implemented. The next measurement slice is a bounded comparison/learning policy over eligible baselines, still deterministic and without premature statistical inference.

## Current Measurement Addition — Performance Trend & Baseline

Phase 16 now includes `app/domain/performance_trend.py`, providing a deterministic comparison between two compatible `PerformanceAggregate` instances.

The comparison:
- requires explicit current and baseline windows
- preserves business, metric, and unit identity
- reports current/baseline averages
- derives absolute change
- derives relative change only when the baseline average is non-zero
- preserves source observation identifiers
- carries evidence quality for both windows

A missing window produces no comparison. The result is descriptive evidence, not a forecast, recommendation, or policy decision.

Statistical inference remains deliberately deferred.


## Current Measurement Addition — Evidence & Baseline Policy

The Measurement & Learning domain now includes an explicit evidence-aware baseline eligibility policy. A supplied historical aggregate can be assessed against minimum observation count, minimum average evidence quality, and explicit maximum age. Future baselines are rejected, and every ineligible result has a deterministic reason. The policy does not select baselines, forecast, mutate policy, or execute actions.

Eligible historical evidence is now consumed by the bounded comparison policy. Statistical inference remains deliberately deferred.

## Current Measurement Addition — Bounded Performance Comparison

Phase 16 now includes an explicit comparison-policy foundation. A comparison first requires an eligible baseline, then checks current observation count and evidence quality, business/metric/unit compatibility, and non-overlapping temporal windows.

A successful result is the existing descriptive PerformanceTrend. Rejected comparisons return an explicit reason. No forecasting, statistical inference, ranking, scoring, policy mutation, or external execution was introduced.

The evidence/provenance enrichment and bounded comparison slices are now implemented. Statistical learning remains deliberately deferred until its own design gate.

## Current Measurement Addition — Performance Evidence Provenance

Phase 16 now preserves source-type provenance in PerformanceAggregate alongside raw observation identifiers. A comparison rejects current/baseline aggregates with incompatible source provenance, preventing identical metric/unit labels from silently crossing evidence domains.

Raw observations remain authoritative. This slice does not introduce source-reliability scoring, causal attribution, statistical inference, persistence, provider integration, or automatic policy mutation.

## Current Measurement Addition — Performance Source Reliability Policy

Phase 16 now has an explicit `PerformanceSourceReliabilityPolicy` and `SourceReliabilityAssessment` foundation. Source reliability is policy-derived and separate from observation-level evidence quality. Mixed-source aggregates are assessed conservatively using the weakest configured source reliability, while missing source configuration blocks eligibility with an explicit reason.

This remains a provider-independent eligibility input. It does not rank providers, infer causality, forecast, mutate policy, or execute external actions.

The latest branch changes are awaiting CI verification before any green-test claim is recorded.

## Current Measurement Addition — Baseline Reliability Integration

Baseline eligibility now optionally consumes `PerformanceSourceReliabilityPolicy`. This preserves the distinction between source reliability and observation-level evidence quality while making reliability a real eligibility gate. Existing baseline policies without source reliability retain their prior behavior.

The comparison layer continues to consume `BaselineEligibility` without duplicating reliability logic.

## Current Measurement Addition — Current Evidence Source Reliability

`PerformanceComparisonPolicy` now optionally requires source reliability for current aggregates. Current reliability is an additional gate beside observation sufficiency and evidence quality, with explicit missing/insufficient rejection reasons. Baseline reliability remains owned by `PerformanceBaselinePolicy`.

## Current Measurement Addition — Evidence-Aware Operational Learning

`OperationalLearningPolicy` now includes `minimum_average_evidence_quality`. Learning signals require sufficient evidence quality as well as minimum observations and material average relative variance. The default threshold remains 50 to preserve the existing measurement evidence baseline. The policy does not mutate source measurements or execute actions.

## Current Measurement Addition — Provenance Compatibility Hardening

Performance comparison now treats source-type provenance as an unordered set of evidence domains rather than an ordered tuple. Compatibility still requires exact source-domain membership. Reliability assessment state is also validated so the eligibility flag cannot contradict its reason.
