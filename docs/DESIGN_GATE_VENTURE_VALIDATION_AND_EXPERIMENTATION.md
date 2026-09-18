# Design Gate — Venture Validation & Experimentation

**Status:** APPROVED — V1 domain direction committed; provider-independent validation experiment foundation implemented.

## Purpose

The platform must not treat an economically attractive venture thesis as proven merely because its research and estimates look promising.

Validation answers:

> What is the cheapest credible experiment that can produce decision-useful evidence about this thesis?

The validation domain turns explicit hypotheses into bounded, measurable experiments and preserves the resulting evidence.

## V1 Flow

**Venture Thesis → Validation Hypothesis → Experiment → Measurable Result → Explicit Decision → Evidence / Learning**

The experiment is a controlled test, not a guarantee of business success.

## V1 Experiment Contract

A validation experiment contains:
- hypothesis
- objective
- measurable success criterion
- controlled variants
- budget limit
- lifecycle status

A completed result contains:
- experiment outcome
- observed measurement
- whether the success criterion was met
- evidence produced
- explicit decision

## Result Decisions

- PROMOTE — evidence supports advancing the tested thesis
- REJECT — evidence contradicts the tested thesis enough to stop this path
- CONTINUE_TESTING — evidence is useful but insufficient for a final decision

INCONCLUSIVE is an experiment outcome, not an implicit approval.

No result silently changes venture lifecycle, policy, economics, or portfolio posture.

## Evidence Boundary

Experiment results become EXPERIMENT_RESULT evidence.

The domain preserves the distinction between hypothesis, forecast, observed experiment result, and business decision. A result does not rewrite the original hypothesis.

## Safety and Resource Boundary

V1 supports a budget limit as an experiment constraint. It does not execute spending, reserve capacity, contact customers, publish campaigns, or call external providers.

Those actions remain application/capability concerns governed by authorization and autonomy policy.

## Controlled Variants

Variants are explicit labels used to compare alternative hypotheses, offers, prices, messages, or execution approaches.

The domain does not prescribe statistical methodology in V1. Exact statistical significance, sample-size calculation, attribution, and experiment analysis policies remain future policy concerns.

## Non-Goals

V1 does not implement:
- marketplace or advertising APIs
- scraping
- customer communication
- automatic financial spend
- automatic venture promotion/rejection outside an explicit result
- statistical inference engines
- persistence
- scheduling
- portfolio allocation

## Design Decisions

1. Validation is provider-independent.
2. Experiments are bounded and measurable.
3. Controlled variants are first-class experiment data.
4. Experiment results become evidence.
5. Promotion/rejection is explicit.
6. Learning cannot silently rewrite policy.
7. External execution remains behind capabilities and authorization.

## Design Gate Outcome

Approved for V1 implementation of the provider-independent validation experiment domain foundation.
