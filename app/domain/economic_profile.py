from dataclasses import dataclass


@dataclass(frozen=True)
class EconomicProfile:
    """Changeable, evidence-aware economic quality profile.

    Scores are derived assessments, not raw facts. The profile intentionally
    avoids a universal master score so future policies can optimize different
    objectives without changing the underlying business identity.
    """

    profitability_score: int
    profit_potential_score: int
    profit_stability_score: int
    demand_stability_score: int
    safety_score: int
    recurring_revenue_score: int
    automation_score: int
    capital_efficiency_score: int
    scalability_score: int
    evidence_quality_score: int

    def __post_init__(self) -> None:
        scores = {
            "profitability_score": self.profitability_score,
            "profit_potential_score": self.profit_potential_score,
            "profit_stability_score": self.profit_stability_score,
            "demand_stability_score": self.demand_stability_score,
            "safety_score": self.safety_score,
            "recurring_revenue_score": self.recurring_revenue_score,
            "automation_score": self.automation_score,
            "capital_efficiency_score": self.capital_efficiency_score,
            "scalability_score": self.scalability_score,
            "evidence_quality_score": self.evidence_quality_score,
        }
        for name, value in scores.items():
            if not isinstance(value, int) or isinstance(value, bool):
                raise TypeError(f"{name} must be an integer")
            if not 0 <= value <= 100:
                raise ValueError(f"{name} must be between 0 and 100")
