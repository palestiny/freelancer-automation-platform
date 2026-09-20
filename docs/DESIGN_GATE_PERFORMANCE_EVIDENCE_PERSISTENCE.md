# Design Gate — Performance Evidence Persistence

**Status:** APPROVED — V1 durable persistence boundary for authoritative performance observations.

## Problem

The domain/runtime can now produce evidence, statistical analysis, learning handoffs, and execution outcomes, but authoritative performance observations are not yet durably stored behind an explicit persistence boundary.

## V1 Scope

Persist only the authoritative normalized `BusinessPerformanceObservation` records.

Derived artifacts such as:
- aggregates
- trends
- statistical results
- evidence composition
- learning signals

remain recomputable from authoritative observations and are not required to be persisted in this first slice.

## Contract

### Domain boundary

The domain remains persistence-agnostic.

### Application port

Introduce a repository contract with:
- save observation
- get observation by id
- list observations for one business
- preserve source identity, metric/unit, expected/actual values, timestamp, and evidence quality
- reject duplicate observation IDs
- reject cross-business writes where the repository is business-scoped

Repository methods must not perform domain interpretation, scoring, statistical analysis, policy evaluation, or execution.

### Infrastructure adapter

Provide a reference SQLite adapter using Python's standard library `sqlite3`.

SQLite is a reference/local durable adapter, not a commitment that production deployment must use SQLite. A future PostgreSQL or other adapter must satisfy the same application contract.

## Transaction / consistency rules

1. An observation write is atomic.
2. Duplicate IDs fail explicitly.
3. Reads return normalized domain observations.
4. Stored data must preserve exact source identity and evidence values.
5. Persistence failures must not be converted into successful domain outcomes.
6. No external provider call occurs inside the repository.
7. No automatic retry is introduced by the repository.

## Explicit non-goals

- generic ORM
- event sourcing
- CQRS
- migrations framework
- production database selection
- API/UI
- background workers
- caching
- cross-business analytics
- automatic policy mutation
- statistical recomputation during persistence

## Test strategy

RED tests cover:
- round-trip persistence
- duplicate rejection
- business isolation
- nullable expected value
- evidence-quality preservation
- timestamp/source/metric/unit preservation

Then implement the smallest adapter and contract needed to turn RED green.
