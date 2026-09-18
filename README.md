# Freelancer Automation Platform

Professional automation platform for the freelancer lifecycle.

## Current Phase

**Phase 0 — Product & Architecture — Gate Approved; Domain TDD in progress**

The Opportunity Intelligence Design Gate is closed. The first domain TDD slice is being implemented without marketplace, persistence, API, UI, or AI dependencies.

## Product Direction

The platform is a controlled autonomous freelancer lifecycle system that can eventually:

- discover freelance opportunities across multiple marketplaces
- evaluate opportunities against configurable user policy
- prepare and manage proposals
- plan and execute projects using replaceable AI/tool capabilities
- communicate with clients
- handle revisions
- verify and deliver work
- learn from outcomes and operational metrics
- measure and improve marketplace integrations using reports, feedback, comments, and AI-assisted recommendations

Marketplace selection is runtime configuration. No single marketplace is a core architectural dependency.

## First Domain Slice

**Opportunity → Evaluation Policy → Evaluation Result**

Current behavior includes eligibility evaluation, criterion evidence, explicit uncertainty, qualification outcomes, and policy-independent re-evaluation.

The first implementation remains domain-only:

- no marketplace SDK
- no real marketplace credentials
- no persistence
- no HTTP/API
- no UI
- no AI provider

## Architecture Direction

- Modular monolith initially.
- Domain logic remains independent from HTTP, persistence, marketplace SDKs, UI, and AI providers.
- External freelance platforms are isolated behind adapters/ports.
- Marketplace integrations are independently evolvable capabilities.
- AI is a replaceable capability, not the owner of business architecture.
- Evaluation results must be explainable and preserve evidence/uncertainty.

## Engineering Process

**UNDERSTAND → MAP → DESIGN → DISCUSS TRADE-OFFS → DECIDE → TEST → IMPLEMENT → REVIEW → REFACTOR → DOCUMENT → LEARN → UPDATE THE MAP**

See docs/README.md for the documentation map and source-of-truth rules.

## Current TDD Progress

- Eligibility PASS
- Eligibility FAIL
- Missing evidence → REVIEW_REQUIRED
- Criterion evidence preservation
- Opportunity identity preservation
- Policy independence
- Budget eligibility boundaries

Tests are executed automatically through GitHub Actions.
