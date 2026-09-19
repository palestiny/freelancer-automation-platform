# Design Gate — Action Authorization & Progressive Autonomy

**Status:** APPROVED — V1 authorization artifact; execution remains outside this boundary.

## Purpose

Define how an explicit policy review can become authorization for a requested action without coupling authorization to execution.

## V1 Decisions

Policy review remains responsible for POLICY_SATISFIED, POLICY_NOT_SATISFIED, and REVIEW_REQUIRED. Authorization adds AUTHORIZED, HUMAN_APPROVAL_REQUIRED, NOT_AUTHORIZED, and SAFETY_BLOCKED.

V1 uses progressive-autonomy levels L0 OBSERVE, L1 RECOMMEND, L2 PREPARE, L3 EXECUTE_WITH_APPROVAL, L4 EXECUTE_AUTOMATICALLY_WITHIN_POLICY, and L5 OPTIMIZE_WITHIN_POLICY. An action cannot be authorized above the maximum autonomy explicitly supplied by policy.

V1 action classes are INFORMATIONAL, REVERSIBLE_EXTERNAL, IRREVERSIBLE_EXTERNAL, and FINANCIAL. IRREVERSIBLE_EXTERNAL and FINANCIAL actions are never automatically authorized by this domain slice.

Authorization preserves policy_id, policy_version, requested_autonomy_level, and maximum_autonomy_level. No policy mutation occurs inside authorization.

Authorization requires a policy-satisfied review. Incomplete or context-invalid evidence cannot authorize an action.

ActionAuthorization is an immutable evidence/control artifact. It does not execute, enqueue, schedule, submit, spend, communicate, or mutate external state.

## Non-Goals

No execution adapter, queue, worker, marketplace API, payment provider, campaign spend, client communication, or capital movement is implemented.
