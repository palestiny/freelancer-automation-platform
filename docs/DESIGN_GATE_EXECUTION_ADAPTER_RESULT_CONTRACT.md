# Design Gate — Execution Adapter Result Contract

**Status:** APPROVED — V1 application-layer adapter result contract hardening.

## Purpose

Replace the raw dictionary crossing the execution adapter boundary with an explicit immutable result contract and verify request identity before creating the provider-independent ExecutionOutcome.

## V1 Decisions

- Adapter results are represented by a typed immutable `ProviderExecutionResult`.
- The result carries request identity, idempotency identity, outcome status, outcome code, observation time, and optional external reference.
- Dispatch rejects results whose `request_id` or `idempotency_key` differs from the prepared request.
- Provider-specific payloads remain outside the domain contract.
- The adapter boundary does not authorize, retry, schedule, compensate, or execute policy.
- No provider implementation is introduced by this hardening.

## Safety Boundary

A provider adapter cannot accidentally associate an outcome with a different request or idempotency key. The resulting ExecutionOutcome remains provider-independent evidence.
