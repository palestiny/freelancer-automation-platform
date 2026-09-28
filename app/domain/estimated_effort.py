from dataclasses import dataclass


@dataclass(frozen=True)
class EffortConstraint:
    constraint_id: str
    maximum_value: int | float
    unit: str
    evidence_refs: tuple[str, ...]
    required_scope_refs: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.constraint_id.strip():
            raise ValueError("constraint_id must not be empty")
        if isinstance(self.maximum_value, bool) or not isinstance(
            self.maximum_value, (int, float)
        ):
            raise TypeError("maximum_value must be numeric")
        if self.maximum_value < 0:
            raise ValueError("maximum_value must not be negative")
        if not self.unit.strip():
            raise ValueError("unit must not be empty")
        if not self.evidence_refs:
            raise ValueError("evidence_refs must not be empty")
        if not self.required_scope_refs:
            raise ValueError("required_scope_refs must not be empty")
        for name, values in (
            ("evidence_refs", self.evidence_refs),
            ("required_scope_refs", self.required_scope_refs),
        ):
            if not isinstance(values, tuple):
                raise TypeError(f"{name} must be a tuple")
            if any(not isinstance(value, str) or not value.strip() for value in values):
                raise ValueError(f"{name} must contain non-empty strings")
            if len(set(values)) != len(values):
                raise ValueError(f"{name} must contain unique references")
