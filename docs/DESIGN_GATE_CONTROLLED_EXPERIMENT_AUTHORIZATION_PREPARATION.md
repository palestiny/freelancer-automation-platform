# Design Gate — Controlled Experiment Authorization Preparation

**Status:** APPROVED — V1 non-authorizing preparation boundary.

## Purpose

Bridge an accepted controlled-experiment review decision into an explicit action-authorization request without granting authorization or executing the experiment.

## V1 Contract

Input:
- ExperimentPolicyReviewDecision
- explicit policy identity/version
- requested action class
- requested autonomy

Output:
- immutable ExperimentAuthorizationRequest

Rules:
1. Only an ACCEPT review decision can produce an authorization request.
2. REJECT and REQUEST_MORE_EVIDENCE remain non-authorizable.
3. The request is preparation evidence, not authorization.
4. The request preserves decision, handoff, experiment, metric, reviewer, rationale, policy outcome, and observation lineage.
5. No provider call, scheduling, allocation, execution, lifecycle mutation, payment, or capital movement occurs.
6. The existing generic action authorization boundary remains responsible for authorization.
7. Requested autonomy and action class are explicit inputs; they are not inferred from the experiment result.
8. The request does not imply that the requested action is safe or permitted.
