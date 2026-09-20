# Design Gate — Provider Adapter Conformance

**Status:** APPROVED — V1 reusable conformance boundary for future external execution adapters.

## Purpose

Real marketplace, marketing, payment, and other external providers must remain replaceable adapters. Before any concrete provider is integrated, the platform needs a provider-independent conformance contract that verifies the adapter boundary without embedding provider semantics into the domain.

## V1 Contract

An execution adapter must:
- accept only the prepared execution request contract;
- preserve request identity and idempotency identity;
- return the explicit provider execution result contract;
- provide a timezone-aware observation timestamp;
- preserve explicit success/failure/unknown semantics;
- never authorize an action;
- never mutate retry policy;
- never schedule another attempt;
- never silently transform an unknown result into success/failure;
- keep provider credentials/configuration outside the domain model.

## Conformance Scope

The V1 conformance layer verifies structural/runtime adapter behavior only. It does not:
- select providers;
- rank providers;
- perform real external calls;
- define marketplace-specific semantics;
- choose credentials;
- implement retries;
- introduce queues or workers;
- authorize execution.

A concrete provider integration still requires its own adapter design and integration tests.

## Gate Rule

No real provider adapter should be considered production-ready unless it passes the common conformance contract plus provider-specific tests.
