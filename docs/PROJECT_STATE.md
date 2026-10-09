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

Criterion-level evidence and uncertainty are preserved. Overall outcomes are QUALIFIED, NOT_QUALIFIED, or REVIEW_REQUIRED. The obsolete parallel opportunity-evaluation semantic owner has been removed; the canonical Opportunity Intelligence contracts are the sole evaluation surface.

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

**Descriptive Evidence + Statistical Evidence → Evidence Composition → Evidence Review Handoff → Policy Review → Authorization → Execution Preparation → Execution → Outcome / Recovery Evidence**

Decision-support remains non-executing. It does not create universal scores, rankings, automatic portfolio actions, policy mutation, or external side effects.

Descriptive change, metric favorability, and statistical detection remain separate. Favorability requires explicit metric-direction policy; statistical detection does not establish whether a change is favorable. Disagreement is preserved rather than hidden.

The evidence review handoff is an explicit non-authorizing boundary: eligible composed evidence may be handed to policy review, while unavailable or context-invalid evidence remains not ready.

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

The Opportunity Intelligence semantic foundation is implemented: immutable `EvaluationContext`, provider-independent evidence metadata and quality states, explicit applicability, and lineage-preserving evidence snapshots. **Eligibility V1, Requirement Fit V1, Estimated Effort V1, Economic Fit V1, Client / Project Risk V1, and Success Confidence V1 are implemented, merged, and completion-verified.**

**Opportunity Prioritization V1** (D-231) is implemented via PRs #487 and #488. **Opportunity Decision Pipeline V1** is implemented and merged via PR #489 (merge commit `e2192e0304b99c403cfea9c7ab862d1523998521`). The pipeline composes evaluation and prioritization for one normalized opportunity and returns an immutable result; it does not persist data, perform provider I/O, rank batches, authorize, or execute. Reference freshness validation remains deferred until an authoritative registry exists.

**Opportunity History & Persistence V1** (D-233) is now implemented and merged. PR #490 merged the approved design/repository contract (merge commit `3f7eeed5428f881491be67567300693d9865c186`). PR #491 merged the versioned canonical codec, provider-neutral repository port, immutable revision/decision record types, in-memory reference adapter, and application service that evaluates the exact persisted revision before recording a decision (merge commit `c16eb2cecb833c58447da0facf7528d7100aad68`). CI passed on the final PR #491 head `c35184b4b28e3cb1ae67c3d31e6119131eb06d2c` (run [37864333083](https://github.com/palestiny/freelancer-automation-platform/actions/runs/37864333083)); a separate post-merge workflow run has not been confirmed.

The in-memory adapter is a reference/conformance implementation only: it does not claim crash durability, multi-process linearizability, or distributed locking. No production database has been selected. The current pipeline result does not carry the full `EvaluationContext`, original `Evidence` payloads/provenance/quality, or applicability map, so persistence does not claim to preserve absent data. API/UI, provider integration, evidence registry/freshness, production persistence, batch ranking, authorization, bidding, messaging, and execution remain outside this slice.
## Documentation Integrity Rule

This file is the canonical current-state summary. Historical implementation details belong in the decision log and dedicated design gates, not as repeated chronological appendices here.

## Completion Rule

A meaningful increment is complete only after applicable design, RED/GREEN TDD, hardening/refactoring, documentation reconciliation, passing CI, commit/merge, and verified project state.

## Canonical Current-State Rule

This document intentionally contains one current-state summary. Historical slices, duplicate reconciliation notes, and implementation chronology belong in the decision log and dedicated design gates.

## Performance Evidence Decision Support

The platform now has a bounded downstream evidence-composition layer that combines deterministic performance trend direction with the existing eligible statistical evidence artifact. It preserves disagreement explicitly and does not produce a business decision, score, ranking, policy mutation, learning mutation, portfolio action, or execution.
