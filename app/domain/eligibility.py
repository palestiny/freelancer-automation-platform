from dataclasses import dataclass


@dataclass(frozen=True)
class EligibilityConstraint:
    constraint_id: str
    evidence_refs: tuple[str, ...]
    allowed_values: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.constraint_id.strip():
            raise ValueError("constraint_id must not be empty")
        if not self.evidence_refs:
            raise ValueError("eligibility constraint requires evidence references")
        if any(not isinstance(value, str) or not value.strip() for value in self.evidence_refs):
            raise ValueError("evidence_refs must contain non-empty strings")
        if len(set(self.evidence_refs)) != len(self.evidence_refs):
            raise ValueError("evidence_refs must not contain duplicates")
        if not self.allowed_values:
            raise ValueError("eligibility constraint requires allowed values")
        if any(not isinstance(value, str) or not value.strip() for value in self.allowed_values):
            raise ValueError("allowed_values must contain non-empty strings")
        if len(set(self.allowed_values)) != len(self.allowed_values):
            raise ValueError("allowed_values must not contain duplicates")
