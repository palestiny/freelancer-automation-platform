# Design Gate — Execution Outcome Temporal Contract

**Status:** APPROVED — V1 temporal integrity hardening for execution outcomes.

## Purpose

Ensure execution outcome observations are temporally valid relative to the prepared execution request without introducing clocks, scheduling, retries, or execution policy.

## Rules

1. observed_at must be timezone-aware.
2. When prepared_at exists, observed_at must not precede prepared_at.
3. The domain does not infer missing timestamps.
4. This contract validates evidence integrity only; it does not prove that execution happened at the provider at that exact time.
5. No automatic retry, freshness re-evaluation, authorization mutation, reconciliation, or provider behavior is introduced.
