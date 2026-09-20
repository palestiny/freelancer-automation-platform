# Design Gate — Controlled Experiment Variant Comparison

**Status:** APPROVED — V1 bounded descriptive comparison consumer.

## Purpose

Compare two declared experiment variants descriptively using the existing ready outcome summary without selecting a winner or calculating statistical significance.

## V1 Contract

Inputs:
- a `ControlledExperimentOutcomeSummary`
- two distinct declared variant names

Outputs:
- experiment and metric identity
- first/second variant identity
- each variant average and count
- absolute average difference
- relative average difference when the first average is non-zero
- observation lineage for both variants
- explicit applicability status

Statuses:
- APPLICABLE
- VARIANT_NOT_FOUND
- SAME_VARIANT
- INSUFFICIENT_VARIANT_EVIDENCE
- INCOMPATIBLE_CONTEXT

## Rules

1. This is descriptive evidence only.
2. No winner, ranking, recommendation, statistical significance, causal claim, experiment lifecycle mutation, or execution.
3. Difference direction is neutral; it must not imply better/worse.
4. The comparison preserves both variant identities and observation lineage.
5. Relative difference is unavailable when the first average is zero.
6. The existing outcome summary remains authoritative; this consumer does not recompute raw observations.
