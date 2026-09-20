# Design Gate — Controlled Experiment Exposure-to-Outcome Linkage

**Status:** APPROVED — V1 temporal/evidence linkage boundary.

## Purpose

Create an explicit evidence artifact linking an observed experiment outcome to a recorded exposure without treating temporal linkage as causal attribution.

## V1 Contract

The linkage preserves:
- experiment identity
- assignment identity
- exposure identity
- subject identity
- variant identity
- outcome observation identity
- exposure timestamp
- outcome timestamp

Rules:
1. All identities are non-empty.
2. Exposure and outcome belong to the same experiment, subject, and assigned variant.
3. Outcome observation time must not precede exposure time.
4. Linkage identity is immutable and caller-provided.
5. One linkage identity represents one explicit exposure/outcome relationship.
6. Temporal linkage is evidence provenance only; it does not establish causality.
7. No statistical analysis, winner selection, lifecycle mutation, allocation change, policy mutation, authorization, or execution occurs.

## Boundary

This is a domain evidence contract. Persistence, querying, causal attribution, statistical inference, and provider delivery remain separate boundaries.
