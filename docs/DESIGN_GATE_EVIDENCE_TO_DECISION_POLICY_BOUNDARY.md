# Design Gate — Evidence-to-Decision Policy Boundary

**Status:** APPROVED — V1 policy boundary only; no automatic decision execution.

## Purpose

Define the boundary between composed evidence and a future explicit business decision. The current evidence layer must not silently become policy.

## V1 Decision Object

A future decision-support consumer may accept:
- composed descriptive/inferential evidence
- an explicit decision policy
- explicit policy version
- explicit required evidence conditions

It may return:
- SUPPORTS
- DOES_NOT_SUPPORT
- INSUFFICIENT_EVIDENCE
- POLICY_INAPPLICABLE

## Rules

1. Evidence composition and policy evaluation remain separate.
2. Policies are explicit, versioned inputs; no hidden thresholds.
3. Statistical significance is never a universal decision rule.
4. Evidence quality and source reliability remain separate inputs.
5. Insufficient evidence cannot be converted into a positive or negative business decision.
6. Policy evaluation produces a decision-support artifact only.
7. No automatic lifecycle transition, portfolio action, spending, execution, or policy mutation.
8. Any executable policy requires a later authorization/execution design gate.
