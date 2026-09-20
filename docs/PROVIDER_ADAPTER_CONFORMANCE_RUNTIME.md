# Provider Adapter Conformance — Runtime Contract

This increment turns the approved provider-adapter conformance gate into a reusable non-executing validation boundary.

The validator receives an already-produced ProviderExecutionResult and the AuthorizedExecutionRequest it claims to represent. It verifies:
- result type
- request identity
- idempotency identity
- timezone-aware observation
- explicit status
- non-empty outcome code
- non-empty optional external reference

It performs no provider call, authorization, retry, scheduling, or state mutation.

The existing dispatch path remains responsible for invoking the provider adapter and then delegates result validation to this boundary.
