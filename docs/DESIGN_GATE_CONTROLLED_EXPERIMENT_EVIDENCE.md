# Design Gate — Controlled Experiment Evidence

**Status:** APPROVED — V1 provider-independent experiment allocation and observation evidence.

## Purpose

Turn the existing validation-experiment domain into an evidence-producing boundary without introducing a queue, scheduler, provider execution, automatic allocation, or statistical method.

## V1 Contract

A planned experiment may define explicit variants. A consumer may record an immutable assignment and an immutable observed result for one experiment subject.

The domain records:
- experiment identity
- subject identity
- selected variant
- assignment timestamp
- observation identity
- observed metric/value
- observation timestamp
- evidence quality

## Rules

1. Variant selection is explicit input; the domain does not randomize or optimize allocation.
2. Assignment and observation are evidence artifacts, not execution commands.
3. Observations must reference an existing experiment identity and explicit variant.
4. Cross-experiment mixing is rejected.
5. Duplicate assignment identity and duplicate observation identity are rejected.
6. No causal inference is performed.
7. No statistical significance is calculated.
8. No experiment lifecycle mutation is performed by evidence recording.
9. No provider, queue, scheduler, persistence, or external execution dependency is introduced.
10. Later analysis may consume these artifacts through a dedicated design gate.
