# Decision Log

## Canonicalization

This is the canonical decision register. Duplicate legacy identifiers were reassigned to unique IDs during documentation cleanup so every decision has exactly one identifier. The decision text was preserved; this cleanup does not change runtime behavior. Unused numeric IDs are intentionally left unused.

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


## D-039 — Market Intelligence Preserves Observation Boundaries

**Status:** COMMITTED

Market Intelligence separates external observations from derived demand signals and downstream opportunity/business decisions.

External observations preserve provenance and observation time. Demand signals are derived assessments with explicit evidence quality and supporting-observation counts.


## D-040 — Existing Demand Is Valid Discovery Input

**Status:** COMMITTED

Demand discovery must support both emerging demand and established demand in competitive markets. Existing competition does not invalidate demand; it becomes evidence/context for later venture and business-model evaluation.


## D-041 — Market Intelligence Is Provider-Independent

**Status:** COMMITTED

Core Market Intelligence does not depend on a search engine, scraping provider, social network, marketplace, data vendor, or AI provider. External research enters through replaceable adapters/capabilities.


## D-042 — Validation Is Explicit Experimentation

**Status:** COMMITTED

A venture thesis is not considered proven merely because research or economic estimates look attractive. Validation must use a bounded, measurable experiment that produces decision-useful evidence.


## D-043 — Experiment Variants Are Explicit

**Status:** COMMITTED

Controlled variants are first-class experiment data so alternative offers, prices, messages, or approaches can be compared without embedding provider-specific execution into the domain.


## D-044 — Experiment Results Are Evidence, Not Silent Policy Changes

**Status:** COMMITTED

Experiment results become EXPERIMENT_RESULT evidence and carry an explicit PROMOTE, REJECT, or CONTINUE_TESTING decision. Results do not silently mutate venture lifecycle, policy, economics, or portfolio posture.


## D-045 — Revenue Is Explicitly Split Into Expected and Realized

**Status:** COMMITTED

Revenue contracts describe the commercial model, while RevenueEvent represents realized revenue. The platform must not confuse forecasts or pricing hypotheses with actual revenue.


## D-046 — Recurring Revenue Requires an Explicit Period

**Status:** COMMITTED

Recurring revenue is modeled explicitly with a recurring period. A recurring label alone is insufficient.


## D-047 — Payment Execution Is Outside the Revenue Domain

**Status:** COMMITTED

The core domain does not process payments or move money. Payment providers remain replaceable capabilities behind authorization and policy.


## D-048 — Communication Is Provider-Independent

**Status:** COMMITTED

The core domain models communication meaning and authorization without depending on social, email, chat, or messaging providers.


## D-049 — Drafts Are Not Sent Messages

**Status:** COMMITTED

A generated response draft is distinct from an actually sent message. This preserves an auditable boundary between preparation and external action.


## D-050 — Escalation Overrides Automated Approval

**Status:** COMMITTED

A communication requiring escalation cannot simultaneously be approved for automated sending in the V1 domain foundation.


## D-051 — Credentials Stay Outside the Domain

**Status:** COMMITTED

External account credentials and provider authentication remain adapter/infrastructure concerns and are not represented by the communication domain.


## D-052 — Optimization Produces Recommendations, Not Silent Spend Changes

**Status:** COMMITTED

Campaign optimization recommendations do not execute provider actions or mutate external spend.


## D-053 — Budget Limits Are Hard Safety Constraints

**Status:** COMMITTED

Optimization recommendations cannot exceed the explicit campaign budget limit.


## D-054 — Optimization Requires Sufficient Evidence

**Status:** COMMITTED

Insufficient observations produce a non-executable recommendation state rather than invented certainty.


## D-055 — Optimization Policy Is Changeable

**Status:** COMMITTED

Optimization thresholds and adjustment rules remain policy and may evolve independently of business identity.


## D-056 — Financial Spend Remains Explicitly Authorized

**Status:** COMMITTED

Paid spend remains an external financial action. V1 does not introduce automatic ad spending.


## D-057 — Business Is a First-Class Domain Entity

**Status:** COMMITTED

A managed business has an identity separate from an opportunity, venture thesis, campaign, or revenue contract.


## D-058 — Operations Are Separate From Business Identity

**Status:** COMMITTED

Operational state can change without redefining the business.


## D-059 — Work Is Provider-Independent

**Status:** COMMITTED

The domain represents operational work meaning; scheduling, workers, providers, and AI remain external capabilities/infrastructure.


## D-060 — Multi-Business Isolation Is Explicit

**Status:** COMMITTED

Each operational cycle and work item belongs to exactly one business.


## D-061 — Operations Produce Evidence

**Status:** COMMITTED

Operational outcomes are observations for learning and do not silently rewrite economics, policy, or business state.


## D-062 — Operational Outcomes Are First-Class Observations

**Status:** COMMITTED

Work-item outcomes are explicit observations that preserve what happened without directly changing policy or business state.


## D-063 — Expected and Actual Values Remain Separate

**Status:** COMMITTED

Operational measurements preserve expected and actual values independently and derive variance rather than overwriting estimates with observations.


## D-064 — Learning Signals Are Evidence, Not Policy

**Status:** COMMITTED

Learning signals summarize evidence and cannot silently mutate business policy, economics, workflow, or lifecycle state.


## D-065 — Improvement Requires an Explicit Handoff

**Status:** COMMITTED

Improvement recommendations must explicitly target policy review or controlled experimentation. Recommendations are not execution commands.


## D-066 — Operational Measurement Is Provider-Independent

**Status:** COMMITTED

Operational measurement meaning remains independent from schedulers, workers, providers, databases, HTTP, AI, and financial execution.


## D-067 — Business Isolation Applies to Measurement

**Status:** COMMITTED

Operational observations, measurements, learning signals, and recommendations carry explicit business ownership. Cross-business measurement contamination is invalid.


## D-068 — Business Performance History Is a Normalized Evidence View

**Status:** COMMITTED

Business Performance History is a derived, provider-independent view over bounded observations. It does not replace the source domain that produced an observation.


## D-069 — Source Identity Is Preserved

**Status:** COMMITTED

Every normalized performance observation preserves its source type and source identifier.


## D-070 — Expected Values May Be Absent

**Status:** COMMITTED

An actual performance observation may exist without an expected value. The platform must not invent an expectation to manufacture variance.


## D-071 — Business Isolation Is Mandatory

**Status:** COMMITTED

A performance history belongs to exactly one business. Cross-business observations cannot be combined.


## D-072 — History Does Not Mutate Source Domains

**Status:** COMMITTED

Organizing performance evidence does not mutate operational state, revenue, campaign state, economic profiles, or business lifecycle state.


## D-073 — Aggregation Policy Remains Separate

**Status:** COMMITTED

Ordering, filtering, time windows, baselines, thresholds, and future statistical methods remain changeable policy rather than hard-coded business identity rules.

## D-074 — Historical Aggregates Preserve Raw Evidence

**Status:** COMMITTED

Historical aggregation produces a derived summary over normalized performance observations. It must preserve source observation identifiers, business/metric/unit context, and the explicit time window so aggregate values remain traceable to raw evidence.

V1 uses deterministic count, minimum, maximum, and average-style summaries. It does not introduce a universal sum operation because summation semantics depend on metric meaning.

Missing expected values are excluded from expected-derived aggregates rather than treated as zero. Aggregation does not mutate source observations or policy.


## D-079 — Baseline Eligibility Is Policy, Not Evidence

**Status:** COMMITTED

A historical performance aggregate is derived evidence. Whether it is suitable for baseline use is evaluated by an explicit policy rather than embedded in the aggregate itself.


## D-080 — Baseline Eligibility Requires Sufficient Observations

**Status:** COMMITTED

Baseline eligibility requires a configurable minimum observation count; sparse history must not be treated as sufficient evidence by default.


## D-081 — Baseline Eligibility Requires Evidence Quality

**Status:** COMMITTED

Baseline eligibility requires a configurable minimum average evidence quality. Evidence quality remains an evidence property, not a correctness guarantee.


## D-082 — Baseline Freshness Is Explicit

**Status:** COMMITTED

Baseline age is evaluated against an explicit `as_of` timestamp and configurable maximum age. The domain does not infer recency from the current clock.


## D-083 — Ineligibility Must Be Explainable

**Status:** COMMITTED

Baseline assessment returns a deterministic eligibility reason, including insufficient observations, insufficient evidence quality, stale history, or future baseline timing.


## D-084 — Comparison Requires an Eligible Baseline

**Status:** COMMITTED

Performance comparison must first pass the explicit baseline eligibility policy. Comparison cannot bypass evidence sufficiency or freshness requirements.


## D-085 — Current Evidence Has Minimum Sufficiency

**Status:** COMMITTED

Current performance evidence requires configurable minimum observation count and evidence quality before producing a descriptive comparison.


## D-086 — Comparison Windows Must Be Temporally Ordered

**Status:** COMMITTED

Current and baseline windows may not overlap. The current window must start at or after the baseline window ends.


## D-087 — Comparison Produces Descriptive Evidence

**Status:** COMMITTED

The comparison policy can produce a descriptive PerformanceTrend but cannot forecast, rank, score, mutate policy, or execute actions.


## D-088 — Derived Aggregates Preserve Source-Type Provenance

**Status:** COMMITTED

Performance aggregates preserve the distinct source types represented by their normalized observations. Observation identifiers remain necessary lineage, but source-type context must also remain directly inspectable.


## D-089 — Aggregation Does Not Invent Provenance

**Status:** COMMITTED

Source provenance is copied from normalized observations. Aggregation does not infer or manufacture source identity.


## D-090 — Comparison Requires Compatible Provenance Context

**Status:** COMMITTED

A descriptive performance comparison requires matching source-type provenance between current and baseline aggregates. Identical metric/unit names are not sufficient to establish comparable evidence domains.


## D-091 — Raw Observation Lineage Remains Authoritative

**Status:** COMMITTED

Aggregates remain derived evidence views. Raw observation identifiers and source observations remain the authoritative lineage for audit and interpretation.


## D-092 — Source Reliability Is Policy-Derived

**Status:** COMMITTED

Source reliability is not an immutable observation fact. An explicit policy assigns reliability values to known source types and evaluates whether an evidence context satisfies a required minimum.


## D-093 — Observation Evidence Quality Remains Separate

**Status:** COMMITTED

Observation-level `evidence_quality` and source-type reliability are distinct concepts. Reliability policy must not silently replace observation evidence quality.


## D-094 — Mixed-Source Evidence Uses the Weakest Configured Source

**Status:** COMMITTED

When an aggregate contains multiple source types, V1 uses the minimum configured reliability among represented sources. This conservative rule avoids inventing weights between heterogeneous evidence domains.


## D-095 — Missing Reliability Configuration Blocks Eligibility

**Status:** COMMITTED

A source type without explicit reliability configuration cannot be assumed reliable. The assessment returns an explainable missing-policy result.


## D-096 — Reliability Does Not Rank or Execute

**Status:** COMMITTED

V1 source reliability is an eligibility input only. It does not rank providers, infer causal correctness, mutate evidence, execute actions, or change business policy.


## D-097 — Baseline Eligibility May Require Source Reliability

**Status:** COMMITTED

A baseline policy may optionally require an explicit source-reliability policy. Existing policies without one retain their prior behavior.


## D-098 — Source Reliability Is an Additional Gate

**Status:** COMMITTED

Source reliability does not replace minimum observations, observation-level evidence quality, or freshness. All applicable baseline requirements must pass.


## D-099 — Reliability Failures Are Explainable

**Status:** COMMITTED

Baseline eligibility distinguishes insufficient source reliability from missing source-reliability configuration.


## D-100 — Comparison Semantics Remain Stable

**Status:** COMMITTED

The comparison layer continues to consume `BaselineEligibility` and does not duplicate source-reliability logic.


## D-101 — Current Evidence Reliability Is Optional Policy

**Status:** COMMITTED

`PerformanceComparisonPolicy` may include source reliability requirements for current evidence. Existing policies without the requirement retain their previous behavior.


## D-102 — Current Reliability Is an Additional Gate

**Status:** COMMITTED

Current source reliability is checked in addition to current observation sufficiency and evidence quality.


## D-103 — Reliability Rejections Remain Explicit

**Status:** COMMITTED

Insufficient current reliability and missing current source configuration are distinct comparison rejection reasons.


## D-104 — Comparison Does Not Duplicate Baseline Reliability

**Status:** COMMITTED

Baseline reliability belongs to `PerformanceBaselinePolicy`; current reliability belongs to `PerformanceComparisonPolicy`. The comparison service composes these boundaries.


## D-105 — Learning Requires Evidence Sufficiency

**Status:** COMMITTED

Repeated variance is necessary but not sufficient for an operational learning signal. Contributing measurements must meet an explicit average evidence-quality threshold.


## D-106 — Evidence Quality Is Policy, Not Rewritten Evidence

**Status:** COMMITTED

The learning policy determines signal eligibility and does not mutate measurement evidence quality.


## D-107 — Existing Variance Rules Remain Unchanged

**Status:** COMMITTED

Minimum observations and minimum average relative variance remain independent learning requirements.


## D-108 — Learning Remains Non-Executing

**Status:** COMMITTED

A learning signal remains evidence for explicit improvement handling and does not silently change policy, economics, lifecycle, or execution.


## D-109 — Current Comparison Evidence Must Not Extend Beyond As-Of

**Status:** COMMITTED

A performance comparison requires the current aggregate window to end at or before the explicit `as_of` timestamp. This keeps both baseline and current evidence bounded by known observation time and prevents a descriptive comparison from consuming future evidence. The rule is enforced by the comparison policy and remains separate from baseline freshness policy.


## D-110 — Statistical Learning Requires Its Own Design Gate

**Status:** COMMITTED

Statistical inference is not an implicit extension of deterministic Phase 16 measurement. Any statistical method must have an explicit use case, assumptions, applicability rules, insufficient-data behavior, provenance semantics, and a defined consumer before implementation.


## D-112 — Phase 17 Uses an Explicit t-Interval Contract

**Status:** COMMITTED

The first statistical method candidate is a Student's t confidence interval for an observed mean. V1 proposes a 95% confidence level and a mathematical applicability floor of two valid observations. Invalid, insufficient, or inapplicable data must produce explicit outcomes; no fallback statistical method is selected automatically. The contract was closed for the first use case and implemented in `app/domain/statistical_mean_uncertainty.py`. Runtime scope remains limited to this use case.


## D-116 — Student's t Numerical Evaluation Has Explicit Standard-Library Semantics

**Status:** COMMITTED

The Phase 17 Student's t implementation evaluates the distribution through a regularized incomplete-beta formulation with a continued-fraction evaluation, using only the Python standard library. Numerical regression tests cover known critical values, symmetry, bounded CDF output, and non-default confidence levels. This is an implementation contract for reproducibility and numerical hardening; it does not expand the statistical use-case boundary.


## D-117 — Phase 17 Mean Uncertainty Applicability Is Explicitly Consumer-Declared

**Status:** COMMITTED

The Student's t mean-uncertainty calculation does not infer normality or independence from observations. The consumer explicitly declares applicability. Structural context and finite-value validation take precedence over applicability failure so malformed evidence is not masked.


## D-113 — Statistical Results Are Evidence Artifacts, Not Policy

**Status:** COMMITTED

The Phase 17 mean-uncertainty result is an evidence artifact. Producing a confidence interval does not mutate performance trends, learning signals, policy, business state, lifecycle state, or execution state.


## D-114 — Statistical Applicability Assumptions Are Not Silently Proven

**Status:** COMMITTED

The domain implementation does not claim to prove independence or normality from operational observations. Consumers must treat the Student's t assumptions as explicit applicability context rather than inferred facts.


## D-115 — Statistical Method Dependencies Must Remain Explicit

**Status:** COMMITTED

The first V1 statistical method uses the Python standard library and does not introduce a statistical provider dependency. Any future external statistical dependency requires an explicit design decision.


## D-118 — Phase 17 Historical Mean Comparison Uses Welch's Two-Sample t-Test

**Status:** COMMITTED

The next Phase 17 statistical use case compares observed means from two explicit, non-overlapping historical windows for the same business, metric, and unit. V1 uses a two-sided Welch's two-sample t-test with alpha = 0.05 and a mathematical minimum of two observations per window. Applicability assumptions remain consumer-declared; the domain does not infer independence or distributional assumptions. The result remains an evidence artifact and does not mutate policy, learning, business state, or execution.


## D-119 — Phase 17 Current Statistical Method Scope Is Closed

**Status:** COMMITTED

The current Phase 17 V1 statistical surface is closed after implementing and hardening two bounded methods: Student's t mean uncertainty and Welch's two-sample historical mean comparison. Additional statistical methods or automatic consumers require a concrete downstream use case and dedicated design gate. Statistical outputs remain evidence artifacts and do not replace raw evidence, source reliability, policy, or execution boundaries.


## D-120 — Phase 17 Statistical Evidence Is Composed Through an Explicit Consumer

The first downstream statistical consumer must preserve statistical results as evidence artifacts and separately evaluate evidence quality and source reliability. V1 composition may report eligibility and bounded statistical interpretation, but must not collapse evidence into a universal score or mutate policy, learning, lifecycle, portfolio, or execution state.


## D-122 — Statistical Detection Does Not Establish Directional Alignment

The evidence composition layer must not label descriptive and inferential evidence as aligned merely because a statistical difference is detected. Direction is derived from the descriptive trend, while statistical detection remains a separate inferential status.


## D-121 — Descriptive and Inferential Performance Evidence Remain Separate

The first decision-support composition layer may expose descriptive direction alongside statistical evidence status, but must preserve disagreement and must not convert the combination into a score, recommendation, policy mutation, or execution action.


## D-123 — Evidence Composition Boundary Is Semantically Closed

The current V1 evidence-composition layer is a reporting/decision-support boundary only. Descriptive direction and inferential detection remain separate, statistical difference direction is explicit, and lineage is preserved. New automated decisions or actions require a dedicated policy/design gate.


## D-124 — Economic Estimates and Realized Outcomes Remain Separate

Expected economics remain immutable estimate evidence. Realized revenue, cost, and effort are recorded as separate business-scoped outcomes. Derived variances are actual minus expected; this boundary does not score, forecast, allocate capital, mutate policy, or execute financial actions.


## D-125 — Economic Performance Aggregation Remains a Derived Evidence View

Economic performance aggregation uses explicit windows and preserves raw outcome lineage. Missing windows remain absent rather than zero-filled. Aggregation does not score businesses, forecast outcomes, allocate capital, mutate policy, or execute financial actions.


## D-126 — Economic Health and Stability Are Descriptive Evidence

V1 economic health/stability evidence exposes profitability and profit variability metrics from realized outcomes. It must not collapse them into a universal score, automatic business posture, forecast, capital allocation, policy mutation, or financial execution.


## D-127 — Economic Health Evidence Requires an Explicit Window

Economic health/stability evidence must be computed over an explicit start-inclusive/end-exclusive window and preserve that window. This prevents implicit all-history comparisons and keeps the evidence boundary deterministic.


## D-128 — Stable Profitability Is an Explicit Policy Eligibility Result

Stable profitability is assessed from economic-health evidence using explicit policy thresholds for observation sufficiency, profitable-outcome rate, average profit, and profit variability. The result is explainable eligibility evidence, not a universal score or automatic portfolio posture.


## D-129 — Economic Numeric Inputs Must Be Finite

Economic estimates and realized outcomes must reject NaN and infinite numeric inputs. Derived economic evidence must never be allowed to propagate non-finite source values.


## D-130 — Economic Stability Evidence Remains Explicitly Composed

Economic health metrics and stability-policy eligibility are composed into one evidence artifact while preserving their semantic distinction. The consumer must not create a universal score, portfolio posture, capital allocation, forecast, policy mutation, or financial execution action.


## D-146 — Opportunity Cost Is Evidence, Not Allocation [consolidated legacy duplicate of D-122]

The first opportunity-cost capability represents the foregone expected economic value of an alternative use of constrained capacity. It must not rank alternatives or silently decide resource allocation.


## D-147 — Evidence Handoff Does Not Authorize Action [consolidated legacy duplicate of D-122]

Decision-support evidence may be handed to policy review only when context is valid. The handoff preserves evidence lineage and posture and never authorizes execution or mutates policy.


## D-131 — Evidence Handoff Preserves Full Context and Requires Explicit Policy Review

A valid evidence handoff preserves descriptive direction, inferential status, posture, and current/baseline/statistical observation lineage. Valid evidence is marked as requiring explicit policy review; context-invalid evidence is blocked. The handoff never authorizes action or execution.


## D-132 — Policy Review Is Explicit and Non-Executing

Evidence policy review evaluates supplied evidence against an explicit immutable policy and returns a deterministic policy status/reason without authorizing or executing an action. Policy identity/configuration is caller-supplied; no default policy, automatic policy selection, ranking, recommendation, or mutation is introduced.


## D-133 — Authorization Is Separate From Execution and Bounded by Explicit Autonomy

Authorization requires a policy-satisfied review, preserves policy identity/version and autonomy bounds, and returns an explicit authorization status. L3 requires human approval. Irreversible external and financial actions are safety-blocked by this V1 domain boundary. No execution or external side effect occurs.


## D-134 — Execution Preparation Is Separate From Execution

An authorized action may produce a prepared execution request carrying explicit request identity, idempotency key, action class, autonomy, and policy identity/version. Preparation does not execute, enqueue, schedule, or cause an external side effect. Only authorized actions may cross this boundary.


## D-135 — Execution Outcomes Are Provider-Independent Evidence

Execution outcomes record what an external adapter reports for a prepared request. Unknown outcomes remain explicit, request identity and idempotency are preserved, and recording an outcome does not authorize, retry, compensate, bill, mutate policy, or execute further actions.


## D-136 — Execution Outcome Assessment Is Non-Executing

Execution outcomes are classified by explicit policy into accepted, retry-eligible, manual-review-required, or terminal failure. Retry eligibility never authorizes or performs a retry; request identity and idempotency remain preserved, and execution orchestration remains outside the domain.


## D-137 — Recovery Handoff Does Not Execute Recovery

Execution-outcome policy may produce a retry-eligible or manual-review assessment. A separate recovery handoff can preserve that intent, but it never schedules, retries, compensates, authorizes, or performs an external action.


## D-148 — Statistical Direction Requires Eligible Inferential Evidence [consolidated legacy duplicate of D-122]

A downstream performance evidence artifact may expose statistical direction only when the statistical evidence is eligible. Ineligible or unavailable statistical evidence must preserve raw lineage but expose no inferential direction.


## D-149 — Provider Execution Is an Application Adapter Boundary [consolidated legacy duplicate of D-124]

External execution is reached only through an explicit application-layer port after authorization has produced a prepared request. The port cannot authorize, retry, schedule, or mutate policy; provider-specific credentials and integrations remain outside the domain.


## D-138 — Execution Adapter Results Must Be Runtime-Validated

The execution adapter port rejects results that are not the explicit immutable ProviderExecutionResult contract and rejects invalid status/timestamp types before translating them into ExecutionOutcome. Runtime validation does not authorize, retry, schedule, compensate, or execute.


## D-139 — Execution Adapter Observation Times Must Be Timezone-Aware

Provider execution results must carry timezone-aware observation timestamps. This prevents ambiguous execution evidence at the adapter boundary without introducing provider-specific behavior or authorization/execution policy.


## D-150 — Execution Coordination Is Non-Executing Application Composition [consolidated legacy duplicate of D-122]

The coordinator composes existing authorization/request, provider execution, outcome policy, and recovery artifacts. It does not own provider selection, retries, scheduling, compensation, authorization, or policy mutation. External side effects remain behind the ExecutionPort implementation.


## D-151 — Execution Attempts Are Immutable Evidence [consolidated legacy duplicate of D-122]

Repeated provider execution attempts are preserved as explicit evidence with request identity, idempotency identity, and attempt number. The attempt history does not infer retry policy or perform scheduling/execution.


## D-152 — Execution Attempt History Consistency Does Not Infer Missing Attempts [consolidated legacy duplicate of D-125]

Execution history consistency validates identity and latest observed attempt agreement. Attempt numbers are explicit evidence; gaps are not treated as implicit failures or retries. The consistency boundary remains non-executing and non-authorizing.


## D-153 — Execution Retry Policy Must Consume Consistent Attempt Evidence [consolidated legacy duplicate of D-124]

Retry eligibility must not be derived from a caller-supplied attempt count when immutable execution history is available. Outcome/history identity and latest-attempt consistency are required before policy assessment; the policy remains non-executing.


## D-154 — Recovery Handoff Requires Consistent Attempt Evidence [consolidated legacy duplicate of D-138]

Recovery intent must be derived from the history-consistent execution policy assessment. Immutable attempt history is authoritative for observed attempt count; inconsistent history blocks recovery handoff creation. The boundary remains non-executing and non-authorizing.


## D-140 — Immutable Attempt History Is Authoritative During Execution Coordination

The history-aware coordinator derives the next attempt number from immutable execution history, records the provider outcome as an explicit attempt, and performs policy/recovery assessment only after history consistency is established. Callers must not provide a separate attempt count for this boundary. No retry, scheduling, authorization, compensation, or external side effect is introduced.


## D-155 — History-Aware Coordination Results Use Concrete Domain Types [consolidated legacy duplicate of D-122]

The history-aware coordination boundary must expose concrete provider-independent result types rather than generic object values. This is a type-safety hardening only; it does not authorize, retry, schedule, compensate, or execute additional actions.


## D-141 — Execution Retry Orchestration Requires an Explicit Scheduling Boundary

Retry orchestration must remain outside the domain policy layer. Any future scheduler/worker implementation must consume history-consistent recovery handoffs, preserve authorization and idempotency, revalidate before external execution, and define durable/concurrency semantics before implementation.


## D-142 — Retry Orchestration Requires Durable Identity and Pre-Execution Revalidation

**Status:** COMMITTED

Retry orchestration must use durable command identity and idempotency semantics, preserve immutable execution-attempt history, and revalidate authorization/policy immediately before an external retry. Stale authorization, stale policy/autonomy context, ambiguous scheduler state, duplicate scheduling, and concurrent claims must remain explicit and non-executing until reconciled. Runtime scheduler/worker implementation requires a separate persistence and scheduler boundary.


## D-143 — Retry Orchestration Requires Separate Durable Persistence and Scheduler Ports

Runtime retry orchestration requires replaceable persistence and scheduler ports before a concrete adapter is introduced. Durable command identity is the deduplication anchor; atomic claiming prevents concurrent duplicate execution; scheduler ambiguity remains explicit infrastructure evidence; authorization and retry policy are revalidated immediately before external execution.


## D-144 — Retry Command Identity Is Explicit and Provider-Independent

Retry orchestration commands preserve request identity, provider idempotency identity, attempt identity, authorization context, and command identity as explicit immutable evidence. Persistence and scheduler implementations remain replaceable ports; command contracts do not perform execution.


## D-156 — Performance Evidence States Are Non-Decisioning [consolidated legacy duplicate of D-122]

The performance evidence policy state is an evidence classification for downstream consumers. It must not be interpreted as an automatic recommendation or execution instruction, and it preserves insufficient inference and descriptive/inferential disagreement explicitly.


## D-157 — Retry Orchestration Runtime-Neutral Boundary Is Implemented [consolidated legacy duplicate of D-122]

The retry orchestration application boundary may coordinate durable command identity, atomic claiming through a port, authorization revalidation, scheduler acknowledgements, and explicit failure states. Concrete persistence, scheduler/queue, worker, retry-loop, and provider adapters remain outside the current boundary.


## D-158 — Retry Command Persistence Uses a Replaceable SQLite Adapter in V1 [consolidated legacy duplicate of D-122]

The first concrete retry persistence adapter uses standard-library SQLite behind the existing RetryCommandStore port. Durable logical identity and atomic claim semantics are infrastructure guarantees; retry policy and provider execution remain outside the adapter.


## D-145 — Durable Retry Scheduling Remains an Adapter Boundary

The SQLite retry scheduler persists logical scheduling identity and returns explicit scheduler acknowledgements. Identity conflicts and concurrency/lock outcomes remain explicit infrastructure evidence; the scheduler does not execute workers or providers and does not authorize retries.


## D-159 — Retry Execution Claim Is Separate From Execution [consolidated legacy duplicate of D-122]

A scheduled retry command may transition to EXECUTION_IN_PROGRESS through an explicit claim and produce a provider-independent handoff. The claim does not imply provider execution, completion, or success. Persistence/race failures remain explicit and non-executing.


## D-160 — Retry Execution Outcomes Do Not Automatically Retry [consolidated legacy duplicate of D-123]

Observed retry execution outcomes are consumed only to close the current command state. Success is terminal completion; non-success is explicit manual review. Automatic retry, compensation, and subsequent scheduling remain outside this boundary.


## D-161 — Retry Worker Dispatch Remains a Single-Command Application Boundary [consolidated legacy duplicate of D-122]

Worker dispatch may consume one scheduled retry command through atomic claim, authorization revalidation, the existing ExecutionPort, and outcome handoff. It must not introduce a background loop, queue framework, provider selection, automatic retry, compensation, or authorization mutation.


## D-162 — Retry Provider Failures Enter Explicit Manual Review [consolidated legacy duplicate of D-124]

A provider exception after an execution claim must not silently leave the command unresolved. V1 attempts a manual-review transition. If persistence fails, the system reports the persistence failure without fabricating an outcome or performing automatic retry/compensation.

