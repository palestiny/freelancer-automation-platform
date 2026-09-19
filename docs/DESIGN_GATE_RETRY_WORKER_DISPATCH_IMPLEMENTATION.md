# Retry Worker Dispatch Runtime Contract

**Status:** V1 implementation.

This application boundary consumes one durable scheduled retry command at a time. It does not implement a background loop, queue framework, lease renewal, or provider selection.

Flow:

**Scheduled Command → Atomic Claim → Authorization Revalidation → Prepared Request → ExecutionPort → Observed Outcome → Outcome Handoff**

Safety:
- failed claim never executes;
- authorization/request identity is revalidated before provider dispatch;
- stale authorization is persisted as REJECTED_STALE;
- duplicate delivery cannot create a second claim;
- provider UNKNOWN outcome is passed to the existing outcome handoff and therefore requires manual review;
- provider exceptions do not fabricate an ExecutionOutcome;
- persistence failure after provider execution remains explicit and preserves the observed outcome for reconciliation;
- no automatic retry is initiated.

The existing ExecutionPort remains the only provider-facing boundary.
