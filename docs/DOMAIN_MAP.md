# Domain Map

## Product Core

The platform is an **Economic Opportunity OS / Business Automation OS**.

Freelancing is the first laboratory, not the permanent architectural boundary.

## Core Domain Areas

### Market Intelligence

Future responsibility:

- market observation
- demand signals
- trend and competitor observations
- source provenance
- data quality
- research boundaries

### Opportunity Intelligence

Answers:

> What opportunities exist, what do we know about them, and how suitable are they under the applicable policy?

Responsibilities:

- opportunity representation
- opportunity type
- external observation normalization
- six-dimensional evaluation for applicable opportunity contexts
- evidence and uncertainty
- qualification result

### Business Model Discovery

Answers:

> What different ways could this demand become an economically useful business?

Responsibilities:

- business-model hypotheses
- target customer
- value proposition
- revenue model
- recurring-revenue potential
- automation intensity
- alternative models for the same demand

### Business Economics

Answers:

> What are the expected economics of this opportunity or business model?

Responsibilities:

- expected revenue
- expected cost
- expected profit
- expected margin
- profit per hour
- risk-adjusted economics
- economic assumptions/provenance
- consumption of resource-cost information

### Resource Economics

Answers:

> What resources are consumed, and what monetary cost does that consumption represent?

Responsibilities:

- resource usage
- resource kind
- quantity
- unit cost
- derived total resource cost

V1 kinds:

- HUMAN_TIME
- CAPABILITY_USAGE
- INFRASTRUCTURE
- COMMUNICATION
- MARKETPLACE_FEE
- REVIEW_TIME

### Capacity

Answers:

> How much constrained human-time capacity remains in a planning period?

Responsibilities:

- planning period
- total hours
- committed hours
- reserved hours
- remaining hours
- utilization

Capacity is operational constraint data, not a profitability score.

### Economic Health

Answers:

> How economically healthy, stable, safe, and scalable is this opportunity or business across the dimensions that matter?

Responsibilities:

- profitability score
- profit potential score
- profit stability score
- demand stability score
- safety score
- recurring revenue score
- automation score
- capital efficiency score
- scalability score
- evidence quality score
- preservation of supporting evidence/metrics

The Economic Profile is intentionally a vector rather than a universal master score. Scoring formulas and thresholds remain changeable policy.

### Venture Intelligence

Answers:

> Is this broader venture thesis worth validating?

Responsibilities:

- venture evaluation
- market demand
- market size
- competition
- capital requirement
- time to revenue
- recurring revenue
- automation potential
- scalability
- risk
- evidence quality
- strategic fit
- exit/expansion potential

### Decision & Portfolio Planning

Future responsibility:

- opportunity selection
- portfolio allocation
- capacity-aware planning
- opportunity cost
- capital allocation
- configurable business objectives

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
- venture/business performance
- business memory
- learning signals

### Experimentation & Validation

Future responsibility:

- hypotheses
- validation experiments
- controlled variants
- measurable outcomes
- promotion/rejection decisions

### Revenue Engine

Future responsibility:

- demand acquisition
- offer design
- pricing
- conversion
- delivery
- retention
- expansion
- recurring revenue

## Cross-Cutting Business Concerns

- Policy
- Risk
- Auditability
- Explainability
- Autonomy level
- Versioning
- Resource constraints
- Provenance
- Capital constraints

## Domain Flow

**Market Signals → Opportunity Discovery → Evaluation → Business Model Discovery → Economics → Resource/Capacity Analysis → Venture Thesis → Validation → Execution → Revenue → Measurement → Learning → Experimentation → Scale / Kill → Portfolio / Capital Allocation**

The freelance loop remains a concrete first path through this broader flow.

## Boundary Rule

No external marketplace SDK, HTTP framework, database, UI framework, AI provider, or financial execution provider may become a dependency of core business meaning.

External systems enter through explicit replaceable boundaries.


### Marketing & Growth Automation

Answers:

> How do we acquire demand, operate distribution, and learn whether marketing creates durable economic value?

Responsibilities:

- positioning and offer communication
- campaign planning
- audience/channel selection
- organic and paid growth experiments
- campaign lifecycle
- measurable performance observations
- social presence operations
- customer/comment feedback handling
- campaign learning and iteration

The domain is provider-independent. Advertising platforms, social networks, content tools, communication providers, and AI models enter through replaceable capabilities/adapters.

### Revenue & Growth Measurement

Marketing performance connects Revenue Engine and Measurement & Learning through observable metrics such as impressions, clicks, leads, conversions, spend, revenue, CTR, conversion rate, CAC, and ROAS.

Campaign metrics are not a universal business score. They are evidence used by business economics, economic health, and experimentation policies.

## Expanded Domain Flow

**Market Signals → Opportunity Discovery → Evaluation → Business Model Discovery → Economics → Resource/Capacity Analysis → Venture Thesis → Validation → Build → Market → Sell → Operate → Measure → Learn → Experiment → Scale / Kill → Portfolio / Capital Allocation**

### Market Intelligence — Current Foundation

The first domain foundation now distinguishes:

**Market Observation → Demand Signal**

MarketObservation preserves source, observed value, timestamp, and evidence quality.

DemandSignal is a derived assessment with bounded demand strength, evidence quality, and supporting observation count.

Neither object is itself a validated opportunity or business decision.

## Venture Validation & Experimentation — Current Foundation

Answers:

> What is the cheapest credible test that can produce decision-useful evidence for this venture thesis?

Responsibilities:

- validation hypotheses
- measurable success criteria
- controlled variants
- bounded experiment budgets
- experiment lifecycle
- measured outcomes
- explicit promotion/rejection/continue-testing decisions

The validation model is provider-independent. External execution belongs to capabilities/adapters and authorization policy.

**Validation Flow:** Venture Thesis → Hypothesis → Experiment → Result → Evidence → Explicit Decision → Learning

Experiment results do not silently rewrite policy or venture state.
