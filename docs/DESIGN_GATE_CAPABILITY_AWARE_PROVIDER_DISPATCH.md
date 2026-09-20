# Design Gate — Capability-Aware Provider Dispatch

**Status:** APPROVED — V1 explicit capability precondition for provider execution.

## Purpose

The provider registry now declares capabilities. Execution dispatch must be able to enforce an explicit capability precondition before invoking an adapter.

## V1 Contract

Input:
- provider registry
- provider key
- required ProviderCapability
- prepared AuthorizedExecutionRequest

Behavior:
1. Validate the provider key and capability.
2. Resolve the provider explicitly.
3. Verify the provider declares the required capability.
4. Only then invoke the existing execution dispatch.

Failure:
- unknown provider → explicit KeyError
- unsupported capability → explicit ValueError
- invalid request remains governed by existing dispatch validation

## Boundaries

No capability inference, provider ranking, fallback, credential lookup, health routing, authorization creation, policy mutation, or execution beyond the already-authorized dispatch.

Capability checks are preconditions, not authorization.
