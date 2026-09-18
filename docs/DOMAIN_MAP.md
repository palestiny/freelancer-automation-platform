# Domain Map

## Product Core

The platform is a **Business Automation OS** initially validated through the freelance-work domain.

Freelancing is the first market/use case, not the permanent architectural boundary.

## Core Domain Areas

### Opportunity Intelligence

Answers:

> What opportunities exist, what do we know about them, and how suitable are they under policy?

Responsibilities:

- external observation normalization
- opportunity representation
- six-dimensional evaluation
- evidence and uncertainty
- qualification result

### Business Economics

Answers:

> Is this opportunity economically worth pursuing?

Responsibilities:

- expected revenue
- expected cost
- expected profit
- expected margin
- profit per hour
- risk-adjusted economics
- economic assumptions/provenance

### Decision & Planning

Future responsibility:

- opportunity selection
- portfolio allocation
- capacity-aware planning
- execution strategy selection

### Capability & Execution

Future responsibility:

- capability registry
- capability selection
- cost/quality/reliability metadata
- execution planning
- execution monitoring

AI and tools are capabilities, not domain owners.

### Quality & Delivery

Future responsibility:

- quality gates
- verification
- delivery readiness
- acceptance evidence
- revision handling

### Measurement & Learning

Future responsibility:

- expected vs actual
- variance analysis
- outcome metrics
- capability performance
- marketplace performance
- learning signals

### Experimentation

Future responsibility:

- hypotheses
- controlled policy/strategy variants
- experiment metrics
- promotion/rejection decisions

## Cross-Cutting Business Concerns

- Policy
- Risk
- Auditability
- Explainability
- Autonomy level
- Versioning
- Resource constraints

## Domain Flow

External Observation
→ Normalization
→ Opportunity
→ Opportunity Evaluation
→ Economic Assessment
→ Decision
→ Planning
→ Capability Selection
→ Execution
→ Quality
→ Delivery
→ Measurement
→ Learning
→ Experimentation / Policy Improvement

## Boundary Rule

No external marketplace SDK, HTTP framework, database, UI framework, or AI provider may become a dependency of core business meaning.

External systems enter through explicit replaceable boundaries.
