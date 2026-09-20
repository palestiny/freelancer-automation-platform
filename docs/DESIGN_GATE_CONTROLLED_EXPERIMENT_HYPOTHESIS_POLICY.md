# Design Gate — Controlled Experiment Hypothesis Policy

**Status:** APPROVED — V1 policy consumer of existing experiment evidence synthesis.

## Purpose

Translate an explicitly declared experiment hypothesis into a bounded policy-support result using existing descriptive and inferential evidence. This is a policy evaluation boundary, not winner selection or experiment execution.

## V1 Contract

Inputs:
- experiment/metric identity
- evidence synthesis for exactly two variants
- declared hypothesis direction: INCREASES or DECREASES
- minimum required evidence eligibility

Outputs:
- SUPPORTS_HYPOTHESIS
- DOES_NOT_SUPPORT_HYPOTHESIS
- INSUFFICIENT_EVIDENCE
- POLICY_INAPPLICABLE

Rules:
1. No winner selection or variant ranking.
2. No causal claim.
3. Statistical significance is required only when the declared policy says so; V1 policy requires eligible statistical evidence.
4. Descriptive movement must align with the declared hypothesis direction.
5. Evidence disagreement yields DOES_NOT_SUPPORT_HYPOTHESIS rather than being hidden.
6. No allocation change, lifecycle mutation, execution, or automatic follow-up.
7. Preserve experiment, metric, variant, and observation lineage.
