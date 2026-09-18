# Opportunity Evaluation Policy

## Status

**COMMITTED — Version 1 domain evaluation direction**

This document describes the committed V1 Opportunity Intelligence evaluation model. Marketplace selection, persistence, API, UI, and advanced ranking remain separate decisions.

## Evaluation Goal

Given an opportunity and a user-configured policy, determine:

- whether it satisfies hard constraints
- how well its requirements fit available capabilities
- what effort may be required
- whether the economics appear suitable
- what observable project/client risks exist
- how confident the system is that the work can succeed

Every derived conclusion must preserve evidence and uncertainty.

## Six Evaluation Dimensions

### C1 — Eligibility

Hard user constraints such as:

- allowed project types
- required capabilities
- budget boundaries
- client/location constraints
- project-size constraints

Possible criterion outcomes:

- PASS
- FAIL
- INSUFFICIENT_DATA
- NOT_APPLICABLE

### C2 — Requirement Fit

Assesses alignment between requested work and configured capabilities.

The evaluator must not invent missing requirements.

### C3 — Estimated Effort

Represents an effort range/estimate with explicit uncertainty rather than false precision.

### C4 — Economic Fit

Evaluates expected economics using explicit assumptions such as:

- expected revenue
- estimated effort
- platform fees
- capability/tool costs
- operating costs
- revision allowance

### C5 — Client / Project Risk

Captures observable evidence such as:

- incomplete information
- unclear requirements
- unusually broad scope
- conflicting constraints
- externally available historical indicators

The system must not turn sparse evidence into unsupported claims about a client.

### C6 — Success Confidence

Represents confidence that the work can be completed successfully under current information and capabilities.

It is a derived assessment, not a fact about the client.

## Overall Outcomes

- QUALIFIED
- NOT_QUALIFIED
- REVIEW_REQUIRED

The model explicitly represents uncertainty.

## Numeric Scoring

A numeric score is **not required** for V1.

Ranking can be introduced later as a separate derived representation after real evaluation behavior provides evidence for useful weighting.

## Relationship to Business Economics

Economic Fit is one evaluation dimension.

The broader Business Economics domain also owns reusable economic calculations used later by:

- opportunity selection
- pricing
- resource planning
- portfolio allocation
- expected-vs-actual measurement

This prevents economic logic from being trapped inside Opportunity Evaluation.

## Re-Evaluation

An opportunity can be evaluated multiple times under different policy versions.

Evaluation remains derived data and does not mutate Opportunity identity.

## Learning

Evaluation outcomes can become learning evidence later, but learning does not silently rewrite policy.
