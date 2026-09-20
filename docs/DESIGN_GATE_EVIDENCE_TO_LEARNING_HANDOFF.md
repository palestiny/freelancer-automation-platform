# Design Gate — Evidence to Learning Handoff

**Status:** APPROVED — V1 explicit handoff from composed performance evidence to a non-executing learning recommendation.

## Purpose

Close the current gap between evidence composition and the existing learning boundary without allowing statistical evidence to silently mutate policy.

## V1 Contract

Input:
- PerformanceEvidenceDecisionSupport
- explicit learning target
- explicit recommendation statement

Output:
- LearningEvidenceHandoff
- evidence eligibility
- source observation lineage
- descriptive/inferential evidence posture
- explicit handoff type: POLICY_REVIEW or EXPERIMENT

Rules:
1. Only eligible statistical evidence may be handed off.
2. Descriptive evidence remains visible but does not become a policy automatically.
3. No score or ranking is created.
4. No policy, lifecycle, portfolio, or execution state is mutated.
5. The handoff is an evidence artifact/recommendation boundary.
6. The consumer must explicitly choose POLICY_REVIEW or EXPERIMENT.
7. Business, metric, and unit identity are preserved.
8. Statistical lineage remains intact.
