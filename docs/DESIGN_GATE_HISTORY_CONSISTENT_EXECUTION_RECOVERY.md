# Design Gate — History-Consistent Execution Recovery Handoff

**Status:** APPROVED — V1 composition boundary.

## Purpose

Prevent recovery intent from being created from a policy assessment that was produced without validating the immutable execution attempt history.

## V1 Flow

**ExecutionOutcome + ExecutionAttemptHistory + ExecutionOutcomePolicy → History Consistency → Policy Assessment → Recovery Handoff**

## Contract

- Inconsistent execution history produces no recovery handoff.
- Consistent history allows the existing history-aware policy assessment to produce the recovery assessment.
- The handoff preserves request identity, idempotency identity, observed attempt count, source assessment status, and recovery mode.
- Existing retry/manual-review semantics are reused; no new policy is introduced.

## Boundary

No scheduling, authorization, retry execution, compensation, provider calls, persistence, or automatic policy mutation.

## Decision

The history-aware composition function is the only V1 path that combines immutable attempt evidence with recovery intent. Existing low-level handoff creation remains available for already validated policy assessments.
