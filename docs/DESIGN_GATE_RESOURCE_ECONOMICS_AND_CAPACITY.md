# Design Gate — Resource Economics & Capacity

## Status

**APPROVED — V1 domain direction**

This gate establishes the first explicit resource/capacity model required to turn business economics into operational economics.

## Problem

Expected profit is incomplete if the system does not know what scarce resources produce that profit.

The platform must distinguish:

- monetary resource cost
- resource consumption
- scarce capacity
- committed capacity
- reserved capacity
- remaining capacity
- capacity utilization

Human time is the first constrained capacity modeled in V1. Other resource-capacity models remain extensible but are not invented prematurely.

## V1 Decisions

### D-030 — Resource Usage Is Explicit

A resource consumption record represents:

- resource kind
- quantity consumed
- monetary unit cost

Total monetary cost is derived as:

**quantity × unit cost**

Resource usage is independent from a specific marketplace or provider.

### D-031 — Resource Kinds Are Explicit

V1 recognizes:

- HUMAN_TIME
- CAPABILITY_USAGE
- INFRASTRUCTURE
- COMMUNICATION
- MARKETPLACE_FEE
- REVIEW_TIME

These are cost categories, not provider identities.

### D-032 — Human Time Is the First Capacity Model

V1 capacity is expressed in hours for a defined period.

The model distinguishes:

- total capacity
- committed capacity
- reserved capacity
- remaining capacity
- utilization

### D-033 — Capacity Is Not Profit

Capacity availability is an operational constraint. It does not directly imply economic quality.

Economic evaluation may consume capacity information, but Economic Profile scores remain separate derived assessments.

## Ownership

**Resource Economics** owns resource consumption and monetary resource-cost calculation.

**Capacity** owns constrained availability and utilization.

**Business Economics** consumes resource economics when calculating expected cost/profit.

**Economic Health** consumes resulting metrics as evidence but does not own raw resource accounting.

## Boundary

This gate does not define:

- workforce scheduling
- calendar integration
- task assignment
- payroll
- provider billing reconciliation
- portfolio allocation
- automatic capital movement
- multi-resource optimization
- final opportunity-selection policy

## TDD Slice

1. Resource usage validates non-negative quantity and unit cost.
2. Resource usage calculates total cost.
3. Resource kinds are explicit.
4. Capacity validates its period and non-negative hour inputs.
5. Capacity calculates remaining hours.
6. Capacity calculates utilization.
7. Capacity cannot report negative remaining capacity.
8. Resource economics remains independent from external providers.

## Trade-offs

### Generic resource records vs fixed cost fields

**Chosen:** explicit resource kinds plus quantity/unit cost.

This avoids growing constructor fields whenever a new resource category appears while keeping the categories controlled and explainable.

### Full scheduling vs capacity snapshot

**Chosen:** capacity snapshot.

Scheduling is a separate problem. V1 needs enough information to reason about scarcity without prematurely introducing calendars, assignments, or scheduling infrastructure.

### One master economic score

**Rejected:** resource/capacity information must not be collapsed into a universal economic score.

## Open Questions

- How capacity periods are generated from actual availability.
- Whether capacity should support multiple currencies.
- How resource costs are normalized across currencies.
- How actual resource usage is captured.
- How capacity reservations interact with execution lifecycle.
- How opportunity cost is calculated from scarce capacity.
- How capacity feeds future portfolio posture policies.

## Gate Exit Criteria

This gate is closed for the domain foundation. Implementation can proceed with domain-only TDD while the open questions remain explicit.
