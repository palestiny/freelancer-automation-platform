Design Gate — Business Operations & Multi-Business Execution

Status: APPROVED — V1 domain direction committed; provider-independent business operating foundation implemented.

Purpose: connect validated business models to repeatable operations without coupling the domain to task schedulers, providers, payment systems, or AI.

Flow: Business → Operating Plan → Operational Cycle → Work Item → Outcome Observation → Measurement / Learning

Decisions:
- D-057 Business is a first-class domain entity.
- D-058 Operations are separate from business identity.
- D-059 Work is provider-independent.
- D-060 Multi-business isolation is explicit: each cycle and work item belongs to exactly one business.
- D-061 Operations produce evidence and do not silently rewrite economics, policy, or business state.

V1 Business lifecycle: PLANNING → VALIDATING → OPERATING, with PAUSED and CLOSED states.
V1 operational cycle states: PLANNED, RUNNING, COMPLETED, CANCELLED.
V1 work states: PENDING, IN_PROGRESS, COMPLETED, FAILED, CANCELLED.

Boundary: no scheduling, queues/workers, provider credentials, marketplace/social/ad APIs, payment execution, automatic capital allocation, AI model selection, or cross-business resource optimization.

Non-goals: workflow orchestration, task assignment algorithms, calendars, billing reconciliation, portfolio allocation, automatic business lifecycle decisions.
