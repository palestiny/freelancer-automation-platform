# Opportunity History Repository Contract V1

**Status:** OWNER-APPROVED 2026-10-09; RED contract tests in progress. No production database selected.
**Parent gate:** [Opportunity History & Persistence V1 Design Gate](OPPORTUNITY_HISTORY_PERSISTENCE_V1_DESIGN_GATE.md)
**Decision context:** D-233 approved versioned opportunity revisions and immutable decision records, caller-owned identities, and embedded policy snapshots.

## 1. Scope and non-goals

Define stable repository semantics for normalized opportunity revisions and their associated immutable decision records. The contract is provider-neutral and must not depend on a specific database, API, UI, queue, or marketplace adapter.

This contract does not add event sourcing, batch ranking, evidence-registry semantics, evidence freshness guarantees, authorization, bidding, messaging, execution, payments, or policy mutation.

## 2. Record identities and relationships

All identity values are caller-supplied, non-empty strings. The repository must not generate replacement identities or infer identity from mutable content, title, source URL, or provider identity.

- **Opportunity identity:** stable parent identity.
- **Revision identity:** unique within its opportunity identity. A revision is immutable and contains the complete normalized `Opportunity` snapshot plus its caller-supplied revision ID.
- **Decision identity:** globally unique within the repository contract. A decision record references one exact opportunity identity and revision identity.
- **Evaluation identity:** preserve the caller-supplied `evaluation_ref` from the pipeline result; it is lineage, not a substitute for decision identity.
- **Policy snapshots:** each decision record contains the complete evaluation-policy and prioritization-policy definitions supplied to the pipeline, not only their IDs and versions.

The repository must reject a decision whose referenced revision does not exist. The record must also reject identity/lineage mismatches: the result's `priority_decision.opportunity_ref` must equal the record's opportunity identity, and the stored evaluation reference must equal the result's `priority_decision.evaluation_ref`.

Identity validation is **non-blank but non-normalizing**: reject strings whose `strip()` result is empty, while preserving every accepted identifier exactly as supplied. Do not silently trim, case-fold, or Unicode-normalize identities.

The repository/use-case boundary must also verify that the supplied policy snapshots match the identities and versions embedded in the result: evaluation policy ID/version must match both the evaluation and priority decision; prioritization policy ID/version must match the priority decision. A mismatch is a validation error before persistence.

A decision's revision link must mean the exact normalized `Opportunity` snapshot passed to evaluation—not merely an unrelated revision sharing the same caller-supplied ID. The repository alone cannot prove this from `OpportunityDecisionResult`, because that result does not contain the input `Opportunity`. Therefore the application use case must load the referenced persisted revision and pass that exact stored snapshot to `OpportunityDecisionPipeline`, or otherwise compare an explicit canonical fingerprint of the evaluated input with the revision before saving. Do not claim exact revision lineage if neither verification path is used. This orchestration remains outside the pure pipeline and does not add provider I/O or side effects to it.

Revision IDs are scoped to their parent opportunity identity. Reusing a revision ID under the same parent with equivalent canonical content is idempotent; reusing it with different canonical content is a conflict. A revision ID under another parent is a distinct scoped identity. Decision IDs are global; reusing one for a different opportunity, revision, result, or policy snapshot is a conflict.

## 3. Canonical content equivalence and idempotency

Idempotency compares the entire persisted logical record except the repository-assigned `recorded_at` value. For a retry, the existing record's original `recorded_at` is returned unchanged.

Canonicalization V1 rules:

1. Serialize a typed, versioned envelope; do not serialize Python objects with pickle or depend on Python `repr()`, object identity, or incidental dataclass field traversal.
2. Use explicit stable type tags for supported domain types and an explicit serializer version. Unknown type tags or unsupported schema versions fail closed; they are not silently coerced.
3. Encode enums by their declared string value and preserve the enum type tag.
4. Encode dataclasses only through an explicit, versioned serializer registry that enumerates the allowed type tag and exact field names for each supported domain type. Do not derive the persisted field manifest dynamically from dataclass reflection. Unknown domain types or fields fail closed. Object/map keys are emitted in lexicographic Unicode code-point order; object key order therefore does not affect equivalence.
5. Preserve tuple/list order because policy criteria, constraints, criterion results, rationale lists, and snapshots can carry meaningful sequence order.
6. Canonicalize `frozenset` values by canonicalizing each element and sorting by its canonical encoded representation. Duplicates are invalid where the domain type already defines uniqueness.
7. Encode `Decimal` values as normalized base-10 strings without exponent notation or insignificant trailing fractional zeros; normalize all signed zero forms to `"0"`. Do not pass Decimal values through binary floating point.
8. Encode aware datetimes as UTC ISO-8601 with fixed microsecond precision and a `Z` suffix. Equivalent instants with different UTC offsets are equivalent; naive datetimes and datetimes whose `utcoffset()` is `None` are rejected.
9. Encode `None`, booleans, strings, integers, and floats with distinct type tags so values such as integer `1` and float `1.0` cannot collide. Encode finite floats as their exact hexadecimal representation using the language's standardized float-hex conversion; reject NaN and infinities. String values are not trimmed or case-folded for equality.
10. For `Evidence.value` or any other `Any`-typed field, support only recursively JSON-compatible primitives, finite floats, lists/tuples, and string-keyed mappings under these rules. Unsupported runtime objects fail explicitly rather than being stringified or dropped.
11. Use UTF-8 canonical JSON with compact separators and no insignificant whitespace. Unicode strings are preserved as provided; no implicit Unicode normalization is applied.

The repository compares canonical logical content, not raw serialized bytes supplied by a caller. An identical identity + equivalent content returns the existing immutable record. An identity collision with non-equivalent content raises an explicit conflict and never overwrites the stored record. Validation/canonicalization failure happens before any record is committed.

## 4. Snapshot envelope and compatibility

Persist each domain snapshot inside an envelope with:
- a stable record-kind tag (`opportunity_revision` or `opportunity_decision`);
- a positive integer schema version for that record kind;
- the canonical payload;
- the original caller-supplied identities and lineage fields;
- repository-assigned timezone-aware `recorded_at`.

The V1 payload explicitly represents all persisted fields of the normalized `Opportunity`, `OpportunityEvaluation`, `OpportunityPriorityDecision`, `EvaluationPolicy`, and `PrioritizationPolicy`, including nested constraints/rules, enum values, Decimal amounts, ordered tuples, criterion snapshots, reasons, evidence refs, and evaluated-at time. Optional values remain explicit as null rather than being omitted based on truthiness.

Deserializer behavior is fail-closed for unknown schema versions, missing required fields, unexpected type tags, invalid enum values, malformed decimals, invalid timestamps, or unsupported values. Do not silently default a missing historical field to a new current default. Any future migration must be explicit, versioned, deterministic, and tested; it must not rewrite the original historical meaning invisibly.

A round-trip guarantees domain-semantic equivalence under the canonicalization rules, not preservation of original timezone-offset spelling, JSON whitespace, Python object identity, or dictionary insertion order.

## 5. Recorded time and deterministic history

The persistence boundary assigns `recorded_at` once, on first successful acceptance of a record, using an injected clock so tests are deterministic. The timestamp must be timezone-aware and normalized to UTC for storage and comparison. A retry returns the original timestamp; it never refreshes it.

Preserve `OpportunityPriorityDecision.evaluated_at` as decision time. Never replace it with `recorded_at`. Revisions and decisions each have their own recorded-at timestamp.

Revision history order is ascending by (`recorded_at` UTC instant, revision ID). Decision history order is ascending by (`recorded_at` UTC instant, decision ID). The corresponding latest-recorded view is the final item in that deterministic order. `get_latest_opportunity_revision` and any latest-decision projection use these same rules; “latest” means latest accepted by this repository, not source-current, freshest, or causally latest. IDs are tie-breakers only: if timestamps tie, ordering is deterministic but does not claim which event happened causally later. Do not use database row order, insertion order without a persisted timestamp, or lexicographic ID as the primary chronological signal.

## 6. Minimum repository operations

The provider-neutral repository port must expose behavior equivalent to:

- `save_opportunity_revision(opportunity_id, revision_id, opportunity)`
- `get_opportunity_revision(opportunity_id, revision_id)`
- `list_opportunity_revisions(opportunity_id)`
- `get_latest_opportunity_revision(opportunity_id)` — returns the final revision under the deterministic recorded-at ordering above, or an explicit not-found result when no revision exists; this means latest-recorded, not necessarily latest at the provider/source
- `save_decision(decision_id, opportunity_id, revision_id, evaluation_policy, prioritization_policy, result)`
- `get_decision(decision_id)`
- `list_decisions(opportunity_id)`

Exact Python method signatures may follow existing project conventions, but must preserve these identities and invariants. Return values must distinguish newly created records from idempotent replays only if callers need that distinction; either way, the stored record returned for an idempotent replay must be the original record. Missing records should have an explicit not-found result/exception, never a fabricated empty record.

V1 guarantees single-record idempotency and immutable record semantics. It does not claim atomic transactions spanning a revision save and a decision save, multi-process linearizability, distributed locking, or crash durability until an adapter-specific contract and tests establish those properties.

## 7. Evidence and policy lineage boundary

Persist exactly the evaluation and prioritization artifacts that the current `OpportunityDecisionPipeline` returns, together with the full policy snapshots supplied to that call. This includes evaluation criteria outcomes, evidence references, missing-evidence entries, uncertainty, rationale, priority reasons/rule IDs/tier, policy identities and versions, and decision time.

**Important model limitation:** the current `OpportunityDecisionResult` does not contain the original `EvaluationContext` or its `Evidence` objects, evidence values/provenance/quality, or the applicability mapping. The repository must not fabricate those values or claim they were preserved. Capturing complete evidence/context snapshots would require a separately designed and approved pipeline-result extension; it is outside this repository contract.

Evidence references remain references. Persisting a reference or a historical quality label does not prove that the target is resolvable, current, authoritative, or fresh. Retrieval returns the stored historical record and must not re-evaluate it or resolve current policy definitions in its place.

## 8. Verification matrix before adapter work

Tests must establish:

1. Canonical equivalence is stable under mapping key order and canonical JSON formatting whitespace; whitespace inside string values remains significant and is not trimmed.
2. Tuple order remains significant; set/frozenset order does not.
3. Decimal, exact finite-float, and aware-datetime canonicalization follows the rules above; naive timestamps, datetimes without a valid UTC offset, non-finite floats, unsupported values, and malformed decimals fail closed.
4. Exact retry returns the original record and original `recorded_at`; conflicting identity reuse raises without mutation.
5. Revisions are immutable and scoped to opportunity identity.
6. A decision cannot be saved before its referenced revision exists; mismatched opportunity/evaluation lineage is rejected.
7. Histories are deterministic when timestamps tie, and latest-recorded is not described as freshest or causally latest.
8. All current domain and policy fields round-trip, including nested constraint/rule values and enum/Decimal values.
9. Unknown/missing schema fields fail closed; compatibility changes require explicit versioned migration tests.
10. The repository boundary has no provider/network I/O and does not evaluate, prioritize, rank batches, authorize, or execute.
11. Tests against an in-memory adapter establish only in-process contract behavior; storage-specific durability/concurrency claims require tests against the actual adapter.

## 9. Implementation boundary

After this contract is accepted, implement RED tests for the repository port and canonical codec first, then the smallest provider-neutral repository port and a replaceable reference adapter selected explicitly in a separate decision. Keep persistence separate from `OpportunityDecisionPipeline`. Do not choose a production database or add API/UI/provider integration as part of this increment.
