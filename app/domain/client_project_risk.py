from dataclasses import dataclass
from enum import Enum


class RiskScope(str, Enum):
    CLIENT = "CLIENT"
    PROJECT = "PROJECT"


class RiskComparisonOperator(str, Enum):
    ALLOWED_VALUES = "ALLOWED_VALUES"


@dataclass(frozen=True)
class RiskConstraint:
    constraint_id: str
    scope: RiskScope | str
    signal: str
    operator: RiskComparisonOperator | str
    expected_values: tuple[str, ...]
    evidence_refs: tuple[str, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.constraint_id, str) or not self.constraint_id.strip():
            raise ValueError("constraint_id must not be empty")

        try:
            scope = RiskScope(self.scope)
        except (TypeError, ValueError) as exc:
            raise ValueError("scope must be a supported RiskScope") from exc

        if not isinstance(self.signal, str) or not self.signal.strip():
            raise ValueError("signal must not be empty")

        try:
            operator = RiskComparisonOperator(self.operator)
        except (TypeError, ValueError) as exc:
            raise ValueError(
                "operator must be a supported RiskComparisonOperator"
            ) from exc

        if not isinstance(self.expected_values, tuple):
            raise TypeError("expected_values must be a tuple")
        if not self.expected_values:
            raise ValueError("expected_values must not be empty")
        if any(
            not isinstance(value, str) or not value.strip()
            for value in self.expected_values
        ):
            raise ValueError("expected_values must contain non-empty strings")

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
            raise ValueError("evidence_refs must not contain duplicates")

        object.__setattr__(self, "scope", scope)
        object.__setattr__(self, "operator", operator)
