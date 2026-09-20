# Design Gate — Provider Adapter Registry & Resolution

**Status:** APPROVED — V1 provider-independent adapter registration boundary.

## Purpose

Allow multiple external execution adapters to coexist without coupling the domain or execution coordinator to a concrete provider.

## V1 Contract

- Adapters are registered under an explicit non-empty provider key.
- A key resolves to exactly one adapter.
- Duplicate registration is rejected.
- Unknown keys are rejected explicitly.
- Resolution never ranks providers.
- Resolution never chooses a fallback provider.
- Registry never stores credentials or provider configuration secrets.
- Registry does not perform execution; it only resolves an already registered adapter.
- The execution coordinator continues to receive an `ExecutionPort`, preserving the existing boundary.

## Non-goals

No provider discovery, provider ranking, credential management, health-based routing, automatic fallback, load balancing, marketplace semantics, or external calls.
