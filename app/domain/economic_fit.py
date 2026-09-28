from dataclasses import dataclass
from enum import Enum
from math import isfinite


class EconomicMetric(str, Enum):
    EXPECTED_PROFIT = "expected_profit"
    EXPECTED_MARGIN = "expected_margin"
    EXPECTED_PROFIT_PER_HOUR = "expected_profit_per_hour"
    EXPECTED_COST = "expected_cost"
    EXPECTED_REVENUE = "expected_revenue"


class EconomicComparisonOperator(str, Enum):
    MINIMUM = "MINIMUM"
    MAXIMUM = "MAXIMUM"


@dataclass(frozen=True)
class EconomicConstraint:
    constraint_id: str
    metric: EconomicMetric | str
    operator: EconomicComparisonOperator | str
    threshold: int | float
    unit: str
    currency: str | None
    evidence_refs: tuple[str, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.constraint_id, str) or not self.constraint_id.strip():
            raise ValueError("constraint_id must not be empty")

        try:
            metric = EconomicMetric(self.metric)
        except (TypeError, ValueError) as exc:
            raise ValueError("metric must be a supported EconomicMetric") from exc

        try:
            operator = EconomicComparisonOperator(self.operator)
        except (TypeError, ValueError) as exc:
            raise ValueError(
                "operator must be MINIMUM or MAXIMUM"
            ) from exc

        if isinstance(self.threshold, bool) or not isinstance(
            self.threshold, (int, float)
        ):
            raise TypeError("threshold must be numeric")
        if not isfinite(float(self.threshold)):
            raise ValueError("threshold must be finite")

        if not isinstance(self.unit, str) or not self.unit.strip():
            raise ValueError("unit must not be empty")
        if self.currency is not None and (
            not isinstance(self.currency, str) or not self.currency.strip()
        ):
            raise ValueError("currency must be a non-empty string or None")

        if not isinstance(self.evidence_refs, tuple):
            raise TypeError("evidence_refs must be a tuple")
        if not self.evidence_refs:
            raise ValueError("evidence_refs must not be empty")
        if any(
            not isinstance(value, str) or not value.strip()
            for value in self.evidence_refs
        ):
            raise ValueError("evidence_refs must contain non-empty strings")
        if len(set(self.evidence_refs)) != len(self.evidence_refs):
            raise ValueError("evidence_refs must contain unique references")

        object.__setattr__(self, "metric", metric)
        object.__setattr__(self, "operator", operator)
