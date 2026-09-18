# Business Economics & Growth Design Gate

## Status

**APPROVED — V1 business-economics direction committed; domain TDD implementation in progress.**

## Purpose

Make profitability, resource economics, measurement, learning, and controlled growth first-class platform concerns rather than reporting features added after automation works.

The platform's goal is not merely to automate freelance actions. It must continuously improve the economic outcome of the work it performs.

## Product-Level Business Loop

Opportunity → Evaluation → Economic Assessment → Decision → Planning → Execution → Quality → Delivery → Measurement → Learning → Policy/Experiment Improvement.

The loop is intentionally closed. Actual outcomes must be able to challenge previous estimates.

## Committed V1 Economic Concepts

### Expected Revenue

Revenue expected from the opportunity before execution.

### Expected Cost

The expected cost of producing and delivering the work, including applicable platform fees, capability/tool costs, operating costs, and configured allowances.

### Expected Profit

Expected Revenue minus Expected Cost.

### Expected Margin

Expected Profit divided by Expected Revenue when revenue is positive.

### Expected Profit per Hour

Expected Profit divided by expected effort when effort is positive.

### Risk-Adjusted Profit

Expected Profit adjusted by a configured success-confidence probability.

This is a derived planning metric, not a guarantee.

## Economic Health and Stability

Economic quality is broader than expected profit alone. The platform must measure and preserve separate dimensions for profitability, profit potential, profit stability, demand stability, safety, recurring revenue, automation, capital efficiency, scalability, and evidence quality.

A stable profitable business is not automatically inferior to a higher-upside but less stable business. Future policy may protect, maintain, or carefully optimize stable economic assets.

The V1 Economic Profile is a changeable 0–100 score vector. It does not define a universal master score. Scoring formulas, thresholds, evidence requirements, comparison baselines, and time windows remain policy concerns.

See `DESIGN_GATE_ECONOMIC_HEALTH_AND_PORTFOLIO_POLICY.md` for the dedicated gate.

## Resource Economics

Resource economics is now an approved V1 domain foundation.

The platform models explicit resource consumption using:

- resource kind
- quantity
- monetary unit cost
- derived total cost

V1 resource kinds are:

- HUMAN_TIME
- CAPABILITY_USAGE
- INFRASTRUCTURE
- COMMUNICATION
- MARKETPLACE_FEE
- REVIEW_TIME

Human time is the first constrained capacity model. Capacity snapshots represent a defined planning period with total, committed, reserved, remaining, and utilization hours.

Resource cost and capacity are separate concepts:

- resource usage answers what was consumed and what it cost
- capacity answers what constrained availability remains

Neither is itself an Economic Health score.

See `DESIGN_GATE_RESOURCE_ECONOMICS_AND_CAPACITY.md` for the dedicated boundary and trade-offs.

## Portfolio Direction

The platform should eventually optimize a portfolio of opportunities under constrained capacity rather than evaluating each opportunity in isolation.

The optimization objective must remain explicit and configurable. The platform must not silently invent a user's business objective.

## Measurement Loop

Every meaningful execution should be able to compare:

Expected → Actual → Variance → Learning Signal.

Important measurements include:

- revenue
- cost
- effort
- margin
- delivery time
- revisions
- acceptance
- reliability
- capability cost/performance
- marketplace integration performance

## Learning and Policy Safety

Learning produces evidence and recommendations.

Learning does not silently rewrite business policy.

The controlled path is:

Observed Data → Analysis → Recommendation → Policy/Experiment Decision → Versioned Change.

## Experimentation

The platform will support controlled experiments around:

- evaluation policies
- pricing
- proposal strategies
- execution strategies
- capability selection

Experiments must have a hypothesis, measurable metrics, a defined comparison, and an explicit promotion/rejection decision.

## Autonomy Levels

The platform should support progressive autonomy:

- L0 — Observe
- L1 — Recommend
- L2 — Prepare
- L3 — Execute with Approval
- L4 — Execute Automatically within Policy
- L5 — Optimize within Policy

Autonomy level is a policy concern. It is not permission for an AI provider to bypass business controls.

## Non-Goals of This Gate

This gate does not decide:

- first marketplace
- persistence technology
- API technology
- UI technology
- exact pricing thresholds
- a specific AI provider
- autonomous irreversible business actions without policy/approval

## First TDD Slice

Completed domain foundation:

1. Represent an economic estimate explicitly.
2. Calculate expected cost from explicit cost components.
3. Calculate expected profit.
4. Calculate expected margin.
5. Calculate expected profit per hour.
6. Calculate risk-adjusted profit from explicit success confidence.
7. Preserve the estimate as derived data without mutating Opportunity.
8. Reject invalid economic inputs instead of silently producing misleading values.

Resource/capacity foundation completed in its dedicated gate:

1. Represent explicit resource usage.
2. Calculate total resource cost.
3. Represent controlled resource kinds.
4. Represent human-time capacity for a planning period.
5. Calculate remaining capacity.
6. Calculate utilization.
7. Reject over-allocation.

Future slices include actual-vs-expected economics, opportunity cost, historical economics, and capacity-aware planning.
