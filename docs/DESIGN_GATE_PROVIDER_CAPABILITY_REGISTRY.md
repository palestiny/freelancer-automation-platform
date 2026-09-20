# Design Gate — Provider Capability Registry

**Status:** APPROVED — V1 explicit provider capability declaration and lookup.

## Purpose

Execution provider registration currently resolves an adapter by provider key. The platform also needs to know, without invoking a provider, which bounded capabilities an adapter declares.

This gate adds metadata only. It does not add provider discovery, credentials, health checks, fallback, ranking, execution, or automatic capability selection.

## V1 Capability Vocabulary

- SEARCH_OPPORTUNITIES
- READ_OPPORTUNITY
- SUBMIT_PROPOSAL
- SEND_MESSAGE
- DELIVER_ASSET
- READ_CLIENT_FEEDBACK

The vocabulary is intentionally small and provider-independent. Adding a capability requires an explicit design decision.

## Contract

A provider registration consists of:
- provider_key
- execution adapter
- declared capability set

The registry must:
- reject empty provider keys
- reject duplicate provider keys
- reject non-ExecutionPort adapters
- reject empty capability declarations
- reject unknown capability values
- resolve provider adapter explicitly
- answer whether a provider declares a capability
- expose capabilities without executing the provider

## Boundaries

No provider API calls, credentials, health status, ranking, fallback, dynamic capability discovery, policy mutation, authorization, execution, or marketplace-specific behavior.
