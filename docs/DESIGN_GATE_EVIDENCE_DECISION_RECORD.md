# Design Gate — Evidence Decision Record

**Status:** APPROVED — V1 explicit decision-record boundary.

## Purpose

Record an externally supplied business decision and its evidence lineage without allowing the domain to generate, authorize, or execute that decision.

## V1 Contract

An EvidenceDecisionRecord preserves:
- explicit business identity
- explicit decision outcome
- decision statement
- rationale
- evidence lineage
- decision timestamp
- decision-maker identity

V1 outcomes are deliberately bounded to ACCEPT, REJECT, and DEFER.

## Rules

1. Recording a decision is not generating a decision.
2. The domain does not infer authorization from the record.
3. Evidence references must be non-empty and unique.
4. Decision-maker identity is explicit.
5. The record is immutable.
6. No policy, lifecycle, learning, portfolio, capital, or execution state is mutated.
7. Financial execution is outside this boundary.
