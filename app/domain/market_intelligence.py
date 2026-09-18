from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class MarketObservation:
    """Provider-independent observation of an external market signal."""

    topic: str
    observed_value: str
    source: str
    observed_at: datetime
    evidence_quality: int = 50

    def __post_init__(self) -> None:
        for name, value in (
            ("topic", self.topic),
            ("observed_value", self.observed_value),
            ("source", self.source),
        ):
            if not value.strip():
                raise ValueError(f"{name} cannot be empty")

        if not 0 <= self.evidence_quality <= 100:
            raise ValueError("evidence_quality must be between 0 and 100")


@dataclass(frozen=True)
class DemandSignal:
    """Derived demand assessment supported by market observations."""

    topic: str
    demand_strength: int
    evidence_quality: int
    supporting_observation_count: int

    def __post_init__(self) -> None:
        if not self.topic.strip():
            raise ValueError("topic cannot be empty")
        if not 0 <= self.demand_strength <= 100:
            raise ValueError("demand_strength must be between 0 and 100")
        if not 0 <= self.evidence_quality <= 100:
            raise ValueError("evidence_quality must be between 0 and 100")
        if self.supporting_observation_count <= 0:
            raise ValueError(
                "supporting_observation_count must be greater than zero"
            )
