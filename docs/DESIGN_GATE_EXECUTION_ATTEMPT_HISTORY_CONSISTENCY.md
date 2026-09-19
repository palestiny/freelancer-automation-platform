# Design Gate — Execution Attempt History Consistency

**Status:** APPROVED — V1 evidence-consistency validation between execution outcomes and attempt history.

## Purpose

Prevent downstream recovery consumers from treating an execution outcome and its attempt history as the same evidence when their identities, counts, or latest observations disagree.

## V1 Contract

Input:
- one ExecutionOutcome
- one ExecutionAttemptHistory

Output:
- CONSISTENT
- IDENTITY_MISMATCH
- LATEST_ATTEMPT_MISMATCH
- EMPTY_HISTORY

Rules:
1. Request ID and idempotency key must match.
2. History must contain at least one attempt.
3. The consistency artifact reports the observed history length; it does not infer missing attempts or require contiguous attempt numbers.
4. The latest attempt must match outcome status, outcome code, timestamp, and external reference.
5. Consistency validation does not retry, schedule, authorize, execute, compensate, or mutate policy.
6. The history remains immutable evidence.
7. This boundary does not require contiguous attempt numbers; missing numbers remain explicit evidence.
