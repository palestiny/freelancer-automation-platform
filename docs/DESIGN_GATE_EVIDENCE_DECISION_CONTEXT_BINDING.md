# Design Gate — Evidence Decision Context Binding

**Status:** APPROVED — V1 explicit binding between decision context and decision record.

## Purpose

Provide a narrow factory that records an explicitly supplied decision against a previously built EvidenceDecisionContext while preserving the context's business identity and evidence lineage.

## V1 Contract

Inputs:
- EvidenceDecisionContext
- explicit DecisionOutcome
- explicit statement
- explicit rationale
- explicit decision-maker identity
- explicit decision record ID
- explicit timezone-aware decision timestamp

Output:
- EvidenceDecisionRecord

The factory derives evidence references from the context:
- source references
- statistical observation IDs
- current observation IDs
- baseline observation IDs

Duplicate references are collapsed while preserving first-seen order.

## Rules

1. The decision outcome is supplied by the caller; it is never inferred.
2. Business identity comes from the context and cannot be independently overridden.
3. Evidence lineage comes from the context; callers cannot replace it with an unrelated business's evidence.
4. No authorization is inferred.
5. No policy, lifecycle, learning, portfolio, capital, or execution state is mutated.
6. The record remains immutable.
7. This is a construction/binding boundary, not a recommendation engine.
