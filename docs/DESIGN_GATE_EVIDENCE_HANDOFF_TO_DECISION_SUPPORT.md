# Design Gate — Evidence Handoff to Decision Support

**Status:** APPROVED — V1 explicit handoff from evidence composition to a downstream consumer.

## Purpose

Create a non-executing handoff artifact so downstream policy/decision systems can consume evidence without treating evidence composition itself as a decision.

## V1 Contract

Input:
- PerformanceEvidenceDecisionSupport
- explicit consumer_id

Output:
- business/metric/unit context
- consumer identity
- descriptive direction
- inferential status
- combined evidence posture
- statistical observation lineage
- handoff status

Handoff statuses:
- READY
- NOT_READY

NOT_READY applies when:
- context is invalid
- inferential evidence is unavailable

READY does not mean a business action is approved. It means the evidence artifact is structurally available to a named downstream consumer.

## Boundary

- no recommendation
- no score/rank
- no policy mutation
- no learning mutation
- no lifecycle mutation
- no portfolio allocation
- no execution
- no automatic consumer selection
