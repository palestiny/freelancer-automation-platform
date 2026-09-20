# Design Gate — Controlled Experiment Observation Exposure Lineage

**Status:** APPROVED — V1 attribution-safety boundary.

## Purpose

Ensure an experiment metric observation is explicitly attributable to an actual exposure context before downstream experiment evidence uses it.

## V1 Contract

Inputs:
- an ExperimentObservation
- an ExperimentExposure

The lineage check succeeds only when:
- experiment identity matches
- assignment identity matches
- subject identity matches
- variant matches
- observation occurs at or after exposure

Outputs are descriptive validation only:
- VALID
- INVALID_CONTEXT
- BEFORE_EXPOSURE

## Rules

1. Assignment alone is not evidence of exposure.
2. An observation is not exposure evidence.
3. This boundary does not infer causality.
4. It does not calculate significance, select winners, mutate lifecycle, allocate traffic, or execute providers.
5. Exposure remains an independent authoritative evidence artifact.
6. Temporal ordering is explicit and timezone-aware.
