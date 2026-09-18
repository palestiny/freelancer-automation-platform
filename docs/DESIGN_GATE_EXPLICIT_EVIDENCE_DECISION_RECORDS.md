# Design Gate — Explicit Evidence Decision Records

**Status:** APPROVED — V1 decision-record boundary.

## Purpose

Preserve an explicit decision made from available evidence without allowing the evidence layer to make or execute that decision.

## V1

A decision record contains:
- business identity
- decision id
- decision outcome
- decision statement
- decision rationale
- evidence references
- decision timestamp
- decision maker identity

Outcomes:
- ACCEPT
- REJECT
- DEFER

## Rules

1. The record is an explicit decision artifact, not an inferred recommendation.
2. Evidence references are lineage only; evidence never silently determines the outcome.
3. No automatic decision generation is included.
4. No policy, lifecycle, portfolio, financial, or execution state is mutated.
5. Evidence references must be unique and non-empty.
6. The record preserves the decision maker identity and timestamp.
7. A future automated decision consumer requires a separate policy/design gate.
