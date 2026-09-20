# Design Gate — Policy Identity Binding Across Review and Authorization

**Status:** APPROVED — V1 hardening.

Policy review and authorization must carry the same explicit policy identity and version. Authorization must not accept caller-supplied policy identity that differs from the policy actually used to produce the satisfied review.

- PolicyReviewPolicy owns policy_id and version.
- EvidencePolicyReview preserves those values.
- Action authorization verifies exact identity/version match.
- Mismatch produces NOT_AUTHORIZED.
- No default policy identity or implicit substitution exists.

This is traceability and safety hardening only; it does not change autonomy levels, action classes, execution, scheduling, provider selection, or policy evaluation semantics.
