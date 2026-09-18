# Design Gate — Statistical Evidence Composition & Decision Support

**Status:** APPROVED — V1 downstream consumer of the existing Phase 17 statistical surface.

## Purpose

Provide a bounded, provider-independent consumer that composes an existing statistical result with the existing evidence-quality and source-reliability context without creating a universal score or silently changing policy.

## Concrete Use Case

A business performance comparison may already have:
- a deterministic descriptive comparison,
- a Welch statistical result,
- observation-level evidence quality,
- source-reliability eligibility.

The platform needs one explicit evidence artifact answering:

> Is the statistical result usable as decision-support evidence, and what does the statistical test report?

This is evidence composition, not an automatic business decision.

## V1 Contract

Inputs:
- an existing `MeanComparisonResult`,
- current evidence quality,
- baseline evidence quality,
- current source-reliability assessment,
- baseline source-reliability assessment,
- an explicit minimum evidence-quality threshold.

Outputs:
- statistical applicability,
- evidence eligibility,
- explicit reason when evidence is not eligible,
- statistical interpretation based only on the supplied Welch result,
- preserved statistical method identity and observation lineage.

V1 interpretations:
- `STATISTICALLY_DETECTED_DIFFERENCE`
- `NO_STATISTICALLY_DETECTED_DIFFERENCE`
- `STATISTICAL_RESULT_NOT_APPLICABLE`

V1 evidence eligibility reasons:
- `ELIGIBLE`
- `STATISTICAL_RESULT_NOT_APPLICABLE`
- `INSUFFICIENT_EVIDENCE_QUALITY`
- `INSUFFICIENT_SOURCE_RELIABILITY`

## Rules

1. A statistical result is never treated as a fact replacing raw observations.
2. Statistical significance does not override evidence quality or source reliability.
3. No universal score, rank, business posture, or action is produced.
4. No policy, learning signal, lifecycle, portfolio, or execution state is mutated.
5. No automatic statistical method selection or fallback is introduced.
6. The consumer does not reinterpret p-values beyond the committed Welch result and alpha already carried by the result.
7. Statistical applicability remains distinct from evidence eligibility.
8. Current and baseline evidence quality are both required.
9. Both source-reliability assessments must be eligible.
10. Observation lineage and method provenance are preserved.

## Decision Gate

This use case is intentionally narrow. It consumes the existing Phase 17 Welch result; it does not add another statistical method. RED tests must cover inapplicable results, insufficient evidence quality, insufficient source reliability, eligible non-significant results, and eligible statistically detected differences.
