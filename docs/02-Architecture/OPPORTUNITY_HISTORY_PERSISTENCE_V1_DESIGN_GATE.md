# Opportunity History & Persistence V1 — Design Gate

**Status: OWNER-APPROVED MODEL — DETAILED V1 CONTRACT DOCUMENTED; CONTRACT REVIEW REQUIRED BEFORE ADAPTER IMPLEMENTATION**  
**Scope:** Provider-independent persistence and retrieval contract for normalized opportunities and their immutable evaluation/prioritization history.  
**Parent capability:** Opportunity Intelligence V1 + Opportunity Decision Pipeline V1  
**Current baseline:** Decision pipeline is implemented and merged via PR #489. It evaluates and prioritizes one already-normalized `Opportunity` in memory; it does not persist records.  
**Out of scope:** Database/vendor selection, API/UI, marketplace adapters, provider polling, automatic ranking across opportunities, authorization, bidding, messaging, execution, and policy mutation.

## 1. Problem

The application can produce an immutable evaluation and priority decision for one normalized `Opportunity`, but it cannot yet answer durable questions such as:

- What opportunity snapshot was evaluated at that time?
- Which evaluation and prioritization policy versions produced the result?
- What evidence references and evidence-quality states supported the result?
- How did the opportunity or its decisions change over time?
- Can a caller safely retry a save without duplicating history or silently overwriting a conflicting record?
- Can a historical decision be retrieved without accidentally presenting it as the current assessment?

Adding persistence before answering these questions risks losing lineage, treating an old decision as current, or binding the domain to a database/API too early.

## 2. Decision required

Choose the V1 persistence model and approve its invariants before implementation.

### Option A — Decision snapshots only

Persist each combined pipeline result together with the normalized opportunity snapshot used to produce it.

- **Benefits:** small contract; preserves what was evaluated; straightforward historical retrieval.
- **Costs / risks:** opportunity identity and current-state discovery become awkward; repeated snapshots duplicate data; updates to opportunity details do not have a first-class revision lifecycle.
- **Disposition:** viable for a narrow audit log, but insufficient if the product needs a durable opportunity workspace.

### Option B — Versioned opportunity history plus immutable decision records (recommended)

Persist a stable opportunity identity, append-only normalized opportunity revisions, and immutable decision records that reference the exact opportunity revision and policy/evidence lineage. Any “current opportunity” or “latest decision” view is a query/projection over these records, not a mutation of historical decisions.

- **Benefits:** preserves the evaluated input, supports history and current-state queries, and separates identity from revisions and assessments.
- **Costs / risks:** requires explicit revision identity, conflict/idempotency semantics, and clear rules for determining “latest.”
- **Disposition:** recommended V1 foundation, without committing to a specific database or event-sourcing framework.

### Option C — Full event-sourced opportunity lifecycle

Persist every lifecycle transition as a domain event and rebuild all state from the event stream.

- **Benefits:** strong temporal reconstruction and extensibility for complex lifecycle workflows.
- **Costs / risks:** introduces event schemas, projection/replay rules, migration/versioning obligations, and operational complexity before a concrete lifecycle requirement exists.
- **Disposition:** defer; V1 history does not require full event sourcing.

## 3. Recommended V1 boundary

If Option B is approved, the first implementation should introduce provider-neutral application repository ports and a replaceable reference adapter only after the owner approves the contract.

### Records and identity

1. **Opportunity identity:** stable, non-empty caller-supplied identifier; not inferred from title, URL, provider name, or mutable content.
2. **Opportunity revision:** immutable snapshot of the canonical normalized `Opportunity`, with a stable revision identifier and explicit recorded-at timestamp.
3. **Decision record:** immutable combined `OpportunityDecisionResult`, with its own stable identity, the exact opportunity/revision identity, evaluation policy identity/version, prioritization policy identity/version, and the result's evidence lineage.
4. **Policy definitions:** each immutable decision record stores the exact immutable evaluation-policy and prioritization-policy snapshots (including IDs and versions) used to produce it. Retrieval must not resolve historical decisions against mutable current policy definitions.
5. **Evidence lineage:** preserve exact evidence references, missing-evidence entries, uncertainty, rationale, criterion outcomes, and priority snapshots that are actually present in the pipeline result. The current result does not carry full evidence quality/provenance/value or the EvaluationContext applicability map; do not invent or claim to preserve absent fields. See the detailed repository contract.

The repository contract must not assume that a provider URL is globally unique or stable. Provider-specific external identity belongs to a future adapter/mapping contract.

### Additional lineage invariants found during contract review

- Reject whitespace-only caller identities, but preserve accepted identity strings exactly; do not silently trim or case-normalize them.
- Verify that the complete evaluation and prioritization policy snapshots passed for persistence match the policy IDs and versions embedded in the combined pipeline result.
- A decision must reference the exact normalized opportunity revision that was evaluated. Since `OpportunityDecisionResult` does not contain the input `Opportunity`, the application use case must evaluate the loaded persisted revision itself or verify a canonical fingerprint of the evaluated input against that revision before saving. Matching identity strings alone is insufficient proof of snapshot lineage.


### History and retrieval

The contract should support, at minimum:

- save a new opportunity revision without mutating earlier revisions;
- save a decision record that references an existing, exact revision;
- retrieve an opportunity's revision history and latest-recorded revision projection by stable identity;
- retrieve revisions for one opportunity in deterministic order;
- retrieve one decision by identity;
- retrieve decision history for one opportunity;
- distinguish a historical decision from the latest recorded decision.

“Latest” must use an explicit persisted ordering rule (prefer a timezone-aware recorded-at timestamp plus a stable tie-break identity or sequence). It must not be inferred from lexicographic IDs, database row order, or client clock assumptions. A latest decision is merely the latest recorded assessment, not necessarily a fresh or valid assessment.

### Idempotency and conflicts

- Identical retries using the same record identity and equivalent canonical content should return the existing record without creating duplicate history.
- Reuse of an identity with conflicting content must fail explicitly; it must not overwrite the existing record.
- The implementation must define how canonical equivalence is checked without depending on incidental serialization order.
- A decision must not be saved as valid history if its referenced opportunity revision cannot be resolved.
- V1 should not imply multi-record transaction guarantees unless the repository port explicitly requires and tests them.

### Time, freshness, and policy history

- Persisted timestamps must be timezone-aware; naive timestamps are rejected rather than assigned an assumed timezone.
- Preserve the original decision/evaluation time and the persistence-recorded time as distinct concepts if both are present. Storage time must not replace the time at which the decision was made.
- Historical records remain immutable when a policy changes. Re-evaluation creates a new decision record; it does not rewrite the previous result.
- Reference freshness validation remains **unresolved** until an authoritative evidence-reference registry/contract exists. Persist evidence references and quality metadata only where those fields are actually present in the supplied pipeline artifacts. The current `OpportunityDecisionResult` preserves criterion outcomes and evidence references but does not carry evidence quality/provenance/value; persistence must not invent those fields or claim that a reference is currently resolvable, fresh, or authoritative.
- Retrieval must not silently re-evaluate an old decision or substitute current policy/evidence into a historical result.

## 4. Explicit non-goals and safety boundaries

This gate does not authorize:

- selecting or committing to SQLite, PostgreSQL, or another production database;
- adding API endpoints, UI/dashboard, background jobs, or provider polling;
- batch ranking or within-tier ordering;
- provider-specific payload mapping or live Freelancer integration;
- generated IDs when caller-supplied identity is part of the approved contract;
- evidence-registry implementation or a claim of evidence freshness;
- authorization, proposals, bidding, messaging, execution, payment, or policy/learning mutation.

The existing `OpportunityDecisionPipeline` remains a pure application composition boundary. Persistence should be a separate application use case, not hidden inside the pipeline.

## 5. Required tests before implementation

After the owner approves the gate and the detailed contract is finalized, tests should cover:

1. Stable opportunity identity is separate from revision and decision identity.
2. A decision references the exact normalized opportunity revision used for evaluation.
3. Earlier revisions and decision records remain unchanged after later saves.
4. Identical retry is idempotent; conflicting reuse of identity fails explicitly.
5. A decision referencing a missing or mismatched revision is rejected.
6. Historical retrieval is deterministic and clearly distinguishes historical from latest-recorded decisions.
7. Policy definitions/IDs/versions, evidence references, criterion snapshots, priority outcomes, and decision timestamps survive round-trip under the documented canonicalization rules; absent EvaluationContext/Evidence fields are not fabricated.
8. Naive timestamps and malformed identities fail closed.
9. Historical records are not silently re-evaluated under current policies.
10. The repository port does not perform provider I/O, authorize, rank batches, or execute actions.
11. Adapter tests prove behavior against its actual storage boundary; no production database guarantee is claimed from in-memory tests alone.

## 6. Owner choices

**Owner decision: APPROVED on 2026-10-09 (Decision D-233).**

- [x] **Persistence model:** Option B — versioned opportunity history + immutable decision records.
- [x] **Identity ownership:** caller supplies stable opportunity, revision, and decision identities; identity conflicts fail explicitly.
- [x] **Policy history:** embed immutable evaluation-policy and prioritization-policy snapshots in each decision record.
- [x] **Reference adapter:** defer technology selection until the repository contract is approved; no production database is selected.

The detailed implementation contract must still define canonical content equivalence, deterministic ordering/tie-breaking for history, and exact snapshot serialization/compatibility semantics. These details must be resolved before implementation, not guessed by an adapter.

## 7. Approval boundary

Approval authorizes only the selected persistence contract and follow-up implementation design. It does not authorize a production database choice, API/UI, marketplace integration, evidence registry, automatic ranking, or execution. The owner choices above are approved. The detailed repository contract has been documented in the linked companion file; adapter implementation remains gated on review of that contract. This approval does not authorize selecting a production database, implementing an evidence registry, or adding API/UI/provider integration.
