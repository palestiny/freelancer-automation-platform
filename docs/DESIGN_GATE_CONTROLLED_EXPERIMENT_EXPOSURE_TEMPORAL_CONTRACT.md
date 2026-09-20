# Design Gate — Controlled Experiment Exposure Temporal Contract

**Status:** APPROVED — V1 temporal validity hardening for authoritative exposure recording.

## Rule

An experiment exposure cannot occur before the authoritative assignment.

For both exposure-recording application boundaries:
- exposed_at must be timezone-aware.
- the authoritative assignment timestamp must be timezone-aware.
- exposed_at >= assigned_at is required.
- invalid temporal input is rejected before persistence.

This is evidence-integrity validation only. It does not prove delivery, causality, experiment success, or lifecycle state.

## Boundary

The application service owns the cross-entity temporal rule because ExperimentExposure intentionally does not duplicate assignment timestamp data.

No provider execution, scheduling, lifecycle mutation, statistical inference, or automatic experiment decision is introduced.
