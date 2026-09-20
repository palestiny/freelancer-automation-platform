# Design Gate — Business Learning Memory Query

**Status:** APPROVED — V1 provider-independent read/query boundary over immutable learning memory.

## Purpose

Make existing business learning memory usable by downstream learning and review consumers without adding persistence, ranking, inference, or automatic policy mutation.

## V1 Contract

Query filters:
- business identity (required)
- optional metric and unit
- optional handoff category
- optional inclusive start / exclusive end time window

Results:
- matching immutable memory entries
- deterministic chronological ordering
- no score or ranking

## Rules

1. Business isolation is mandatory.
2. Query does not mutate memory.
3. Query does not infer causality or effectiveness.
4. Query does not rank memories.
5. Query does not select policy changes.
6. Query does not require a persistence implementation; it operates on supplied memory entries.
7. Duplicate entry IDs are invalid input.
8. Query windows use the existing start-inclusive/end-exclusive convention.
