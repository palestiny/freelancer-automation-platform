# Design Gate — Retry Worker Provider Failure Handoff

**Status:** APPROVED — V1 provider-failure state boundary.

## Purpose

Prevent a claimed retry command from remaining silently in EXECUTION_IN_PROGRESS when the execution provider raises before returning an outcome.

## V1 Contract

When provider execution raises:
- attempt to transition the command to REQUIRES_MANUAL_REVIEW;
- return PROVIDER_FAILURE;
- preserve the explicit failure code `provider_execution_failed`.

If persistence of the manual-review transition fails:
- do not invent a new persisted state;
- retain the in-memory claimed command;
- return PROVIDER_FAILURE;
- expose `provider_failure_persistence_failed`.

## Boundary

This does not retry automatically, compensate, reschedule, classify provider failures, or mutate authorization/policy.