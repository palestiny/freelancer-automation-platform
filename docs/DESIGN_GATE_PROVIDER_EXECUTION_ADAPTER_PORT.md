# Design Gate — Provider Execution Adapter Port

**Status:** APPROVED — V1 application boundary for executing an already-authorized request.

## Purpose

Introduce the first application-layer boundary between domain authorization/request artifacts and future external providers.

Flow:

**Policy Review → Authorization → Authorized Execution Request → Execution Port → Provider Adapter → Execution Outcome**

## V1 Contract

The application port accepts only an `AuthorizedExecutionRequest` in `PREPARED` state and returns an `ExecutionOutcome`.

The port is provider-independent. Provider adapters implement it outside the domain.

The port must preserve request identity and idempotency key, reject non-prepared requests before provider dispatch, return an explicit outcome artifact, never authorize an action, never choose autonomy, never retry automatically, never schedule, never mutate policy, and never perform financial authorization.

## Adapter Boundary

Provider-specific concerns remain outside the domain/application contract: credentials, HTTP/SDK clients, marketplace APIs, browser automation, queues/workers, rate limits, provider-specific retry behavior, persistence, and network calls.

An adapter may translate a provider response into the domain `ExecutionOutcome`.

## Safety

The port does not bypass `ActionAuthorization` or create authorization. It only dispatches a request that has already crossed the explicit authorization boundary.

Financial and irreversible actions remain blocked by the existing authorization boundary.

## Decision Gate

This gate deliberately introduces a port only. No concrete provider adapter, network integration, retry engine, queue, scheduler, or external side effect is implemented in V1.
