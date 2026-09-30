# Freelancer API Terms & Production Access Validation Gate

## Status

**EVIDENCE REVIEW COMPLETE — PRODUCTION ACCESS NOT PROVEN.**

Issue #445 remains open. This gate records the current public evidence reviewed on 2026-09-30 and separates confirmed permissions from unresolved production/commercial access questions.

## Purpose

Validate whether the planned Freelancer marketplace adapter can progress from the existing Sandbox/read-only discovery boundary to a production dependency.

This gate does **not** authorize production integration, bidding, payment, or execution.

## Evidence Reviewed

### 1. Freelancer Developer Site

Freelancer's developer site explicitly describes the API as usable from websites, apps, or software and documents a Sandbox environment for testing without production data.

It also describes API-supported automation and lists open-source SDKs.

Source:
- https://developers.freelancer.com/

### 2. Freelancer API Terms & Conditions

The public API Terms state that Freelancer grants a limited license to **develop, test, and support** software applications and integrate the API with products/services while the agreement is complied with.

The same terms state that:

- the API may not be used in a manner inconsistent with the API terms or other agreements;
- the API should not be relied on for the ordinary course of business;
- applications may be charged for, but API access itself may not be sold/rented/leased/sublicensed/redistributed/syndicated;
- access/rate-limit restrictions must not be circumvented;
- cached data should be refreshed at least every 24 hours;
- stored API data must use strong encryption;
- data storage/copying is restricted by the API terms;
- Freelancer may change, suspend, discontinue, or limit API access.

Source:
- https://www.freelancer.com/about/apiterms

### 3. Current Freelancer User Agreement

The current User Agreement applies to users accessing Freelancer via the API.

Its access/interference section states that robots, spiders, scrapers, or other automated means may not access the Website, including the API, for any purpose without **express written permission**.

The agreement also incorporates the API Terms and Conditions as an additional policy/contractual source.

Source:
- https://www.freelancer.com/about/terms

## Confirmed

| Item | Current evidence | Gate status |
|---|---|---|
| Sandbox exists | Developer site explicitly documents Sandbox | CONFIRMED |
| API is intended for application integration | Developer site and API Terms | CONFIRMED |
| Development/testing/support use is licensed under API Terms | API Terms Section 3 | CONFIRMED |
| Production/commercial business dependency is established by public terms | No | NOT PROVEN |
| Automated API use is unconditionally permitted | No; current User Agreement requires express written permission for automated access | NOT PROVEN |
| Data retention/storage obligations exist | API Terms | CONFIRMED |
| API access can be changed/suspended/limited | API Terms | CONFIRMED |

## Critical Boundary

The public documentation supports continuing **Sandbox development/testing**.

It does **not** establish that this project has permission to make the Freelancer API a production/commercial dependency.

The current User Agreement's express-written-permission requirement for automated access is a material unresolved gate for this project.

Therefore:

**Production Freelancer integration remains blocked pending explicit permission/authorization evidence.**

## Architecture Consequence

No architecture change is required.

The provider-neutral marketplace adapter contract remains valid:

External Marketplace → Provider Adapter → External Observation → Normalization → Opportunity → Opportunity Intelligence

The existing Freelancer Sandbox adapter remains an experimental/test adapter.

The production boundary must not be enabled merely because the SDK/API technically supports a request.

## Required Evidence to Close the Gate

At least one authoritative, project-specific source is still required for the intended production use, such as:

1. explicit written permission from Freelancer authorizing the project's automated API use; or
2. a current official agreement/authorization that clearly covers the intended production/commercial automated use and is applicable to this project.

The evidence should also clarify, where applicable:

- production API access/approval process;
- applicable rate limits;
- allowed production data storage/caching;
- credential/authentication requirements;
- commercial/application restrictions;
- whether the intended opportunity-discovery automation is permitted.

## Non-goals

This gate does not authorize:

- bidding/proposal submission;
- messaging automation;
- payment execution;
- financial execution;
- production credential storage;
- bypassing API restrictions;
- scraping as a substitute for API permission.

## Decision

**Current gate outcome: BLOCKED / NOT PROVEN for production access.**

Sandbox development can continue within the existing provider-neutral adapter boundary.

Production integration must wait for project-specific authorization evidence.

## Exit Criteria

- authoritative production permission evidence captured;
- automation permission confirmed for intended use;
- production access requirements documented;
- storage/cache requirements mapped to the adapter/application boundary;
- no provider-specific production assumption leaks into the domain contract;
- owner records final gate decision.
