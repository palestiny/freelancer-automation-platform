# Design Gate — Performance Observation Application Service

**Status:** APPROVED — V1 application use cases over the persistence port.

## Scope

Expose two provider-independent application operations:
- record one authoritative performance observation
- retrieve one business's ordered performance history

The service depends only on the application repository port and domain types.

## Rules

1. The application layer does not import SQLite or any infrastructure adapter.
2. Recording delegates durable storage to the repository after domain validation.
3. Retrieval preserves repository ordering and returns domain observations.
4. No aggregation, statistical analysis, policy evaluation, learning, authorization, or execution is triggered.
5. Repository failures propagate; the service must not convert persistence failure into success.
6. Business isolation is preserved by the repository contract.
