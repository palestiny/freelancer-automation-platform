# Proposed Opportunity Evaluation Policy

## Status

**PROPOSED — not a committed product decision.**

This document proposes the minimum evaluation model for the first Opportunity Intelligence vertical slice. It is intended to make the design concrete enough for TDD while preserving product-owner decisions.

## 1. Evaluation Goal

The evaluator should answer:

> Given an opportunity and a user-configured policy, what do we know about its suitability, what evidence supports each conclusion, and where is uncertainty preventing a confident decision?

The evaluator is not responsible for submitting proposals, negotiating with clients, executing projects, or making irreversible actions.

## 2. Proposed Criteria

### C1 — Eligibility

Determines whether the opportunity satisfies hard user constraints.

Examples:
- marketplace/source allowed
- project type allowed
- minimum/maximum budget
- required skills
- client location restrictions
- project size restrictions

This criterion may produce:
- PASS
- FAIL
- INSUFFICIENT_DATA

### C2 — Requirement Fit

Assesses whether the requested work matches the platform's configured capability profile.

Evidence may include:
- required technologies
- task categories
- explicit client requirements
- known capability coverage

The evaluator must not invent missing requirements.

### C3 — Estimated Effort

Represents an estimated effort range rather than pretending that an exact number of hours is known.

Example representation:
- minimum estimate
- expected estimate
- maximum estimate
- confidence/data-quality state

The first version should allow this to remain INSUFFICIENT_DATA.

### C4 — Economic Fit

Evaluates whether the opportunity's available compensation is compatible with the configured economic policy.

Possible derived values:
- expected gross revenue
- estimated effort
- implied hourly value
- platform-fee allowance when known
- risk/revision allowance when configured

No specific monetary threshold is committed by this proposal.

### C5 — Client / Project Risk

Captures observable risk indicators without turning them into unsupported claims about the client.

Examples of evidence:
- missing project information
- unclear requirements
- unusually broad scope
- conflicting constraints
- externally reported client history when available

A derived risk assessment must retain its evidence and uncertainty.

### C6 — Success Confidence

Represents the evaluator's confidence that the opportunity can be completed successfully under the current information and capability profile.

This is a derived assessment, not a fact about the client or project.

It should remain distinguishable from:
- client reputation
- marketplace rating
- historical completion counts

## 3. Proposed Result Model

Each criterion produces an explicit result plus evidence.

Conceptually:
- criterion
- outcome
- evidence
- uncertainty
- data-quality status

Candidate criterion outcomes:
- PASS
- FAIL
- INSUFFICIENT_DATA
- NOT_APPLICABLE

The overall qualification result remains:
- QUALIFIED
- NOT_QUALIFIED
- REVIEW_REQUIRED

These outcome names are PROPOSED.

## 4. Scoring Proposal

The first domain implementation should NOT require a numeric score.

The proposed initial approach is:
1. Evaluate hard eligibility rules first.
2. Evaluate qualitative/economic criteria independently.
3. Preserve criterion-level outcomes and evidence.
4. Produce an overall qualification result.
5. Add numeric scoring only after real evaluation behavior demonstrates a need for ranking opportunities.

Reason: a numeric score can create false precision before the project has enough validated domain behavior to justify weights.

If ranking becomes a requirement, scoring can be introduced as a separate derived representation without changing Opportunity identity.

## 5. Policy Configuration Proposal

The policy should be a domain concept rather than scattered constants.

A policy should eventually be able to express:
- allowed project types
- skill/capability requirements
- budget boundaries
- client/location constraints
- project-size constraints
- economic thresholds
- risk tolerance
- other user-configurable criteria

The exact persistence mechanism remains OPEN.

For the first TDD slice, a policy may be created in memory.

## 6. Evidence and Uncertainty

Every derived conclusion should distinguish:

**Known**
- directly supported by normalized external data or another trusted internal source.

**Derived**
- calculated or interpreted from available evidence.

**Unknown**
- information not available.

**Uncertain**
- information exists but its quality or interpretation is insufficient for a confident conclusion.

The evaluator must never convert UNKNOWN into a fabricated fact.

## 7. Re-Evaluation

An opportunity may be evaluated multiple times.

An evaluation should therefore be treated as a separate derived result with enough context to understand:
- which policy was used
- which opportunity representation was evaluated
- which criteria were evaluated
- what evidence was available
- what result was produced

This supports future policy changes and historical analysis.

## 8. Proposed First TDD Scope

The first domain tests should focus on behavior, not persistence or HTTP.

Minimum scenarios:
1. A policy can define a hard eligibility requirement.
2. An eligible opportunity passes the requirement.
3. A clearly ineligible opportunity fails the requirement.
4. Missing required evidence produces INSUFFICIENT_DATA rather than an invented value.
5. Evaluation records criterion-level evidence.
6. Evaluation leaves the Opportunity unchanged.
7. The same Opportunity can be evaluated under two different policies.
8. Overall REVIEW_REQUIRED can represent unresolved uncertainty.
9. No numeric score is required for the first implementation.

## 9. Open Decisions Requiring Product-Owner Approval

Before treating this proposal as committed, Khaled must decide:
1. Whether these six criteria are the right first evaluation dimensions.
2. Whether hard eligibility should be separated from softer qualification criteria.
3. Whether the initial overall outcomes should be QUALIFIED / NOT_QUALIFIED / REVIEW_REQUIRED.
4. Whether numeric scoring should remain out of the first vertical slice.
5. Which policy constraints are mandatory in version one.
6. Which first marketplace will provide real-world observations.

Until these are approved, this document remains a design proposal.
