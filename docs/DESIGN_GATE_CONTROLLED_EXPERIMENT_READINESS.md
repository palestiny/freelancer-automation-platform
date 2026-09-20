# Design Gate — Controlled Experiment Evidence Readiness

**Status:** APPROVED — V1 evidence sufficiency/readiness assessment for controlled experiments.

## Purpose

Determine whether collected experiment evidence is sufficient to hand off to an existing analysis consumer, without performing statistical inference or changing experiment lifecycle.

## V1 Contract

Inputs:
- one ValidationExperiment
- immutable assignments
- immutable observations
- minimum observations per declared variant
- minimum evidence quality

Outputs:
- COLLECTING
- READY
- INVALID_CONTEXT

## Rules

1. Every assignment and observation must belong to the supplied experiment.
2. Every assigned/observed variant must be declared by the experiment.
3. Observation assignment lineage must match assignment subject and variant.
4. Assignment and observation identities must be unique within the supplied evidence.
5. Every declared variant must reach the minimum usable observation count.
6. Evidence quality is a readiness gate, not rewritten evidence.
7. Readiness does not calculate significance, effect, causality, or winner/loser.
8. Readiness does not mutate experiment lifecycle or decision state.
9. Empty variants or an experiment without at least one declared variant are invalid context.
10. The result is an evidence artifact that can hand off to a dedicated analysis consumer.
