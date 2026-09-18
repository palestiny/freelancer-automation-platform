# Freelancer Automation Platform

Professional automation platform for the freelancer lifecycle.

## Current Phase

**Phase 0 — Product & Architecture**

The project is currently completing the Opportunity Intelligence Design Gate. Implementation has intentionally not started.

## Product Direction

The platform is being designed as a controlled autonomous freelancer lifecycle system that can eventually:

- discover freelance opportunities
- evaluate opportunities against configurable user policy
- prepare and manage proposals
- plan and execute projects using replaceable AI/tool capabilities
- communicate with clients
- handle revisions
- verify and deliver work
- learn from outcomes and operational metrics

The first implementation slice is intentionally much smaller:

**Opportunity Discovery → Normalization → Evaluation → Persistence → API/Dashboard**

## Architecture Direction

- Modular monolith initially.
- Domain logic remains independent from HTTP, persistence, marketplace SDKs, UI, and AI providers.
- External freelance platforms are isolated behind adapters/ports.
- AI is a replaceable capability, not the owner of business architecture.
- Evaluation results must be explainable and preserve evidence/uncertainty.

## Engineering Process

**UNDERSTAND → MAP → DESIGN → DISCUSS TRADE-OFFS → DECIDE → TEST → IMPLEMENT → REVIEW → REFACTOR → DOCUMENT → LEARN → UPDATE THE MAP**

See docs/README.md for the documentation map and source-of-truth rules.

## Current Gate

**Opportunity Intelligence Design Gate — OPEN**

The proposed evaluation model and gate-resolution documents are intentionally marked as proposals. Product-owner decisions must be approved before they become committed domain behavior.

Once the gate is closed, implementation starts with domain TDD:

**RED → GREEN → REFACTOR**
