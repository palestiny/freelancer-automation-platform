# Production Persistence — Design Gate

**Status: DRAFT — OWNER REVIEW REQUIRED**
**Decision ID:** TBD after owner approval
**Scope:** Requirements and acceptance criteria for selecting and integrating production persistence for Opportunity History & Persistence V1.
**Prerequisites:** D-233; Opportunity History Repository Contract V1; PR #491 reference implementation.
**Non-goal:** This gate does not select a database, approve a migration, or authorize production rollout.

## 1. Problem and current baseline

Opportunity History & Persistence V1 defines immutable opportunity revisions, immutable decision records, canonical serialization, idempotency/conflict semantics, and a provider-neutral repository port. The in-memory repository is a reference/conformance adapter only. It does not establish crash durability, cross-process coordination, or production recovery guarantees.

The production adapter must preserve the approved repository contract. Database-specific behavior must not leak into domain models or application ports.

## 2. Decisions required before selecting a technology

The owner must approve or explicitly defer each item below. Where requirements are unknown, record the uncertainty rather than silently choosing a vendor or assuming a deployment shape.

1. **Deployment topology:** single process, multiple application processes, multiple hosts, or horizontally scaled workers.
2. **Durability target:** acceptable loss window for acknowledged writes; whether acknowledged commits must survive process, host, and power failure.
3. **Concurrency:** expected concurrent readers/writers; whether multiple processes may append revisions or decisions concurrently.
4. **Availability and recovery:** required recovery time objective (RTO), recovery point objective (RPO), and behavior during storage unavailability.
5. **Data volume and retention:** expected opportunities, revisions, decisions, write/read rates, retention, and archival/deletion obligations.
6. **Operational environment:** local-first desktop/single-user pilot versus hosted service; managed database availability, operational skill, and cost constraints.
7. **Security:** tenant/business isolation, access control boundary, encryption requirements, secret handling, and audit access.
8. **Backup and restore:** backup frequency, retention, off-site requirements, restore testing, and integrity verification.
9. **Schema evolution:** migration ownership, forward/backward compatibility expectations, rollback policy, and recovery from partially applied migrations.
10. **Observability:** health/readiness signals, storage latency/error metrics, conflict rates, migration status, and audit-safe logging.
11. **Transactions and uniqueness:** atomic enforcement for globally unique decision IDs, opportunity-scoped revision IDs, foreign-key lineage, and same-identity/different-content conflicts.
12. **Portability:** required deployment targets and acceptable dependence on database-specific SQL or features.

## 3. Candidate evaluation — no choice pre-approved

Evaluate candidates against the approved requirements, not familiarity alone.

### Candidate A — SQLite
Potential fit: local-first, single-host pilot with modest write concurrency and simple operations.
Risks to validate: write serialization/locking under expected concurrency, backup consistency, multi-process deployment constraints, filesystem assumptions, and future hosted scaling.

**Existing repository precedent is not production proof.** The codebase already contains SQLite-backed retry command/scheduler adapters, but they serve different contracts. Their presence does not establish that their connection lifecycle, transaction boundaries, race handling, backup behavior, or concurrency characteristics satisfy Opportunity History invariants. In particular, `check_same_thread=False` only disables sqlite3's thread-affinity check; it is not itself a synchronization strategy. Review any reuse candidate against its full call paths and test cross-thread/process behavior under the intended topology. Do not copy an adapter or claim concurrency safety based solely on successful unit tests.

### Candidate B — PostgreSQL
Potential fit: hosted multi-process deployment, stronger concurrent writer support, centralized operations, and transactional constraints.
Risks to validate: operational/hosting cost, deployment and backup ownership, connection management, migrations, and local-development parity.

### Candidate C — Other managed relational/document storage
Consider only if a concrete requirement materially favors it. Document the operational and semantic trade-offs; do not introduce a new technology by default.

**Selection rule:** No candidate is selected by this draft. The owner chooses after deployment topology, durability, concurrency, operational ownership, and expected load are known. A local reference adapter or passing unit tests are not proof of production suitability.

## 4. Required adapter invariants

Any production adapter must pass the same provider-neutral repository contract tests and preserve these behaviors:

- Immutable opportunity revisions and decision records; no silent overwrite.
- Caller-supplied identity validation remains non-blank and non-normalizing.
- Revision identity is unique within its opportunity; decision identity is globally unique.
- Equivalent canonical retry is idempotent and returns the original repository-recorded timestamp.
- Reuse of an identity with different canonical content fails with a conflict and leaves the original record unchanged.
- Decision insertion requires an existing exact revision and validates opportunity/revision/result/policy lineage.
- Concurrent competing writes preserve uniqueness and conflict semantics at the storage boundary, not merely through process-local locks.
- Timestamps remain timezone-aware and history order follows the approved contract; identifiers are deterministic tie-breakers, not proof of causality.
- Unsupported serializer/schema versions fail closed; database rows must not bypass canonical validation.
- Transaction boundaries prevent partial decision records or broken revision references.
- Business/tenant isolation is enforced at the persistence boundary if multi-business data shares a database.
- Failure paths do not report success before durable commit semantics required by the approved durability target.

## 5. Required verification before production approval

### Contract and concurrency
- Run the complete shared repository conformance suite against every adapter.
- **Reusable contract baseline in draft PR #494:** `tests/contracts/opportunity_history_repository_contract_cases.py` exposes provider-neutral assertions behind a repository factory, and `tests/infrastructure/test_opportunity_history_shared_contract.py` runs them against the in-memory reference adapter. The baseline covers revision and decision identity validation/preservation, idempotency/conflict behavior, parent-scoped revision IDs, globally unique decision IDs, decision lineage and policy checks, decision-history scoping by opportunity, ordering, timezone-aware recorded timestamps, snapshot preservation, and not-found behavior. CI passed for the latest inspected PR #494 head `57e5d74452b939cf9c7926191e8487a08b4261c7` (run [37916832548](https://github.com/palestiny/freelancer-automation-platform/actions/runs/37916832548)); this includes the new cross-opportunity history and decision-identity assertions. The PR remains unmerged and is a baseline, not a complete extraction of all adapter-neutral assertions.
- **Remaining contract-test work:** PR #494 is a reusable baseline, not a complete extraction of every existing adapter-specific assertion. Before adding a production adapter, compare the shared cases against `tests/infrastructure/test_opportunity_history_repository_contract.py`, move remaining genuinely provider-neutral invariants into shared cases, and run the same suite against both reference and production adapters. Keep adapter-specific failure, transaction, concurrency, backup, and recovery tests separate.
- Test duplicate identical writes and conflicting writes under concurrent calls and, where supported by the deployment, across independent processes.
- Test decision/revision races, foreign-key/lineage violations, transaction rollback, and uniqueness enforcement.
- Test interruption or simulated storage failure before, during, and after commit; document what callers may safely retry.
- Verify deterministic retrieval ordering across repeated runs and database query plans.

### Durability and recovery
- Demonstrate backup creation and restore into a clean environment.
- Verify restored record counts, canonical decode, identity uniqueness, and lineage integrity.
- Exercise recovery from interrupted migrations and document the safe rollback/forward-repair procedure.
- Record actual tested RPO/RTO evidence; do not label targets achieved based only on configuration.

### Security and operations
- Test unauthorized access and cross-business/tenant isolation where applicable.
- Verify credentials are not logged and database errors are surfaced without leaking secrets.
- Define readiness/health checks, storage latency/error metrics, alert ownership, and a runbook for storage outages.
- Measure read/write latency and contention under an agreed representative workload; record hardware, dataset size, concurrency, and methodology.

## 6. Migration and rollout requirements

- Production schema migrations are versioned, reviewed, repeatable where practical, and tested against both empty and populated databases.
- Migration execution has an explicit owner and concurrency guard; application startup must not race migrations across replicas.
- Define whether deployment uses expand/migrate/contract steps and how mixed application versions behave.
- Define import/backfill from the in-memory reference adapter only if real persisted pilot data exists; otherwise do not invent a migration requirement.
- Rollout starts in a non-production environment with backup/restore evidence and contract tests.
- Production enablement requires an explicit owner decision after the acceptance gate passes.

## 7. Acceptance gate

The gate may be marked **PASS** only when all required evidence is linked and the owner approves:

- [ ] Deployment topology and expected load documented.
- [ ] Durability, RPO/RTO, backup, restore, and retention requirements decided.
- [ ] Candidate comparison completed against those requirements.
- [ ] Storage technology and deployment ownership explicitly approved.
- [ ] Provider-neutral adapter design and transaction boundaries reviewed.
- [ ] Shared contract suite passes against the selected adapter.
- [ ] Cross-process concurrency and conflict semantics verified where applicable.
- [ ] Backup/restore and migration recovery tested.
- [ ] Security/isolation requirements verified.
- [ ] Representative performance measurements recorded.
- [ ] Operations runbook, observability, and failure/retry semantics documented.
- [ ] Rollout and rollback plan approved.

A missing or unmeasured item is **GAP** or **NOT PROVEN**, not PASS. Unit-test success alone does not satisfy durability, concurrency, backup, restore, or performance requirements.

## 8. Explicitly deferred

Until this gate is approved and its requirements are known, defer:

- database/vendor selection;
- production adapter implementation;
- schema migrations and deployment automation;
- production rollout;
- API/UI integration;
- evidence-registry freshness and persistence of Evidence/EvaluationContext fields absent from the current pipeline result;
- distributed worker or queue infrastructure.

## 9. Owner decisions to record

1. Intended first deployment topology:
2. Expected workload and concurrency:
3. Durability / RPO / RTO:
4. Backup, restore, retention:
5. Security and tenant isolation:
6. Candidate selected and rationale:
7. Required production acceptance evidence:
8. Owner approval and date:

Until these fields and the acceptance gate are resolved, this document remains a draft and no production persistence technology is authorized.
