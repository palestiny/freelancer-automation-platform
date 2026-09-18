# Design Gate — Business Performance History

**Status:** APPROVED — V1 domain direction committed; normalized business performance history foundation implemented.

## Purpose

Create the bounded bridge that lets the platform reason about business performance across operational, revenue, and campaign observations without collapsing those source domains into one model.

**Source Domain Observation → Normalized Business Performance Observation → Business Performance History → Metric/Variance Analysis → Learning**

## V1 Decisions

### D-068 — Business Performance History Is a Normalized Evidence View

Business Performance History is a derived, provider-independent view over bounded observations. It does not replace the source domain that produced an observation.

### D-069 — Source Identity Is Preserved

Every normalized performance observation identifies its source type and source identifier. Normalization must not erase provenance.

### D-070 — Expected Values May Be Absent

An actual observation may be recorded without an expected value. The platform must not invent an expectation merely to calculate variance.

### D-071 — Business Isolation Is Mandatory

A performance history belongs to exactly one business. Cross-business observations cannot be combined.

### D-072 — History Does Not Mutate Source Domains

Adding or organizing performance observations must not mutate operational state, revenue contracts/events, campaign state, economic profiles, or business lifecycle state.

### D-073 — Aggregation Policy Remains Separate

Ordering, metric filtering, windows, baselines, thresholds, and future statistical methods remain changeable policy. V1 provides only deterministic history organization and per-observation variance.

## V1 Domain Objects

### BusinessPerformanceObservation

A normalized evidence record containing:

- business ownership
- source type
- source identifier
- metric name
- unit
- optional expected value
- actual value
- observation timestamp
- evidence quality

Derived values:

- variance = actual − expected, when expected exists
- relative variance, when expected is non-zero

### BusinessPerformanceHistory

A business-scoped collection of normalized observations.

V1 provides:

- business-isolation validation
- chronological ordering
- metric/unit filtering
- latest-observation access

## Source Boundary

The history model does not directly import or depend on RevenueContract, RevenueEvent, MarketingCampaign, campaign providers, operational infrastructure, or external APIs.

Application/domain mapping may later convert source-specific observations into normalized performance observations.

## Evidence Rules

- Source observations remain attributable to their origin.
- Actual values remain observations.
- Expected values remain separate from actual values.
- Missing expected values remain missing.
- Variance is derived data, not a new observation.
- Evidence quality is carried forward explicitly.
- History is a view/container, not a policy decision.

## Safety / Non-Goals

V1 does not implement:

- persistence
- API/UI
- scheduling
- statistical inference
- attribution modeling
- automatic policy mutation
- automatic experiment execution
- financial execution
- capital allocation
- cross-business aggregation
- provider integrations
- AI model selection

## Acceptance Criteria

1. A normalized observation preserves business and source identity.
2. Variance is deterministic when an expected value exists.
3. No variance is invented when expected value is absent or zero.
4. A history rejects cross-business observations.
5. History can order observations chronologically.
6. History can filter by metric and unit.
7. Source domains remain independent from the history model.
8. Tests cover the safety and evidence boundaries.


## Time-Window Foundation

V1 now includes a deterministic `PerformanceWindow` with start-inclusive/end-exclusive semantics, plus helpers for selecting observations inside a window and constructing a rolling window from an explicit end time and duration.

Time windows are selection primitives only. They do not imply business-period aggregation, trend inference, or policy decisions.