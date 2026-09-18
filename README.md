# Economic Opportunity OS

## Product Direction

This repository is evolving from a freelancer automation platform into an **Economic Opportunity OS / Business Automation OS**.

Freelancing remains the first laboratory because it gives us a concrete, measurable path from demand to sale to delivery to revenue and actual economics.

It is not the permanent architectural boundary.

The long-term system discovers opportunities across multiple markets, proposes multiple business models, evaluates economics and evidence, validates cheaply, operates proven businesses, learns from outcomes, and eventually supports portfolio and capital-allocation decisions under explicit policy.

## Core Economic Loop

**Market Signals → Opportunity Discovery → Business Model Discovery → Venture Thesis → Economic Evaluation → Validation → Revenue → Measurement → Learning → Experimentation → Scale / Kill → Portfolio / Capital Allocation**

## Economic Health

Profitability is not the only economic objective.

The platform maintains a changeable Economic Profile with separate 0–100 dimensions for:

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

There is intentionally no permanent universal master score. A stable, profitable, safe business can therefore be protected even when its growth potential is modest.

Economic scores are derived assessments supported by evidence/metrics. Scoring formulas, thresholds, baselines, and time windows remain policy and may evolve without changing business identity.

Future portfolio postures such as PROTECT, MAINTAIN, GROW, and TURNAROUND are policy decisions, not intrinsic business states.

## Opportunity Types

- Freelance
- Service
- Product
- SaaS
- Game
- Digital Asset
- Recurring Revenue
- Partnership
- Investment
- Acquisition

These types are explicit domain categories. They are not forced into one universal evaluation algorithm.

## Opportunity Intelligence

The original six dimensions remain committed for their applicable opportunity context:

1. Eligibility
2. Requirement Fit
3. Estimated Effort
4. Economic Fit
5. Client / Project Risk
6. Success Confidence

Evaluation remains explainable and preserves criterion-level evidence and uncertainty.

## Venture Intelligence

Broader ventures use a separate evaluation model covering:

- Market Demand
- Market Size
- Competition
- Capital Requirement
- Time to Revenue
- Recurring Revenue Potential
- Automation Potential
- Scalability
- Risk
- Evidence Quality
- Strategic Fit
- Exit / Expansion Potential

## Evidence

The domain distinguishes:

**FACT → OBSERVATION → ESTIMATE → ASSUMPTION → HYPOTHESIS → FORECAST → EXPERIMENT_RESULT**

This prevents estimates and hypotheses from silently becoming facts.

## Business Model Discovery

The same demand can produce multiple hypotheses:

- freelance service
- productized service
- managed service
- SaaS
- API
- digital product
- game
- white-label
- subscription
- partnership

Recurring revenue and automation intensity are explicit.

## Low-Touch Recurring Revenue

The system should search for businesses with recurring revenue, high automation potential, low human dependency, and acceptable maintenance/support economics.

"Passive income" is modeled as low-touch recurring economics, not assumed literal passivity.

## Investment Boundary

Investment opportunities are initially research and decision support.

Automatic financial execution and automatic capital movement are outside the current domain implementation boundary.

## Architecture

- Modular monolith initially.
- Domain logic is independent from HTTP, persistence, marketplace SDKs, UI, AI providers, and financial execution providers.
- External platforms are isolated behind replaceable adapters.
- AI and tools are replaceable capabilities.
- Business decisions are explainable and auditable.
- Learning produces evidence and recommendations; it does not silently rewrite policy.
- High-risk or irreversible actions require explicit policy and appropriate approval.
- Economic scoring policy remains changeable and separate from core business identity.

## Current Domain Foundations

Implemented:

- OpportunityType
- Evidence taxonomy
- BusinessModelHypothesis
- Venture evaluation
- Venture lifecycle
- EconomicEstimate
- EconomicProfile
- Opportunity Intelligence foundations

Still outside the current slice:

- marketplace SDKs
- real credentials
- persistence
- HTTP/API
- UI
- AI provider dependencies
- financial execution
- automatic capital movement

## Engineering Process

**UNDERSTAND → MAP → DESIGN → DISCUSS TRADE-OFFS → DECIDE → TEST → IMPLEMENT → REVIEW → REFACTOR → DOCUMENT → LEARN → UPDATE THE MAP**

See KHALED_ENGINEERING_WORKING_RULES.md and docs/README.md.
