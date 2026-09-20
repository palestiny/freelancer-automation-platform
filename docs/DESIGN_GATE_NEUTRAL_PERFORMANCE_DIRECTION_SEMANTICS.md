# Design Gate — Neutral Performance Direction Semantics

**Status:** APPROVED — V1 hardening.

## Problem

The existing performance evidence consumer uses IMPROVING and DECLINING directly from the sign of a metric change. That silently assumes that increasing every metric is better and decreasing every metric is worse. This is invalid for metrics such as cost, latency, error rate, or defect count.

## Decision

V1 evidence must describe observed movement neutrally:
- INCREASED
- DECREASED
- NO_CHANGE

No domain-level claim that a movement is good/bad, improving/declining, favorable/unfavorable, or economically desirable is allowed without an explicit metric semantics policy.

Statistical mean difference direction follows the same neutral vocabulary.
