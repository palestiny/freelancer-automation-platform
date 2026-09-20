# Design Gate — Provider Credential Reference Boundary

**Status:** APPROVED — V1 provider-independent credential reference contract.

## Problem

Provider adapters need authentication/configuration at runtime, but provider credentials must not enter domain entities, provider registries, logs, evidence artifacts, or execution policy.

## V1 Decision

The domain may carry an opaque credential reference containing provider key and credential reference ID.
It never carries access tokens, passwords, API keys, cookies, refresh tokens, or secret material.
Credential resolution is an application/infrastructure concern and is not implemented by this gate.

## Contract

ProviderCredentialReference validates non-empty provider key and credential reference ID. Both are opaque identifiers and equality is value-based.

## Trade-offs

Opaque reference (chosen): keeps secrets outside domain and persistence contracts; supports Windows/mobile/server secret stores later; allows provider-specific authentication without coupling the domain.

Raw credentials in execution requests (rejected): simpler adapter invocation but creates leakage risk into logs, tests, persistence, and domain boundaries.

Provider-specific credential types in domain (rejected): precise authentication modeling but couples the core to concrete providers.

## Boundaries

No secret-store implementation, credential fetching, token refresh, rotation, authorization, provider execution, or credential health checking is introduced.