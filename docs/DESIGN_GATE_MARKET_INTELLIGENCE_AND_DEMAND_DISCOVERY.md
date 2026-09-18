# Market Intelligence & Demand Discovery Design Gate

## Status

**APPROVED — V1 domain direction committed; first demand-signal foundation implemented.**

## Purpose

The platform must discover demand without treating external market data as business truth.

Market Intelligence converts external observations into evidence-aware demand signals that can feed Opportunity Intelligence and Business Model Discovery.

## Core Boundary

External data follows:

**External Observation → Normalization → Data Quality → Demand Signal → Opportunity Hypothesis → Business Model Hypotheses**

An observation is not automatically a demand signal, and a demand signal is not automatically a validated opportunity.

## Market Observation

A market observation records an externally observed statement with:

- source
- topic
- observed value
- observation timestamp
- evidence quality

The source is provenance, not proof of truth.

## Demand Signal

A demand signal is a derived representation of observed market demand.

V1 records:

- signal id
- topic
- demand strength
- evidence quality
- supporting observation count

Demand strength and evidence quality are bounded 0–100 derived assessments. They are not revenue forecasts.

## Existing Markets

Demand discovery must support both:

- emerging/new demand;
- established demand in competitive markets.

Established demand may be valuable because it proves market activity. Competition remains an input to venture/business-model evaluation.

## Evidence Discipline

Market Intelligence must preserve epistemic separation:

- FACT: externally established statement;
- OBSERVATION: recorded external observation;
- ESTIMATE: calculated approximation;
- ASSUMPTION: explicit premise;
- HYPOTHESIS: proposed explanation/business idea;
- FORECAST: forward-looking estimate;
- EXPERIMENT_RESULT: measured validation outcome.

No domain service may silently promote an observation into a fact or a forecast into an actual result.

## V1 Non-Goals

- web scraping implementation
- search-engine integration
- social API integration
- marketplace API integration
- proprietary data-provider dependency
- AI-provider dependency
- automated investment decisions
- automatic opportunity qualification from one signal
- final market-size calculation

## First TDD Slice

1. Represent a market observation with provenance and timestamp.
2. Reject empty observation fields and invalid evidence quality.
3. Represent a demand signal independently from raw observations.
4. Require at least one supporting observation.
5. Bound demand strength and evidence quality to 0–100.
6. Preserve source/provider independence.

## Follow-Up

Future gates may define:

- observation normalization
- source reliability policies
- trend detection
- demand persistence over time
- competitor analysis
- market sizing
- signal aggregation
- automated research capabilities
