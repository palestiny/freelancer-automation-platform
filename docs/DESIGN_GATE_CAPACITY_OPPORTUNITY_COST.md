# Design Gate — Capacity Opportunity Cost Evidence

**Status:** APPROVED — V1 bounded opportunity-cost evidence.

## Purpose

Represent the economic cost of consuming constrained capacity when an alternative use of the same capacity has an explicit expected economic value.

## V1 Contract

Inputs:
- committed capacity quantity
- alternative expected profit for the same quantity
- selected use expected profit for the same quantity

Output:
- allocated quantity
- selected expected profit
- alternative expected profit
- opportunity cost = max(0, alternative expected profit - selected expected profit)
- evidence status

Rules:
1. Quantity must be positive and finite.
2. Expected profits must be finite.
3. Opportunity cost is evidence, not an allocation decision.
4. No ranking of alternatives is produced.
5. No portfolio action, capital movement, policy mutation, or execution occurs.
6. The alternative must represent the same resource unit; the domain does not infer equivalence.
