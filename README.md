# Freelancer Automation Platform

## Product Direction

This project is evolving into a **Business Automation OS**, initially validated through the freelance-work market.

The platform is designed to discover opportunities, understand and evaluate them, assess their economics, decide what is worth pursuing, plan and execute work through replaceable capabilities, verify quality, measure actual outcomes, and continuously improve its policies and strategies.

Freelancing is the first market. It is not the permanent architectural boundary.

## Core Business Loop

**Opportunity → Evaluation → Economics → Decision → Planning → Execution → Quality → Delivery → Measurement → Learning → Experimentation**

The goal is not maximum automation for its own sake. The goal is **controlled, measurable, economically valuable automation**.

## Opportunity Evaluation

The first Opportunity Intelligence slice evaluates six dimensions:

1. Eligibility
2. Requirement Fit
3. Estimated Effort
4. Economic Fit
5. Client / Project Risk
6. Success Confidence

Evaluation remains explainable and preserves criterion-level evidence and uncertainty.

Overall outcomes:

- QUALIFIED
- NOT_QUALIFIED
- REVIEW_REQUIRED

Numeric opportunity scoring is intentionally not required in the first domain slice.

## Business Economics

Profitability is a first-class domain concern.

The platform now models:

- expected revenue
- expected cost
- expected profit
- expected margin
- expected profit per hour
- risk-adjusted profit

Cost can explicitly include:

- marketplace/platform fees
- capability/tool costs
- operating costs
- revision allowance

Economic estimates remain derived data and never mutate Opportunity identity.

## Long-Term Platform Direction

The platform is intended to grow toward:

- resource and capacity economics
- opportunity portfolio optimization
- capability selection based on cost, quality, speed, and reliability
- expected-vs-actual measurement
- business memory
- policy versioning
- controlled experimentation
- progressive autonomy levels
- multi-marketplace integrations
- proposal, project, communication, revision, quality, and delivery automation
- AI-assisted analysis and recommendations without making AI the owner of business architecture

## Architecture

- Modular monolith initially.
- Domain logic is independent from HTTP, persistence, marketplace SDKs, UI, and AI providers.
- External platforms are isolated behind replaceable adapters/ports.
- AI and tools are replaceable capabilities.
- Business decisions are explainable and auditable.
- Learning produces evidence and recommendations; it does not silently rewrite policy.
- Irreversible or high-risk actions require explicit policy and appropriate approval.

See `docs/DOMAIN_MAP.md` and `docs/DESIGN_GATE_BUSINESS_ECONOMICS_AND_GROWTH.md`.

## Current Phase

**Phase 0 — Product & Architecture → Business Economics & Growth Gate Approved → Domain TDD in progress**

The first economic domain slice is implemented alongside the approved Opportunity Intelligence domain slice.

The current implementation remains domain-only:

- no marketplace SDK
- no real marketplace credentials
- no persistence
- no HTTP/API
- no UI
- no AI provider dependency

## Engineering Process

**UNDERSTAND → MAP → DESIGN → DISCUSS TRADE-OFFS → DECIDE → TEST → IMPLEMENT → REVIEW → REFACTOR → DOCUMENT → LEARN → UPDATE THE MAP**

See `KHALED_ENGINEERING_WORKING_RULES.md` and `docs/README.md`.
