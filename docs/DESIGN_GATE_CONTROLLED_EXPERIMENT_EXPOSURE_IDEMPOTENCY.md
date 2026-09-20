# Design Gate — Controlled Experiment Exposure Idempotency

**Status:** APPROVED — V1 retry-safe exposure recording semantics.

## Purpose

Make authoritative exposure recording safe under application retries without creating duplicate exposure evidence or silently accepting conflicting payloads.

## V1 Contract

For persisted exposure recording:

1. If `exposure_id` already exists with exactly the same authoritative assignment and exposure payload, return the existing exposure unchanged.
2. If `exposure_id` exists with different payload, reject the request as an exposure identity conflict.
3. If the assignment already has an exposure under a different exposure ID, reject the request as an assignment exposure conflict.
4. Only a genuinely new exposure is persisted.
5. Idempotency is application semantics; the repository uniqueness constraint remains authoritative protection against races.

This boundary does not schedule delivery, execute providers, infer causality, mutate experiment lifecycle, or change allocation.

## Rationale

Retries are expected in background/runtime systems. Treating an already-recorded identical exposure as a hard failure makes recovery noisy; treating a conflicting payload as success would hide evidence corruption. The contract therefore distinguishes safe replay from conflict.
