# Design Gate — Evidence Decision Context Validation

**Status:** COMPLETED — V1 validation hardening.

## Purpose

Keep the EvidenceDecisionContext as a trustworthy immutable evidence-binding boundary by rejecting malformed identity, lineage, and provenance values before an evidence decision can be recorded.

## V1 Contract

The context must reject:

- non-string or blank business/metric/unit identity fields;
- non-tuple observation lineage collections;
- empty observation lineage collections;
- blank or non-string observation identifiers;
- duplicate observation identifiers;
- non-tuple source-reference collections;
- blank or non-string source references;
- duplicate source references;
- evidence-quality values outside 0–100.

## Boundary Rules

1. Validation is structural; it does not infer business meaning.
2. Validation does not generate or recommend a decision.
3. Validation does not infer authorization.
4. Validation does not mutate policy, learning, lifecycle, portfolio, or execution state.
5. Evidence lineage remains explicit and provider-independent.

## Verification

RED tests were added for malformed lineage/provenance and invalid identity types, followed by the minimal implementation change. CI verification is required before merging.
