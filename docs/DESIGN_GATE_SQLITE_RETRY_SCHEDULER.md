# Design Gate — SQLite Retry Scheduler Adapter

**Status:** APPROVED — V1 durable scheduler adapter for the existing RetrySchedulerPort.

## Scope

Provide a concrete SQLite-backed scheduling adapter that records a retry command as durable scheduled work. It does not run workers and does not execute providers.

## Guarantees

1. Scheduling identity is unique per command identity.
2. Re-scheduling the same command returns the existing scheduling identity.
3. A scheduling record preserves command_id and attempt_number.
4. The adapter returns an explicit ACCEPTED acknowledgement after durable insertion/retrieval.
5. No scheduler acknowledgement is reported as accepted before persistence succeeds.
6. No provider execution occurs.
7. No retry policy is evaluated or mutated.
8. Scheduler storage remains replaceable through RetrySchedulerPort.

## Out of Scope

- worker polling/claiming
- queue delivery guarantees beyond SQLite persistence
- distributed scheduling
- execution
- authorization
- automatic retry decisions
