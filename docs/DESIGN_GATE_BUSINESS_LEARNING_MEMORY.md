# Design Gate — Business Learning Memory

**Status:** APPROVED — V1 provider-independent append-only learning-memory artifact.

## Purpose

Create an explicit memory boundary for learning evidence already produced by the platform. Memory stores what was learned and why; it does not decide what policy should change.

## V1 Contract

A `BusinessLearningMemoryEntry` preserves:
- business identity
- metric/unit context when applicable
- learning category
- statement
- source observation lineage
- source handoff identity
- recorded timestamp
- evidence quality

Learning categories:
- POLICY_REVIEW
- EXPERIMENT

## Rules

1. Only an existing EvidenceLearningHandoff may create a memory entry.
2. The handoff must already be eligible.
3. Memory is append-only at the domain contract level; entries are immutable.
4. Source observation lineage is mandatory and unique.
5. Memory does not mutate policy, lifecycle, portfolio, economics, or execution.
6. Memory does not rank, score, deduplicate, infer causality, or select actions.
7. Business isolation is mandatory.
8. Persistence, querying, retention, and cross-business aggregation are outside V1.
9. The recorded timestamp is supplied explicitly; the domain does not read the clock.
