# Design Gate — Controlled Experiment Outcome Summary

**Status:** APPROVED — V1 descriptive experiment outcome evidence.

## Purpose

Provide a deterministic, non-causal summary of observed experiment outcomes by variant after evidence readiness.

## V1 Contract

For one experiment and one metric, summarize only usable observations:
- count
- average
- minimum
- maximum
- average evidence quality
- observation lineage

The experiment summary also preserves:
- experiment identity
- metric identity
- variant summaries
- readiness identity

## Rules

1. This is descriptive evidence only.
2. No causal inference.
3. No statistical significance calculation.
4. No winner selection or ranking.
5. No experiment lifecycle mutation.
6. No automatic decision.
7. All variants remain visible; missing/insufficient variants are explicit.
8. Observations from another experiment or metric are rejected.
9. Evidence-quality filtering is explicit.
10. Raw observation IDs remain authoritative lineage.
