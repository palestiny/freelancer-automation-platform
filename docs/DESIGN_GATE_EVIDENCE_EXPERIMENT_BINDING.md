# Design Gate — Evidence-to-Experiment Binding

**Status:** APPROVED — V1 explicit identity binding for experiment handoffs.

## Purpose

Replace free-form experiment targeting with an explicit, provider-independent binding between an eligible evidence handoff and a concrete validation experiment.

## V1 Contract

Inputs:
- an existing `EvidenceLearningHandoff`
- a `ValidationExperiment`

Rules:
1. The handoff type must be `EXPERIMENT`.
2. The handoff target must exactly equal the experiment ID.
3. The experiment must be identified explicitly; no lookup or inference is performed.
4. The binding preserves handoff identity, experiment identity, business/metric/unit context, and observation lineage.
5. Binding does not start, modify, complete, or cancel an experiment.
6. Binding does not authorize spend or execution.
7. A policy-review handoff cannot be rebound as an experiment.
8. Experiment lifecycle remains owned by `ValidationExperiment`.

The binding is traceability infrastructure, not an experiment result and not an authorization artifact.
