from dataclasses import dataclass
from enum import Enum


class EvidenceKind(Enum):
    FACT = "FACT"
    OBSERVATION = "OBSERVATION"
    ESTIMATE = "ESTIMATE"
    ASSUMPTION = "ASSUMPTION"
    HYPOTHESIS = "HYPOTHESIS"
    FORECAST = "FORECAST"
    EXPERIMENT_RESULT = "EXPERIMENT_RESULT"


@dataclass(frozen=True)
class Evidence:
    kind: EvidenceKind
    statement: str
    source: str | None = None
    confidence: float | None = None

    def __post_init__(self) -> None:
        if not self.statement.strip():
            raise ValueError("statement cannot be empty")
        if self.confidence is not None and not 0 <= self.confidence <= 1:
            raise ValueError("confidence must be between 0 and 1")
