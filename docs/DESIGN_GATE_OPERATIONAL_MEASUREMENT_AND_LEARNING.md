# Design Gate — Operational Measurement & Learning

**Status:** APPROVED — V1 domain direction committed; provider-independent operational measurement and learning foundation implemented.

## Purpose

Connect repeatable business operations to the platform learning loop:

**Business → Operational Cycle → Work Item → Outcome Observation → Measurement → Variance → Learning Signal → Explicit Improvement Handoff**

The goal is to make operational performance measurable without turning observations into automatic policy changes.

## V1 Decisions

### D-062 — Operational Outcomes Are First-Class Observations

A completed or failed work item may produce an explicit outcome observation. The observation records what happened; it does not itself decide what policy should change.

### D-063 — Expected and Actual Values Remain Separate

Operational measurements preserve expected and actual values and derive variance from them. Forecasts and estimates must not be overwritten by observed results.

### D-064 — Learning Signals Are Evidence, Not Policy

A learning signal summarizes evidence from operational observations and measurements. It does not silently mutate business policy, economics, workflow, or lifecycle state.

### D-065 — Improvement Requires an Explicit Handoff

An improvement recommendation must explicitly hand off to either policy review or controlled experimentation. The recommendation is not execution.

### D-066 — Operational Measurement Is Provider-Independent

The domain owns measurement meaning. Schedulers, workers, task systems, marketplaces, communication providers, payment systems, databases, and AI providers remain outside the domain boundary.

### D-067 — Business Isolation Applies to Measurement

Operational observations, measurements, learning signals, and recommendations belong to an explicit business context. Cross-business contamination is invalid.

## V1 Domain Flow

**Work Item → Outcome Observation → Operational Measurement → Variance → Learning Signal → Improvement Recommendation → Policy Review / Experiment**

## Domain Objects

### WorkItemOutcomeObservation

Records an observed result for a work item:

- identity
- business ownership
- work-item ownership
- observation timestamp
- outcome status
- evidence quality

### OperationalMeasurement

Represents one measurable expected-vs-actual value:

- business ownership
- metric name
- unit
- expected value
- actual value
- measurement timestamp

Variance is derived as:

**actual − expected**

Relative variance is derived when the expected value is non-zero.

### BusinessPerformanceSnapshot

Represents a business-level measurement snapshot composed of operational measurements for one business and period.

It is an observation container, not a business-state mutation mechanism.

### LearningSignal

Represents a derived learning statement supported by observed evidence.

It contains:

- business ownership
- source measurement/observation reference
- statement
- evidence quality

### ImprovementRecommendation

Represents a proposed improvement handoff.

V1 handoff types:

- POLICY_REVIEW
- EXPERIMENT

The recommendation must not execute either handoff.

## Evidence Rules

- Outcome observations are observations.
- Expected values may originate from estimates, plans, or hypotheses.
- Actual values are observed results.
- Variance is derived data.
- Learning signals are derived evidence.
- Recommendations are proposals.
- No object silently upgrades evidence certainty.
- No learning signal automatically changes policy.

## Safety / Boundary

This gate does not introduce:

- scheduling
- workers/queues
- persistence
- HTTP/API
- dashboards
- provider integrations
- AI model selection
- automatic policy mutation
- automatic experiment execution
- financial execution
- automatic capital movement

Those remain explicit future capability boundaries.

## Acceptance Criteria

1. Work outcomes can be recorded without coupling to execution infrastructure.
2. Expected and actual values remain independently observable.
3. Variance is deterministic and testable.
4. Business ownership is explicit.
5. Learning is derived from evidence and does not mutate policy.
6. Improvement recommendations require an explicit policy-review or experiment handoff.
7. Domain tests cover valid states and invalid cross-boundary states.


## Evidence Quality Follow-up

Operational measurements now carry explicit bounded evidence quality. Repeated-variance learning derives the learning signal's evidence quality from the average quality of its contributing measurements rather than using a neutral constant.

This keeps learning evidence-aware while leaving richer provenance and evidence aggregation policy as future work.
