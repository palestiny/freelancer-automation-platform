# Design Gate — Controlled Experiment Exposure Assignment Authority

**Status:** APPROVED — V1 exposure recording must resolve the authoritative persisted assignment before recording exposure.

## Problem

The current exposure application service accepts an assignment object directly. That allows a caller to construct an assignment-shaped value without proving it is the authoritative persisted assignment.

## Decision

Exposure recording will resolve the assignment through the application assignment repository using assignment identity.

The service will:
1. require an assignment repository and exposure repository;
2. load the assignment by ID;
3. reject missing assignments;
4. construct exposure only from the persisted assignment;
5. persist exactly one exposure for that assignment.

## Boundary

This is lineage hardening only. It does not schedule exposure, execute providers, randomize allocation, optimize allocation, infer causality, or mutate experiment lifecycle.
