# Design Gate — History-Aware Execution Coordination

**Status:** APPROVED — V1 coordination boundary.

## Purpose

Make immutable execution-attempt history the authoritative source for observed attempt count during coordination.

## V1 Flow

Prepared Request → ExecutionPort → ExecutionOutcome → ExecutionAttempt → Immutable History → History Consistency → Outcome Policy → Recovery Handoff

## Decisions

1. The coordinator derives the next attempt number from existing immutable history.
2. The provider result is recorded as an explicit ExecutionAttempt before policy assessment.
3. Policy assessment consumes history-consistent evidence; callers do not supply an independent attempt count.
4. Existing request/idempotency identity remains authoritative.
5. Empty history starts at attempt 1.
6. Existing history is never mutated in place; a new immutable history is returned.
7. Provider execution remains behind ExecutionPort.
8. The coordinator does not retry, schedule, authorize, compensate, or perform additional external actions.
9. Inconsistent pre-existing history identity is rejected before provider execution.
