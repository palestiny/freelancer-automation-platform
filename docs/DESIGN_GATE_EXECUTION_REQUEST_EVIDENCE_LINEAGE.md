# Design Gate — Prepared Execution Request Evidence Lineage

**Status:** APPROVED — V1 traceability hardening.

## Purpose

Preserve the evidence lineage that produced an authorization when that authorization is converted into a prepared execution request.

## Contract

A prepared request preserves current, baseline, and statistical observation IDs together with policy identity/version, action class, autonomy, request identity, and idempotency identity.

## Rules

1. Preparation remains non-executing.
2. Lineage is copied from the authoritative authorization; callers cannot supply replacement evidence IDs.
3. Observation IDs remain unique within each lineage group.
4. Policy identity/version remain bound to the authorization.
5. This does not add authorization, freshness, retry, scheduling, or provider behavior.
