# Project State

## Current Status

**Current delivery boundary: Progressive Autonomy → Execution Runtime → Recovery Coordination**

The repository has completed provider-independent foundations for opportunity intelligence, economics, market intelligence, venture validation, revenue, communication, marketing, business operations, deterministic measurement/learning, bounded statistical inference, evidence composition, policy review, authorization, execution preparation, execution outcomes, recovery assessment, execution coordination, immutable attempt history, retry policy, durable retry persistence/scheduling, execution claims, retry outcomes, and single-command worker dispatch.

The latest merged runtime work includes bounded retry execution, continuous single-worker lifecycle semantics, crash/recovery reconciliation, provider-status observation, deterministic reconciliation assessment, atomic expected-state state application, and single-observation recovery coordination. A background daemon/queue framework, distributed workers, and automatic re-execution are not implemented.

## Current Product Direction

The platform is an **Economic Opportunity OS / Business Automation OS**.

Freelancing is the first laboratory, not the permanent architectural boundary.

**Discover → Evaluate → Validate → Build → Market → Sell → Operate → Measure → Learn → Experiment → Scale / Kill → Portfolio**

The architecture remains a modular monolith with provider-independent domain contracts and replaceable adapters.

## Architecture Rules

- AI is a replaceable capability, not the domain owner.
- Marketplace, marketing, payment, execution, persistence, and infrastructure integrations remain replaceable adapters/ports.
- External observations, normalized evidence, derived analysis, hypotheses, decisions, authorization, and execution outcomes remain separate semantic layers.
- Learning produces evidence/recommendations; it does not silently mutate policy.
- Authorization is separate from execution.
- Execution preparation is separate from execution.
- Execution outcomes are observations, not automatic retry instructions.
- Retry policy is separate from retry orchestration.
- Retry orchestration is separate from provider execution.
- Financial execution and automatic capital movement remain outside the current product boundary.

## Opportunity Intelligence

The applicable six dimensions remain:
1. Eligibility
2. Requirement Fit
3. Estimated Effort
4. Economic Fit
5. Client / Project Risk
6. Success Confidence

Criterion-level evidence and uncertainty are preserved. Overall outcomes are QUALIFIED, NOT_QUALIFIED, or REVIEW_REQUIRED.

## Economic Model

Economic quality remains multidimensional rather than a universal master score:
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

Expected economics and realized outcomes remain separate. Economic evidence is explicit-window, lineage-preserving, and non-executing.

## Evidence & Measurement

The epistemic taxonomy remains:

**FACT → OBSERVATION → ESTIMATE → ASSUMPTION → HYPOTHESIS → FORECAST → EXPERIMENT_RESULT**

Operational evidence preserves business ownership, metric/unit identity, explicit windows, expected-vs-actual values, source identity/provenance, observation lineage, evidence quality, and optional source reliability.

Deterministic trend/baseline comparison is separate from statistical inference.

## Statistical Surface

Phase 17 is closed for the current V1 statistical-method boundary.

Implemented:
- Student's t mean uncertainty
- Welch's two-sample historical mean comparison
- explicit applicability and validation precedence
- standard-library numerical implementation
- unique observation lineage
- statistical evidence composition

No additional statistical method is currently authorized without a concrete consumer/use case and dedicated design gate.

## Decision-Support Surface

The current evidence pipeline is:

**Descriptive Evidence + Statistical Evidence → Evidence Composition → Evidence Handoff → Policy Review → Authorization → Execution Preparation → Execution → Outcome / Recovery Evidence**

Decision-support remains non-executing. It does not create universal scores, rankings, automatic portfolio actions, policy mutation, or external side effects.

Descriptive direction and inferential detection remain separate. Disagreement is preserved rather than hidden.

## Execution & Retry Surface

The current runtime-neutral execution boundary includes:
- prepared authorized execution requests
- provider-independent execution outcomes
- outcome policy assessment
- recovery handoffs
- application-layer ExecutionPort
- execution coordination
- immutable execution-attempt history
- history-consistent retry assessment
- retry command identity
- replaceable durable retry persistence
- replaceable durable retry scheduling
- atomic execution claim
- retry outcome handoff
- single-command worker dispatch
- provider failure → manual review

The latest approved boundary is a **single-worker recovery-aware runtime** with explicit lifecycle and reconciliation semantics. It is not a background service, queue framework, distributed worker system, or automatic-reexecution engine.

## Current Domain / Infrastructure Boundary

Implemented:
- domain models, value objects, policies, evidence artifacts, and tests
- application-layer execution coordination/ports
- concrete SQLite retry persistence/scheduling adapters
- bounded single-command worker dispatch
- explicit runtime-loop design contract
- finite retry worker runtime invocation
- deterministic SQLite scheduled-work source
- immutable retry runtime invocation observations

Still outside the current boundary:
- real marketplace/provider integrations and credentials
- UI/dashboard
- production background daemon/queue infrastructure
- distributed leases/worker pools
- automatic retry beyond the explicitly designed runtime loop
- payment execution
- automatic capital movement
- portfolio allocation execution
- AI provider selection/execution policy
- cross-business resource optimization

## Current Next Engineering Boundary

The continuous single-worker lifecycle and crash/recovery reconciliation boundaries are implemented and observable. Provider-status observation, deterministic assessment, atomic state application, and single-observation coordination are also implemented. No distributed worker, automatic restart, polling loop, or automatic re-execution semantics are implied.

## Documentation Integrity Rule

This file is the canonical current-state summary. Historical implementation details belong in the decision log and dedicated design gates, not as repeated chronological appendices here.

## Completion Rule

A meaningful increment is complete only after applicable design, RED/GREEN TDD, hardening/refactoring, documentation reconciliation, passing CI, commit/merge, and verified project state.


## Canonical Implemented Cross-Cutting Boundaries

The current state is summarized by the sections above. Completed cross-cutting slices include evidence composition/review, policy evaluation and authorization lineage, prepared-request freshness, provider adapter/capability/credential boundaries, performance observation persistence, controlled-experiment evidence persistence/idempotency, execution outcome persistence, and the bounded retry/recovery runtime.

The canonical runtime pipeline is:

**Evidence → Policy Review → Authorization → Preparation → Freshness → Capability/Credential Checks → Provider Execution Port → Outcome Observation → Recovery Assessment → Atomic State Application → Learning / Review Evidence**

Completed lifecycle/recovery boundaries must not be reopened without a new requirement. The next engineering increment must be selected from an unresolved product or infrastructure requirement and governed by a dedicated design gate.

## Persisted Execution Coordination

The execution runtime now has an explicit persisted-coordination application boundary: provider outcome → durable outcome evidence → policy assessment → recovery handoff. Provider and persistence failures remain explicit and do not fabricate recovery state.


## Current Evidence Interpretation Boundaries

Metric movement remains neutral evidence. Explicit metric polarity policy may interpret movement as FAVORABLE, UNFAVORABLE, or NEUTRAL; missing policy yields NOT_INTERPRETABLE. This interpretation does not create a score, recommendation, lifecycle mutation, learning mutation, portfolio action, or execution.

Controlled experimentation currently preserves explicit assignment, exposure, observation, linkage, lineage, temporal, authority, and retry/idempotency boundaries. Experiment evidence does not imply causality, variant selection, allocation optimization, lifecycle mutation, authorization, or execution.


## Performance Evidence Decision Support

The platform now has a bounded downstream evidence-composition layer that combines deterministic performance trend direction with the existing eligible statistical evidence artifact. It preserves disagreement explicitly and does not produce a business decision, score, ranking, policy mutation, learning mutation, portfolio action, or execution.


## Statistical Direction Provenance Hardening

The performance evidence decision-support boundary now preserves the Welch mean difference explicitly and derives statistical direction from that preserved value. A statistically detected difference that conflicts with the descriptive movement is represented as an explicit conflict posture rather than being treated as aligned evidence.
## Performance Evidence Decision Support

The platform now has a bounded downstream evidence-composition layer that combines deterministic performance trend direction with the existing eligible statistical evidence artifact. It preserves disagreement explicitly and does not produce a business decision, score, ranking, policy mutation, learning mutation, portfolio action, or execution.


## Performance Evidence Decision Support


## Performance Evidence Decision Support

A bounded downstream evidence-composition layer now combines deterministic performance trend direction with the existing eligible statistical evidence artifact. It preserves disagreement explicitly and does not produce a business decision, score, ranking, policy mutation, learning mutation, portfolio action, or execution.


## Performance Evidence Posture Hardening

The current evidence decision-support value object now enforces that available inferential evidence preserves its statistical method and comparison windows. A detected statistical difference must preserve an explicit direction; an aligned posture requires matching descriptive and statistical directions, while a conflict posture requires opposite directions. This is contract hardening only and does not add new statistical methods or decision authority.


## Performance Evidence Decision Support

A bounded downstream evidence-composition layer now combines deterministic performance trend direction with the existing eligible statistical evidence artifact. It preserves disagreement explicitly and does not produce a business decision, score, ranking, policy mutation, learning mutation, portfolio action, or execution.


## Performance Evidence Decision Support

The platform now has a bounded downstream evidence-composition layer that combines deterministic performance trend direction with the existing eligible statistical evidence artifact. It preserves disagreement explicitly and does not produce a business decision, score, ranking, policy mutation, learning mutation, portfolio action, or execution.


## Performance Evidence Decision Support

A bounded downstream evidence-composition layer now combines deterministic performance trend direction with the existing eligible statistical evidence artifact. It preserves disagreement explicitly and does not produce a business decision, score, ranking, policy mutation, learning mutation, portfolio action, or execution.
