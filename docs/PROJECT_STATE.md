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


## Performance Evidence Decision Support

The platform now has a bounded downstream evidence-composition layer that combines deterministic performance trend direction with the existing eligible statistical evidence artifact. It preserves disagreement explicitly and does not produce a business decision, score, ranking, policy mutation, learning mutation, portfolio action, or execution.


## Next Engineering Boundary — Retry Worker Lifecycle

The finite retry-worker runtime boundary is implemented. The next approved design boundary is continuous runtime lifecycle semantics: explicit start/stop states, safe shutdown, single-worker concurrency, crash/recovery reconciliation, and lifecycle observability. Continuous runtime implementation must follow a dedicated TDD increment and must not introduce a daemon or queue framework implicitly.


## Retry Worker Lifecycle — Current State

The approved continuous-runtime lifecycle increment is implemented at the application boundary. The lifecycle controller has explicit STARTING/RUNNING/STOPPING/STOPPED/STOPPED_WITH_ERROR states, explicit stop semantics, wake-up waiting, and bounded failure termination around the authoritative single-command invocation. Immutable lifecycle observations preserve runtime identity, timestamps, final state, stop reason, and transitions.

Still outside the boundary: automatic restart, distributed workers, worker pools, leases/heartbeats, queue framework selection, crash-recovery reconciliation for in-flight provider execution, and external metrics/alerting infrastructure.


## Next Engineering Boundary — Crash / Recovery Reconciliation

A dedicated design gate defines the provider-independent reconciliation boundary for ambiguous in-flight retry commands. The next implementation must preserve unknown outcomes, immutable attempt lineage, request/idempotency identity, and explicit manual reconciliation without automatic re-execution.


## Retry Worker Crash / Recovery Reconciliation — Current State

The approved provider-independent crash/recovery reconciliation boundary is implemented. Ambiguous in-flight retry commands remain explicitly manual-review-only; terminal commands are not reopened; command/request/idempotency identity and attempt number are preserved; duplicate reconciliation is non-executing.

Still outside this boundary: provider-status polling, automatic re-execution, automatic retry scheduling, distributed recovery, leases/heartbeats, automatic restart, and capital/portfolio actions.


## Provider Execution Status Observation

The execution runtime now exposes a provider-independent, non-executing status-observation port for ambiguous execution recovery. It preserves request/idempotency identity and timezone-aware observation evidence. It does not authorize, retry, schedule, poll continuously, mutate durable retry state, or execute provider actions.


## Retry Status Reconciliation Assessment

A provider status observation can now be consumed with a durable retry command to produce a deterministic, non-mutating recovery assessment. Confirmed success can be identified as completion; confirmed failure/rejection requires manual review; unknown remains ambiguous; terminal commands are never reopened. Applying the assessment to durable state remains a separate boundary.


## Retry Status Assessment State Application

The retry recovery pipeline now has an explicit durable-state application boundary. A previously computed recovery assessment can transition a retry command only when the expected durable state still matches. The transition is atomic at the SQLite persistence boundary and preserves immutable command identity. Ambiguous and no-reconciliation assessments remain non-mutating; confirmed failure resolves to manual review rather than automatic retry.


## Retry Status Reconciliation Coordination

The provider-independent recovery path now has an explicit application coordinator: one status observation → deterministic assessment → atomic durable state application. Terminal commands are not re-observed; ambiguous outcomes remain unchanged; confirmed failure resolves to manual review. Polling, scheduling, automatic re-execution, and restart remain outside this boundary.


## Performance Evidence Decision Support — Current State

V1 includes a bounded downstream evidence-composition layer combining deterministic performance trend direction with the existing eligible statistical evidence artifact. It preserves disagreement explicitly and does not produce a score, ranking, business decision, policy mutation, learning mutation, portfolio action, or execution.


## Current Runtime State Reconciliation

The canonical runtime boundary now includes lifecycle control and recovery coordination. Older sections that describe lifecycle or crash/recovery as the next engineering boundary are historical and should not be treated as open work. The next unresolved implementation target should come from an explicitly unresolved product/infrastructure boundary rather than repeating completed runtime work.


## Evidence Review Handoff — Current State

V1 now has an explicit non-executing handoff from composed performance evidence to policy or human review. The handoff preserves descriptive/inferential evidence and observation lineage, but never authorizes or mutates policy or execution.


## Evidence Review Decision — Current State

V1 now represents an explicit review outcome after evidence handoff. ACCEPT, REJECT, and REQUEST_MORE_EVIDENCE are decision artifacts only; even ACCEPT is not authorization for policy mutation, provider execution, payment, capital movement, or external side effects. Reviewer identity, rationale, target, and observation lineage are preserved.


## Provider Adapter Conformance — Current State

The approved provider-adapter conformance boundary is implemented. A reusable non-executing validator now verifies provider execution result type, request identity, idempotency identity, and timezone-aware observation before the existing execution dispatch converts the result into the domain outcome. No provider call, authorization, retry, scheduling, or state mutation is introduced by the conformance layer.


## Provider Adapter Registry — Current State

V1 now provides explicit provider-key registration and resolution above the existing provider-independent execution port. Duplicate keys and unknown providers are rejected explicitly. The registry performs no provider ranking, fallback, credential management, health routing, or execution.


## Provider Capability Registry — Current State

V1 now declares provider capabilities explicitly and resolves them by provider key without executing providers. Capability metadata is provider-independent and non-ranking. Provider calls, credentials, health routing, fallback, and automatic capability selection remain outside this boundary.


## Capability-Aware Provider Dispatch — Current State

The execution boundary now verifies an explicitly declared provider capability before entering the existing authorized execution dispatch. Unsupported capabilities are rejected without invoking the adapter. Capability checks are preconditions, not authorization, and do not infer, rank, select fallback providers, or manage credentials.


## Statistical Evidence Lineage Hardening

The statistical evidence composition artifact now preserves the Welch comparison windows and mean difference alongside method identity and observation lineage. Existing evidence-quality and source-reliability eligibility semantics remain unchanged. The artifact remains non-executing and non-decisioning.


## Provider Credential Reference — Current State

V1 now has an opaque provider credential reference boundary. The domain can identify which provider credential should be resolved without carrying secret material. Secret storage, resolution, token refresh, rotation, and provider-specific authentication remain outside the domain.


## Provider Credential Resolution — Current State

The approved application/infrastructure credential-resolution boundary is implemented and CI-verified. Opaque provider credential references can now be resolved through a replaceable resolver port with explicit success/failure semantics and provider/reference binding. Credential material remains outside domain entities, no fallback or ranking is performed, and resolution does not authorize or execute provider actions.

Concrete secret stores, rotation, refresh, and provider-specific authentication remain infrastructure/integration concerns.


## Provider-Authenticated Execution Dispatch — Current State

V1 now composes explicit provider capability verification with explicit credential resolution and an authenticated adapter contract before provider execution. Credential material remains application/integration-only and is never copied into domain execution state. Authentication remains separate from authorization; no fallback, retry, credential lifecycle, provider selection, or secret persistence is introduced.


## Evidence-to-Decision Policy Boundary

A bounded provider-independent policy evaluator now sits after evidence composition. It accepts an explicit versionable policy and evidence eligibility/quality inputs and returns a decision-support outcome only: SUPPORTS, DOES_NOT_SUPPORT, INSUFFICIENT_EVIDENCE, or POLICY_INAPPLICABLE. It does not execute, mutate business lifecycle, portfolio state, learning policy, or external systems.


## Evidence-to-Decision Policy Lineage Hardening

Decision-support policy results now preserve explicit evidence identity and observation lineage alongside policy identity/version. The policy boundary remains non-executing and does not mutate policy, lifecycle, learning, portfolio, or execution state.


## Policy Identity Binding — Current State

The review-to-authorization boundary now preserves the exact policy ID/version used during evidence policy review. Authorization rejects mismatched policy identity or version, preventing a satisfied review from being rebound to a different policy context.


## Action Authorization Evidence Lineage

Authorization artifacts now preserve the exact current, baseline, and statistical observation IDs carried by the reviewed evidence. This strengthens traceability without changing authorization semantics or enabling execution.


## Prepared Execution Request Evidence Lineage

Prepared execution requests now preserve the current, baseline, and statistical observation IDs carried by the authoritative action authorization. This is traceability hardening only; preparation remains non-executing and does not add freshness, retry, scheduling, or provider behavior.


## Prepared Execution Request Freshness

A provider-independent freshness assessment now provides an explicit safety precondition for prepared execution requests. It uses the request preparation timestamp, an explicit versionable maximum-age policy, and an explicit as-of timestamp. Stale, missing, future, and non-prepared states remain explicit and non-mutating. Freshness does not re-authorize, retry, schedule, or execute a request.


## Performance Evidence Decision Support

A bounded downstream evidence-composition layer combines deterministic performance trend direction with the existing statistical evidence artifact. It preserves disagreement explicitly and does not produce a business decision, score, ranking, policy mutation, learning mutation, portfolio action, or execution.


## Freshness-Aware Provider-Authenticated Dispatch

V1 authenticated provider dispatch now requires an explicit prepared-request freshness policy and explicit as-of time after capability verification and before credential resolution/provider invocation. Stale, future, missing-timestamp, and non-prepared requests are rejected without provider execution. Freshness remains a safety precondition, not authorization, retry, scheduling, or re-authorization.


## Evidence → Learning Handoff

The platform now has an explicit non-executing handoff from eligible composed performance evidence to either policy review or experiment. The handoff preserves business/metric/unit identity and statistical observation lineage. It does not mutate policy, lifecycle, portfolio, or execution state.


## Business Learning Memory

V1 now has an immutable provider-independent business learning-memory artifact created only from eligible evidence-to-learning handoffs. It preserves business/metric/unit context, handoff category, statement, source handoff identity, observation lineage, explicit timestamp, and evidence quality. It does not persist, rank, score, infer causality, mutate policy, or execute actions.


## Learning Lineage Hardening

Evidence learning handoffs now carry an explicit immutable handoff identity. Business learning memory preserves that exact source handoff identity rather than substituting the memory entry ID. This closes the source-lineage gap without changing learning semantics.


## Performance Evidence Direction Semantics

Performance evidence production now uses neutral movement semantics: INCREASED, DECREASED, and NO_CHANGE. The evidence layer does not infer whether a movement is favorable or unfavorable because metric polarity varies by metric. Existing explicit policy consumers retain compatibility with legacy IMPROVING/DECLINING values during migration.


## Metric Direction Policy

V1 now separates neutral evidence movement from favorable/unfavorable interpretation. Metric polarity is an explicit provider-independent policy; raw evidence remains unchanged and missing polarity is not inferred from metric names.


## Metric Direction Interpretation

The existing metric-polarity policy is now explicitly consumed by performance evidence decision support. Raw movement remains neutral; favorable/unfavorable interpretation is consumer-provided policy and missing polarity remains not interpretable. No recommendation or execution semantics were added.


## Canonical Current Boundary Reconciliation — 2026-09-20

The previously labeled “Next Engineering Boundary — Retry Worker Lifecycle” and “Next Engineering Boundary — Crash / Recovery Reconciliation” sections are historical implementation notes. They are superseded by the implemented lifecycle, reconciliation, provider-status observation, atomic state application, and single-observation coordination boundaries documented above.

The current implementation boundary is now:

**Evidence → Policy Review → Authorization → Prepared Execution → Freshness → Capability/Credential Checks → Provider Execution Port → Outcome Observation → Recovery Assessment → Atomic State Application → Learning / Review Evidence**

The next unresolved product/infrastructure boundary is intentionally not selected by this state file. Candidate future boundaries remain concrete provider integrations, production persistence/API/UI integration, controlled experimentation infrastructure, production background runtime infrastructure, broader business-model execution, cross-domain learning, and progressive autonomy. Any selected boundary requires its own design gate and TDD increment.


## Performance Evidence Persistence

V1 authoritative performance observations now have a durable provider-independent application port and a reference SQLite adapter. Raw observations remain authoritative; aggregates, trends, statistical results, and learning artifacts remain derived and recomputable. Persistence does not interpret evidence or execute actions.


## Performance Observation Application Service

A provider-independent application service now sits above the performance observation repository port for recording authoritative observations and retrieving one business's history. It does not trigger derived analysis, policy evaluation, learning, authorization, or execution.


## Performance Observation Temporal Contract

Authoritative performance observations now require timezone-aware timestamps. This closes an ambiguity at the temporal domain boundary used by history, windows, freshness, baseline, trend, and statistical analysis. No implicit local-time/UTC inference or normalization is performed.


## Controlled Experiment Evidence

V1 now has provider-independent immutable experiment assignment and observation evidence. Assignments and observations preserve explicit experiment/subject/variant identity and timezone-aware timestamps. This boundary records evidence only; it does not randomize allocation, schedule work, execute providers, infer causality, calculate statistical significance, or mutate experiment lifecycle.
