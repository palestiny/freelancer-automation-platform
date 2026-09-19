# Design Gate — Explicit Evidence Decision Record

**Status:** APPROVED — V1 non-generating decision record.

## Purpose

Preserve a human or authorized consumer's explicit decision against already-composed evidence without allowing the domain to generate or execute that decision.

## V1 Contract

A decision record contains:
- unique decision id
- business id
- decision maker identity
- decision timestamp
- outcome
- statement
- rationale
- evidence references
- evidence context

The domain validates structure and lineage only.

## Rules

1. The domain records an explicit decision; it never chooses the outcome.
2. A decision must reference at least one evidence artifact.
3. Evidence references are opaque IDs; the record does not reinterpret them.
4. Duplicate evidence references are rejected.
5. Decision timestamps must be timezone-aware so audit ordering is unambiguous.
5. Empty statements/rationales are rejected.
6. No policy, lifecycle, learning signal, portfolio posture, capital allocation, or execution state is mutated.
7. No score, ranking, recommendation, or automatic decision is produced.
8. This record is compatible with future approval/audit infrastructure but does not implement persistence or authorization.
