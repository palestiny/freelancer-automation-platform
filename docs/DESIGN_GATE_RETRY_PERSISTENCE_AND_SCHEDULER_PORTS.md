# Design Gate — Retry Persistence & Scheduler Ports

**Status:** APPROVED — V1 application boundary.

## Purpose
Introduce the smallest runtime-neutral boundary between a durable retry-command store and a replaceable scheduler. The boundary creates at most one logical retry command for a request/idempotency/attempt identity and records explicit scheduler acknowledgement.

## V1 Contract
1. accept only a RETRY recovery handoff;
2. derive the next attempt number from the immutable observed attempt count;
3. create a durable RetryCommand identity;
4. call RetryCommandStore.create_or_get before scheduling;
5. schedule only a command that is not already durably scheduled/completed/manual-review/stale;
6. record ACCEPTED, REJECTED, or AMBIGUOUS scheduler acknowledgement;
7. never retry scheduling speculatively after AMBIGUOUS;
8. never execute the provider.

## Idempotency
The logical scheduling key is (request_id, idempotency_key, attempt_number). command_id identifies the command record but does not replace the logical retry identity. Repeated calls with the same logical identity must reuse the durable command returned by the store.

## Concurrency
Atomic claiming remains a store concern. This service does not simulate locking or claim ownership in memory.

## Boundary
No concrete database, queue, scheduler, worker, provider adapter, authorization revalidation, or external side effect is introduced. Authorization revalidation immediately before provider execution remains the next execution boundary.